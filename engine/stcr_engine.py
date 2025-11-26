# ============================================================
# stcr_engine.py — Targeted Yield Equation Solver
# Uses AST for safe evaluation of math strings.
# Handles ON, OP, OK (Organic variables) correctly.
# ============================================================
import ast
import operator
from engine.normalizer import normalize_soil

# Allowed mathematical operations (Security whitelist)
_ALLOWED_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.Pow: operator.pow,
}

def safe_eval_expr(expr, vars_dict):
    """
    Parses and evaluates a math string safely without using eval().
    Example: "4.25*T - 0.5*SN" -> Result
    """
    if not expr: return 0.0
    try:
        # Parse the expression into an Abstract Syntax Tree
        tree = ast.parse(expr, mode='eval')
        return _eval_node(tree.body, vars_dict)
    except Exception as e:
        # If parsing fails, return 0 (Fail safe)
        return 0.0

def _eval_node(node, vars_dict):
    # Number literal
    if isinstance(node, ast.Num): return node.n
    # Constant (Python 3.8+)
    if isinstance(node, ast.Constant): return node.value
    # Variable Name (T, SN, ON etc.)
    if isinstance(node, ast.Name): return vars_dict.get(node.id, 0.0)
    
    # Binary Operation (A + B)
    if isinstance(node, ast.BinOp):
        op = _ALLOWED_OPS.get(type(node.op))
        if op: return op(_eval_node(node.left, vars_dict), _eval_node(node.right, vars_dict))
        
    # Unary Operation (-A)
    if isinstance(node, ast.UnaryOp):
        op = _ALLOWED_OPS.get(type(node.op))
        if op: return op(_eval_node(node.operand, vars_dict))
        
    return 0.0

def compute_stcr(stcr_entry, soil, T, npk_baseline):
    """
    Calculates nutrient requirement based on Target Yield (T).
    """
    eq = stcr_entry.get("equations", {})
    
    # Prepare Variables for Equation
    # Ensure all organic variables (ON, OP, OK) are present
    vars_dict = {
        "T": float(T) if T else 0.0,
        "SN": float(soil.get("SN", 0)),
        "SP": float(soil.get("SP", 0)),
        "SK": float(soil.get("SK", 0)),
        "ON": float(soil.get("ON", 0)), # Organic Nitrogen
        "OP": float(soil.get("OP", 0)), # Organic Phosphorus
        "OK": float(soil.get("OK", 0)), # Organic Potassium
    }

    # Evaluate Equations
    raw = {
        "N": safe_eval_expr(eq.get("N"), vars_dict),
        "P2O5": safe_eval_expr(eq.get("P2O5"), vars_dict),
        "K2O": safe_eval_expr(eq.get("K2O"), vars_dict)
    }

    # Clamp to 0 (Cannot recommend negative fertilizer)
    final = {k: max(v, 0) for k,v in raw.items()}
    
    # Stability Check
    # If STCR gives crazy high values (>300% of baseline), clamp it to avoid burning crops.
    warnings = []
    if npk_baseline:
        # Example: If Baseline N is 100, STCR shouldn't recommend 500.
        if final["N"] > 3.0 * npk_baseline["N"] and npk_baseline["N"] > 10:
            final["N"] = npk_baseline["N"] * 1.5
            warnings.append("STCR yield target too high for soil. N clamped to safe limit.")

    return {"raw": raw, "final": final, "warnings": warnings}