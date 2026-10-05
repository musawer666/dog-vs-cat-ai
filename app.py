from flask import Flask, render_template, request, send_from_directory
import tensorflow as tf
import numpy as np
from pathlib import Path
from werkzeug.utils import secure_filename

app = Flask(__name__)

MODEL_PATH = "dog_cat_model.keras"
UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

Path(UPLOAD_FOLDER).mkdir(exist_ok=True)

model = tf.keras.models.load_model(MODEL_PATH)


@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    confidence = None
    image_path = None
    error = None

    if request.method == "POST":

        if "image" not in request.files:
            error = "Please select an image."

            return render_template(
                "index.html",
                prediction=prediction,
                confidence=confidence,
                image_path=image_path,
                error=error
            )

        file = request.files["image"]

        if file.filename == "":
            error = "Please select an image."

            return render_template(
                "index.html",
                prediction=prediction,
                confidence=confidence,
                image_path=image_path,
                error=error
            )

        filename = secure_filename(file.filename)

        file_path = Path(app.config["UPLOAD_FOLDER"]) / filename

        file.save(file_path)

        try:
            image = tf.keras.utils.load_img(
                file_path,
                target_size=(128, 128)
            )

            image_array = tf.keras.utils.img_to_array(image)

            image_array = np.expand_dims(
                image_array,
                axis=0
            )

            result = float(
                model.predict(
                    image_array,
                    verbose=0
                )[0][0]
            )

            if result >= 0.5:
                prediction = "Dog 🐶"
                confidence = result * 100
            else:
                prediction = "Cat 🐱"
                confidence = (1 - result) * 100

            image_path = "/uploads/" + filename

        except Exception as e:
            error = f"Prediction error: {e}"

    return render_template(
        "index.html",
        prediction=prediction,
        confidence=confidence,
        image_path=image_path,
        error=error
    )


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


if __name__ == "__main__":
    app.run(debug=True)