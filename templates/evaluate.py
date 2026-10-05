from pathlib import Path

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    ConfusionMatrixDisplay
)


# ==============================
# SETTINGS
# ==============================

MODEL_PATH = "dog_cat_model.keras"

IMAGE_SIZE = (128, 128)
BATCH_SIZE = 32

CLASS_NAMES = ["Cat", "Dog"]


# ==============================
# CHECK MODEL
# ==============================

if not Path(MODEL_PATH).exists():
    print("ERROR: dog_cat_model.keras not found.")
    exit()


# ==============================
# LOAD MODEL
# ==============================

print("\nLoading trained model...")

model = tf.keras.models.load_model(MODEL_PATH)

print("Model loaded successfully!")


# ==============================
# LOAD DATASET
# ==============================

print("\nLoading dataset...")

dataset = tf.keras.utils.image_dataset_from_directory(
    ".",
    class_names=CLASS_NAMES,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False,
    label_mode="binary"
)


# ==============================
# GET TRUE LABELS + PREDICTIONS
# ==============================

true_labels = []
predicted_labels = []

print("\nRunning predictions...")

for images, labels in dataset:

    predictions = model.predict(
        images,
        verbose=0
    )

    predictions = predictions.flatten()

    predicted = (predictions >= 0.5).astype(int)

    true_labels.extend(
        labels.numpy().astype(int).flatten()
    )

    predicted_labels.extend(predicted)


true_labels = np.array(true_labels)
predicted_labels = np.array(predicted_labels)


# ==============================
# METRICS
# ==============================

accuracy = accuracy_score(
    true_labels,
    predicted_labels
)

precision = precision_score(
    true_labels,
    predicted_labels,
    zero_division=0
)

recall = recall_score(
    true_labels,
    predicted_labels,
    zero_division=0
)

f1 = f1_score(
    true_labels,
    predicted_labels,
    zero_division=0
)


# ==============================
# PRINT RESULTS
# ==============================

print("\n")
print("======================================")
print("       DOG vs CAT MODEL EVALUATION")
print("======================================")

print(f"Accuracy  : {accuracy * 100:.2f}%")
print(f"Precision : {precision * 100:.2f}%")
print(f"Recall    : {recall * 100:.2f}%")
print(f"F1 Score  : {f1 * 100:.2f}%")

print("======================================")


# ==============================
# CLASSIFICATION REPORT
# ==============================

print("\nClassification Report:\n")

print(
    classification_report(
        true_labels,
        predicted_labels,
        target_names=CLASS_NAMES,
        zero_division=0
    )
)


# ==============================
# CONFUSION MATRIX
# ==============================

cm = confusion_matrix(
    true_labels,
    predicted_labels
)

print("Confusion Matrix:")
print(cm)


# ==============================
# SAVE CONFUSION MATRIX
# ==============================

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=CLASS_NAMES
)

disp.plot()

plt.title("Dog vs Cat - Confusion Matrix")

plt.savefig(
    "confusion_matrix.png",
    dpi=200,
    bbox_inches="tight"
)

plt.show()


print("\nConfusion matrix saved as:")
print("confusion_matrix.png")