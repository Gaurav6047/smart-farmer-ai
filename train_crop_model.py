import pandas as pd
import numpy as np
import pickle
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier

# -------------------------
# Load dataset
# -------------------------
df = pd.read_csv("datasets/Crop_recommendation.csv")

X = df.drop("label", axis=1)
y = df["label"]

# -------------------------
# Encode labels
# -------------------------
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# -------------------------
# Train-test split
# -------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# -------------------------
# Scale features
# -------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -------------------------
# Train Random Forest (best params)
# -------------------------
rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    min_samples_leaf=2,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)

rf.fit(X_train_scaled, y_train)

# -------------------------
# Evaluate
# -------------------------
pred = rf.predict(X_test_scaled)

print("Accuracy:", accuracy_score(y_test, pred))
print("\nClassification Report:\n", classification_report(y_test, pred, target_names=le.classes_))

# -------------------------
# Train final model on FULL dataset
# -------------------------
scaler_full = StandardScaler()
X_scaled_full = scaler_full.fit_transform(X)

rf_final = RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    min_samples_leaf=2,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)
rf_final.fit(X_scaled_full, y_encoded)

# -------------------------
# Save models
# -------------------------
os.makedirs("models", exist_ok=True)

with open("models/crop_rf_final.pkl", "wb") as f:
    pickle.dump(rf_final, f)

with open("models/scaler.pkl", "wb") as f:
    pickle.dump(scaler_full, f)

with open("models/label_encoder.pkl", "wb") as f:
    pickle.dump(le, f)

print("\nModel saved successfully in /models/")
