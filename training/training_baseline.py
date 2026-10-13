import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import normalize
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)
import joblib

# Load embedded Training data and labels

INPUT_FILE = Path("data")
X_train = np.load(INPUT_FILE / "embeddings/train.npy")
y_train = pd.read_csv(INPUT_FILE / "splits/train.csv")["label"]
X_train_normalized = normalize(X_train,norm="l2")

# Verify Behaviour

print(f"X_train shape: {X_train.shape}")
print(f"y_train shape: {y_train.shape}")
print(f"Normalized embeddings: {X_train_normalized}")
print(f"Verify length of L2 Norm: {np.linalg.norm(X_train_normalized, axis=1)[:5]}")

# Train model with logistic regression

LR_model = LogisticRegression(max_iter=1000)
LR_model.fit(X_train_normalized,y_train)

print(f"Shape of LR Weights: {LR_model.coef_.shape}")
print(f"Shape of LR Bias: {LR_model.intercept_.shape}")

# Now load validation data

X_val = np.load(INPUT_FILE / "embeddings/val.npy")
y_val = pd.read_csv(INPUT_FILE / "splits/val.csv")["label"]
X_val_normalized = normalize(X_val, norm="l2")

print(f"X_val shape: {X_val.shape}")
print(f"y_val shape: {y_val.shape}")
print(f"Normalized embeddings: {X_val_normalized}")
print(f"Verify length of L2 Norm: {np.linalg.norm(X_val_normalized, axis=1)[:5]}")

# Now predict validation values

predicted_val = LR_model.predict(X_val_normalized)
predicted_prob = LR_model.predict_proba(X_val_normalized)

print(f"Predictions: {predicted_val[:5]}")
print(f"AI probabilities: {predicted_prob[:5, 1]}")

# Check accuracy, precision and co.

accuracy_val = accuracy_score(y_val,predicted_val)
precision_val = precision_score(y_val,predicted_val)
recall_val = recall_score(y_val,predicted_val)
f1_val =f1_score(y_val,predicted_val)
cm = confusion_matrix(y_val, predicted_val)

print(f"{accuracy_val:.2%}")
print(f"{precision_val:.2%}")
print(f"{recall_val:.2%}")
print(f"{f1_val:.2%}")
print(cm)

# Create consisive data frame to collect all gathered information so far
y_val_csv = pd.read_csv(INPUT_FILE / "splits/val.csv")
result = pd.DataFrame({
    "path": y_val_csv["path"].values,
    "label": y_val_csv["label"].values,
    "predicted_label": predicted_val,
    "ai_probability": predicted_prob[:, 1]
    })

errors = result[result["label"] != result["predicted_label"]]
false_positives = errors[(errors["label"] == 0) & (errors["predicted_label"] == 1)]
false_negatives = errors[(errors["label"] == 1) & (errors["predicted_label"] == 0)]

print(result.head())
print(errors.head())
print(false_positives.head())
print(false_negatives.head())

# Safe the model for future use
SAVING_PATH = Path("models")
joblib.dump(LR_model, SAVING_PATH / "LR_model.joblib")

# Reload and test model
loaded_LR_model = joblib.load(SAVING_PATH / "LR_model.joblib")

original_predictions = LR_model.predict(X_val_normalized)
loaded_predictions = loaded_LR_model.predict(X_val_normalized)

if np.array_equal(original_predictions, loaded_predictions):
    print(f"The predictions are identically!")
else:
    print(f"The predictions differ.")