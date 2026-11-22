
# ============================================================
# PRIVACY-PRESERVING CYBERATTACK DETECTION IN SMART HOSPITALS
# Using AI, Cloud Computing and Federated Learning
# MCA FINAL YEAR PROJECT
# ============================================================

import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# ============================================================
# CONFIGURATION
# ============================================================

RANDOM_STATE = 42
HOSPITALS = 3
ROUNDS = 10

os.makedirs("results", exist_ok=True)
os.makedirs("dataset", exist_ok=True)
os.makedirs("models", exist_ok=True)

np.random.seed(RANDOM_STATE)

# ============================================================
# 1. GENERATE SYNTHETIC HOSPITAL NETWORK DATA
# ============================================================

print("\n====================================")
print(" SMART HOSPITAL CYBERSECURITY SYSTEM")
print("====================================")

print("\nGenerating hospital network dataset...")

X, y = make_classification(
    n_samples=9000,
    n_features=20,
    n_informative=12,
    n_redundant=4,
    n_classes=2,
    weights=[0.70, 0.30],
    random_state=RANDOM_STATE
)

columns = [
    f"network_feature_{i}"
    for i in range(1, 21)
]

df = pd.DataFrame(X, columns=columns)
df["label"] = y

df.to_csv(
    "dataset/hospital_network.csv",
    index=False
)

print("Dataset generated successfully!")
print(df.head())

print("\nClass distribution:")
print(df["label"].value_counts())

# 0 = Normal traffic
# 1 = Cyberattack

# ============================================================
# 2. DATA PREPROCESSING
# ============================================================

print("\nPreprocessing network data...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=RANDOM_STATE,
    stratify=y
)

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

print("Preprocessing completed!")

# ============================================================
# 3. CENTRALIZED AI MODEL
# ============================================================

print("\nTraining centralized AI model...")

central_model = RandomForestClassifier(
    n_estimators=100,
    random_state=RANDOM_STATE,
    class_weight="balanced"
)

start_time = time.time()

central_model.fit(X_train, y_train)

central_time = time.time() - start_time

central_predictions = central_model.predict(X_test)

central_accuracy = accuracy_score(
    y_test,
    central_predictions
)

print("Centralized model accuracy:", central_accuracy)

# ============================================================
# 4. SIMULATE THREE HOSPITAL CLIENTS
# ============================================================

print("\nCreating hospital clients...")

indices = np.array_split(
    np.random.permutation(len(X_train)),
    HOSPITALS
)

clients = []

for i, idx in enumerate(indices):

    client_X = X_train[idx]
    client_y = y_train[idx]

    clients.append((client_X, client_y))

    print(
        f"Hospital {i+1}: "
        f"{len(client_X)} records"
    )

# ============================================================
# 5. FEDERATED LEARNING USING FEDAVG
# ============================================================

print("\nStarting Federated Learning...")

global_model = LogisticRegression(
    max_iter=1000,
    random_state=RANDOM_STATE
)

# Initialize global model
global_model.fit(
    X_train[:100],
    y_train[:100]
)

round_accuracies = []

start_time = time.time()

for round_number in range(1, ROUNDS + 1):

    local_models = []

    for client_X, client_y in clients:

        # Train local hospital model
        local_model = LogisticRegression(
            max_iter=1000,
            random_state=RANDOM_STATE
        )

        local_model.fit(client_X, client_y)

        local_models.append(
            (
                local_model.coef_,
                local_model.intercept_,
                len(client_X)
            )
        )

    # Federated Averaging
    total_samples = sum(
        item[2] for item in local_models
    )

    global_model.coef_ = sum(
        item[0] * item[2] / total_samples
        for item in local_models
    )

    global_model.intercept_ = sum(
        item[1] * item[2] / total_samples
        for item in local_models
    )

    predictions = global_model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    round_accuracies.append(accuracy)

    print(
        f"Round {round_number}: "
        f"Accuracy = {accuracy:.4f}"
    )

federated_time = time.time() - start_time

# ============================================================
# 6. FEDERATED MODEL EVALUATION
# ============================================================

print("\nEvaluating Federated Model...")

fed_predictions = global_model.predict(X_test)

fed_accuracy = accuracy_score(
    y_test,
    fed_predictions
)

fed_precision = precision_score(
    y_test,
    fed_predictions,
    zero_division=0
)

fed_recall = recall_score(
    y_test,
    fed_predictions,
    zero_division=0
)

fed_f1 = f1_score(
    y_test,
    fed_predictions,
    zero_division=0
)

print("\nFEDERATED LEARNING RESULTS")

print("Accuracy:", round(fed_accuracy, 4))
print("Precision:", round(fed_precision, 4))
print("Recall:", round(fed_recall, 4))
print("F1 Score:", round(fed_f1, 4))

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        fed_predictions,
        target_names=["Normal", "Attack"],
        zero_division=0
    )
)

# ============================================================
# 7. DIFFERENTIAL PRIVACY EXPERIMENT
# ============================================================

print("\nRunning Differential Privacy experiment...")

def add_gaussian_noise(model, noise_scale=0.05):

    noisy_model = LogisticRegression(
        max_iter=1000
    )

    noisy_model.classes_ = model.classes_.copy()

    noisy_model.coef_ = (
        model.coef_ +
        np.random.normal(
            0,
            noise_scale,
            model.coef_.shape
        )
    )

    noisy_model.intercept_ = (
        model.intercept_ +
        np.random.normal(
            0,
            noise_scale,
            model.intercept_.shape
        )
    )

    noisy_model.n_features_in_ = model.n_features_in_

    return noisy_model


private_model = add_gaussian_noise(global_model)

private_predictions = private_model.predict(X_test)

private_accuracy = accuracy_score(
    y_test,
    private_predictions
)

print(
    "Noisy model accuracy:",
    round(private_accuracy, 4)
)

# NOTE:
# Adding Gaussian noise to the final model parameters
# is only a demonstration. It is NOT a formally
# calibrated differential privacy mechanism.
# It does not establish a valid privacy budget.

# ============================================================
# 8. CYBERATTACK DETECTION
# ============================================================

print("\n====================================")
print(" CYBERATTACK DETECTION")
print("====================================")

def detect_attack(input_features):

    input_data = np.array(
        input_features
    ).reshape(1, -1)

    input_data = scaler.transform(input_data)

    prediction = global_model.predict(
        input_data
    )[0]

    probability = global_model.predict_proba(
        input_data
    )[0][1]

    if prediction == 1:

        print("\nWARNING: Suspicious network activity!")

        print(
            "Attack probability:",
            round(probability * 100, 2),
            "%"
        )

        return "ATTACK"

    else:

        print("\nNetwork activity appears normal.")

        print(
            "Attack probability:",
            round(probability * 100, 2),
            "%"
        )

        return "NORMAL"


# Example network record from generated dataset
sample = X_test[0]

detect_attack(sample)

# ============================================================
# 9. CLOUD COORDINATION SIMULATION
# ============================================================

print("\n====================================")
print(" CLOUD COORDINATION")
print("====================================")

print("Cloud coordinator started.")

for hospital_number in range(1, HOSPITALS + 1):

    print(
        f"Hospital {hospital_number}: "
        "Local model update prepared."
    )

print("Global model aggregation completed.")

print("Global model distributed to hospitals.")

# This is a local simulation of cloud coordination,
# not an actual cloud deployment.

# ============================================================
# 10. PERFORMANCE COMPARISON
# ============================================================

print("\n====================================")
print(" MODEL COMPARISON")
print("====================================")

comparison = pd.DataFrame({

    "Model": [
        "Centralized Random Forest",
        "Federated Logistic Regression",
        "Noisy Federated Model"
    ],

    "Accuracy": [
        accuracy_score(y_test, central_predictions),
        fed_accuracy,
        private_accuracy
    ],

    "Precision": [
        precision_score(y_test, central_predictions, zero_division=0),
        fed_precision,
        precision_score(y_test, private_predictions, zero_division=0)
    ],

    "Recall": [
        recall_score(y_test, central_predictions, zero_division=0),
        fed_recall,
        recall_score(y_test, private_predictions, zero_division=0)
    ],

    "F1 Score": [
        f1_score(y_test, central_predictions, zero_division=0),
        fed_f1,
        f1_score(y_test, private_predictions, zero_division=0)
    ]

})

print(comparison)

comparison.to_csv(
    "results/model_comparison.csv",
    index=False
)

# ============================================================
# 11. CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    y_test,
    fed_predictions
)

plt.figure(figsize=(6, 5))

plt.imshow(cm)

plt.title("Federated Cyberattack Detection")

plt.xlabel("Predicted Class")
plt.ylabel("Actual Class")

plt.xticks(
    [0, 1],
    ["Normal", "Attack"]
)

plt.yticks(
    [0, 1],
    ["Normal", "Attack"]
)

for i in range(2):
    for j in range(2):

        plt.text(
            j,
            i,
            str(cm[i, j]),
            ha="center",
            va="center"
        )

plt.colorbar()

plt.tight_layout()

plt.savefig(
    "results/confusion_matrix.png"
)

plt.show()

# ============================================================
# 12. FEDERATED LEARNING ACCURACY GRAPH
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(
    range(1, ROUNDS + 1),
    round_accuracies,
    marker="o"
)

plt.title("Federated Learning Performance")

plt.xlabel("Federated Rounds")
plt.ylabel("Accuracy")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "results/federated_accuracy.png"
)

plt.show()

# ============================================================
# 13. SAVE TRAINED MODELS
# ============================================================

import joblib

joblib.dump(
    global_model,
    "models/federated_model.pkl"
)

joblib.dump(
    central_model,
    "models/centralized_model.pkl"
)

joblib.dump(
    scaler,
    "models/scaler.pkl"
)

# ============================================================
# 14. FINAL PROJECT SUMMARY
# ============================================================

print("\n====================================")
print(" PROJECT EXECUTION COMPLETED")
print("====================================")

print("Dataset: Generated successfully")

print("Hospitals:", HOSPITALS)

print("Federated Rounds:", ROUNDS)

print(
    "Centralized Accuracy:",
    round(central_accuracy, 4)
)

print(
    "Federated Accuracy:",
    round(fed_accuracy, 4)
)

print(
    "Noisy Model Accuracy:",
    round(private_accuracy, 4)
)

print("\nGenerated files:")

print("dataset/hospital_network.csv")

print("results/model_comparison.csv")

print("results/confusion_matrix.png")

print("results/federated_accuracy.png")

print("models/federated_model.pkl")

print("\nSMART HOSPITAL CYBERSECURITY SYSTEM FINISHED!")
