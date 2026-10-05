import sys
from pathlib import Path

import numpy as np
import tensorflow as tf

MODEL_PATH = "dog_cat_model.keras"

if len(sys.argv) < 2:
    print('Usage: python predict.py "test.jpg"')
    sys.exit(1)

image_path = Path(sys.argv[1])

if not image_path.exists():
    print(f"Image not found: {image_path}")
    sys.exit(1)

if not Path(MODEL_PATH).exists():
    print(f"Model not found: {MODEL_PATH}")
    sys.exit(1)

# Load trained model
model = tf.keras.models.load_model(MODEL_PATH)

# Load image
image = tf.keras.utils.load_img(
    image_path,
    target_size=(128, 128)
)

image_array = tf.keras.utils.img_to_array(image)
image_array = np.expand_dims(image_array, axis=0)

# Predict
prediction = float(model.predict(image_array, verbose=0)[0][0])

if prediction >= 0.5:
    result = "Dog"
    confidence = prediction * 100
else:
    result = "Cat"
    confidence = (1 - prediction) * 100

print("\n==============================")
print("      DOG vs CAT RESULT")
print("==============================")
print("Prediction :", result)
print("Confidence :", f"{confidence:.2f}%")
print("==============================")