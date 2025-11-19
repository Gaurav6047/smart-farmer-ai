from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import fertilizer


app = FastAPI(
    title="Smart Farmer Fertilizer Engine API",
    description="Precision nutrient recommendation engine using STCR + IPNS + soil testing.",
    version="1.0.0"
)

# ---------------------------
# CORS (Allow all for Streamlit / Web)
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Routes
# ---------------------------
app.include_router(fertilizer.router, prefix="/api/v1")


# ---------------------------
# Local testing
# ---------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
