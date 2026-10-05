# Dog vs Cat AI

A browser-based image classification project that uses a TensorFlow/Keras convolutional neural network (CNN) to classify an uploaded image as a cat or a dog. The Flask application displays the prediction, confidence score, and uploaded image.

## Project Objective

The objective is to build an end-to-end machine learning application: prepare a labeled image dataset, train and evaluate a CNN, and make the trained model available through an interactive web interface.

## Main Features

- Cat and dog image dataset organized in class folders.
- Dataset image cleaning and format conversion utility.
- CNN training with training and validation accuracy/loss history.
- Saved Keras model at `dog_cat_model.keras`.
- Evaluation metrics and a confusion matrix.
- Command-line prediction with `predict.py`.
- Flask web interface with image upload, drag and drop, immediate preview, and a loading state.
- Cat/Dog prediction, confidence percentage, confidence bar, and analyzed-image preview.
- Responsive interface with a “Try Another Image” action.

## Technologies

- Python
- TensorFlow / Keras
- Convolutional Neural Network (CNN)
- Flask
- HTML
- CSS
- JavaScript
- NumPy
- Pillow
- scikit-learn
- Matplotlib

## Workflow

```text
Dataset
   → Data Cleaning
   → CNN Training
   → Model Evaluation
   → Flask Backend
   → Web Interface
   → Prediction
```

1. **Dataset:** Images are stored in the `Cat/` and `Dog/` class folders.
2. **Data cleaning:** `clean_dataset.py` checks image files and converts valid images to standard RGB JPEG format.
3. **CNN training:** `train.py` loads the dataset, trains the CNN, saves the model, and writes training history and plots.
4. **Model evaluation:** `templates/evaluate.py` calculates classification metrics and saves a confusion matrix.
5. **Flask backend:** `app.py` loads the saved model, accepts uploaded images, and returns prediction data to the page.
6. **Web interface:** The HTML template and static CSS/JavaScript provide the upload experience and display the result.
7. **Prediction:** The model classifies the image as a cat or dog and the interface displays its confidence.

## CNN in Simple Terms

A CNN is a neural network designed to learn patterns in images. Early layers can learn simple visual features such as edges and textures; deeper layers combine those features into more meaningful patterns. The final layer uses the learned image features to estimate whether the image belongs to the cat or dog class.

This project uses a binary output with a sigmoid activation. The model receives images resized to **128 × 128** pixels. During training, images are divided into training and validation subsets.

## Model Evaluation

`templates/evaluate.py` compares the model's predicted labels with the labels from the dataset it loads and reports:

- **Accuracy:** The proportion of evaluated examples classified correctly.
- **Precision:** Of the examples predicted as a class, the proportion that truly belongs to that class.
- **Recall:** Of the examples belonging to a class, the proportion correctly identified.
- **F1 Score:** The harmonic mean of precision and recall.
- **Confusion Matrix:** A table showing correct and incorrect predictions for each class.

### Results

No saved evaluation report with metric values was present when this README was created. Run the evaluation script to obtain current values; do not treat example or placeholder values as measured results.

| Metric | Result |
| --- | --- |
| Accuracy | [Add actual accuracy here] |
| Precision | [Add actual precision here] |
| Recall | [Add actual recall here] |
| F1 Score | [Add actual F1 score here] |

The evaluation script currently loads images from the `Cat/` and `Dog/` directories without a separate held-out test split. For a robust estimate of generalization, evaluate on a distinct test set that was not used for training or model selection.

## Flask Web Application

The Flask app loads `dog_cat_model.keras` when `app.py` starts. On form submission, it saves the uploaded file in `uploads/`, loads and resizes the image for the model, runs prediction, then renders the prediction and confidence in the page. Uploaded image previews are served through the existing `/uploads/<filename>` route.

## Run on Windows

Open PowerShell in the project directory:

```powershell
cd C:\path\to\dog-vs-cat-ai
```

Activate the existing virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script activation, allow scripts for the current PowerShell process, then activate the environment:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Install the application dependencies if they are not already installed in the environment:

```powershell
python -m pip install tensorflow flask numpy pillow scikit-learn matplotlib
```

Start the Flask application:

```powershell
python app.py
```

Open this URL in a browser:

**http://127.0.0.1:5000**

The `dog_cat_model.keras` file must be in the project root before starting the app.

### Optional: Train or Evaluate

Training is not required to run the existing application. If you intentionally want to train the model in the future, run this from the project root:

```powershell
python train.py
```

This runs training and saves/updates `dog_cat_model.keras`, `training_history.csv`, `training_accuracy.png`, and `training_loss.png`.

To evaluate the saved model:

```powershell
python templates\evaluate.py
```

The evaluation script writes `confusion_matrix.png` in the current project directory.

### Optional: Command-Line Prediction

With the virtual environment active and the model in the project root:

```powershell
python predict.py test.jpg
```

Replace `test.jpg` with the path to an image file.

## Project Structure

```text
dog-vs-cat-ai/
├── Cat/                         # Cat class images
├── Dog/                         # Dog class images
├── uploads/                     # Images uploaded to the Flask app
├── static/
│   ├── script.js                # Preview, drag-and-drop, and loading state
│   └── style.css                # Responsive application styles
├── templates/
│   ├── evaluate.py              # Model evaluation script
│   └── index.html               # Flask/Jinja web page
├── .venv/                       # Local Python virtual environment
├── app.py                       # Flask application
├── clean_dataset.py             # Dataset image cleaning utility
├── dog_cat_model.keras          # Trained Keras model
├── predict.py                   # Command-line prediction script
├── train.py                     # CNN training and history/plot generation
├── test.jpg                     # Example image for prediction
├── training_history.csv         # Generated by train.py
├── training_accuracy.png        # Generated by train.py
├── training_loss.png            # Generated by train.py
└── confusion_matrix.png         # Generated by templates/evaluate.py
```

Generated plots and training history appear after their corresponding scripts have been run; they may not exist in a fresh checkout. The local `.venv/`, image dataset, uploaded images, and model file are generally environment-specific or large files and may be excluded from a GitHub repository. Document how to obtain them if you publish the project without them.

## Screenshots

Add screenshots of the application to a `screenshots/` directory, then link them here. No screenshot files were present when this README was created.

Suggested screenshots:

- Main upload page: `screenshots/home-page.png`
- Prediction result with confidence: `screenshots/prediction-result.png`
- Evaluation confusion matrix: `confusion_matrix.png`

## Future Improvements

- Apply transfer learning with a pretrained image classification model.
- Expand and balance the training dataset.
- Create a larger, separate, and representative unseen test set.
- Add additional data augmentation and model evaluation experiments.
- Deploy the application to a production hosting platform.
- Add cloud hosting and managed model storage.
- Extend classification to more animal classes.

## Notes

Model metrics depend on the dataset and evaluation procedure. Add measured results only after running evaluation on an appropriate test set; this README does not claim a particular accuracy or dataset size.
