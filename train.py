import csv
from pathlib import Path

import matplotlib.pyplot as plt
import tensorflow as tf

# Dataset
DATA_DIR = Path(".")
PROJECT_DIR = Path(__file__).resolve().parent


def save_training_history(history, output_dir):
    """Save epoch metrics to CSV and plot training and validation metrics."""
    metrics = history.history
    epoch_count = len(metrics["accuracy"])
    epochs = range(1, epoch_count + 1)
    output_dir = Path(output_dir)

    # Keep the complete metrics returned by Keras for later review.
    history_path = output_dir / "training_history.csv"
    metric_names = list(metrics)
    with history_path.open("w", newline="", encoding="utf-8") as history_file:
        writer = csv.writer(history_file)
        writer.writerow(["epoch", *metric_names])
        for epoch_index in range(epoch_count):
            writer.writerow([
                epoch_index + 1,
                *(metrics[name][epoch_index] for name in metric_names),
            ])

    # Plot training and validation accuracy.
    figure, axis = plt.subplots(figsize=(8, 5))
    axis.plot(epochs, metrics["accuracy"], label="Training Accuracy")
    axis.plot(epochs, metrics["val_accuracy"], label="Validation Accuracy")
    axis.set_title("Dog vs Cat Training and Validation Accuracy")
    axis.set_xlabel("Epochs")
    axis.set_ylabel("Accuracy")
    axis.legend()
    axis.grid(True, linestyle="--", alpha=0.4)
    figure.tight_layout()
    figure.savefig(output_dir / "training_accuracy.png", dpi=200)
    plt.close(figure)

    # Plot training and validation loss.
    figure, axis = plt.subplots(figsize=(8, 5))
    axis.plot(epochs, metrics["loss"], label="Training Loss")
    axis.plot(epochs, metrics["val_loss"], label="Validation Loss")
    axis.set_title("Dog vs Cat Training and Validation Loss")
    axis.set_xlabel("Epochs")
    axis.set_ylabel("Loss")
    axis.legend()
    axis.grid(True, linestyle="--", alpha=0.4)
    figure.tight_layout()
    figure.savefig(output_dir / "training_loss.png", dpi=200)
    plt.close(figure)

    print(f"Training history saved as: {history_path}")
    print(f"Accuracy graph saved as: {output_dir / 'training_accuracy.png'}")
    print(f"Loss graph saved as: {output_dir / 'training_loss.png'}")

print("TensorFlow version:", tf.__version__)
print("Loading dataset...")

# Load training data
train_ds = tf.keras.utils.image_dataset_from_directory(
    DATA_DIR,
    class_names=["Cat", "Dog"],
    validation_split=0.2,
    subset="training",
    seed=42,
    image_size=(128, 128),
    batch_size=32,
    label_mode="binary"
)

# Load validation data
val_ds = tf.keras.utils.image_dataset_from_directory(
    DATA_DIR,
    class_names=["Cat", "Dog"],
    validation_split=0.2,
    subset="validation",
    seed=42,
    image_size=(128, 128),
    batch_size=32,
    label_mode="binary"
)

print("Classes:", train_ds.class_names)

# Improve performance
AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.prefetch(AUTOTUNE)
val_ds = val_ds.prefetch(AUTOTUNE)

# CNN Model
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(128, 128, 3)),

    tf.keras.layers.Rescaling(1.0 / 255),

    tf.keras.layers.Conv2D(32, (3, 3), activation="relu"),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Conv2D(64, (3, 3), activation="relu"),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Conv2D(128, (3, 3), activation="relu"),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Flatten(),

    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dropout(0.3),

    tf.keras.layers.Dense(1, activation="sigmoid")
])

# Compile
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

print("\nModel created successfully!")
model.summary()

# Train
print("\nStarting training...\n")

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=5
)

# Save model
model.save("dog_cat_model.keras")

# Save the training metrics and graphs in the project root.
save_training_history(history, PROJECT_DIR)

print("\n================================")
print("TRAINING COMPLETE!")
print("Model saved as: dog_cat_model.keras")
print("================================")