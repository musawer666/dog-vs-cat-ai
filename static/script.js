const uploadForm = document.querySelector(".upload-form");
const fileInput = document.querySelector("#image-input");
const dropZone = document.querySelector("#drop-zone");
const uploadContent = document.querySelector("#upload-content");
const selectedPreview = document.querySelector("#selected-preview");
const previewImage = document.querySelector("#preview-image");
const selectedName = document.querySelector("#selected-name");
const predictButton = document.querySelector("#predict-button");
let previewUrl;

function showSelectedImage(file) {
    if (!file) {
        return;
    }

    if (file.type && !file.type.startsWith("image/")) {
        fileInput.setCustomValidity("Please choose a valid image file.");
        fileInput.reportValidity();
        return;
    }

    fileInput.setCustomValidity("");
    if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
    }

    previewUrl = URL.createObjectURL(file);
    previewImage.src = previewUrl;
    previewImage.alt = `Preview of ${file.name}`;
    selectedName.textContent = file.name;
    uploadContent.hidden = true;
    selectedPreview.hidden = false;
}

fileInput.addEventListener("change", () => {
    showSelectedImage(fileInput.files[0]);
});

dropZone.addEventListener("keydown", (event) => {
    if (event.target === dropZone && (event.key === "Enter" || event.key === " ")) {
        event.preventDefault();
        fileInput.click();
    }
});

for (const eventName of ["dragenter", "dragover"]) {
    dropZone.addEventListener(eventName, (event) => {
        event.preventDefault();
        dropZone.classList.add("is-dragging");
    });
}

for (const eventName of ["dragleave", "drop"]) {
    dropZone.addEventListener(eventName, (event) => {
        event.preventDefault();
        dropZone.classList.remove("is-dragging");
    });
}

dropZone.addEventListener("drop", (event) => {
    const [file] = event.dataTransfer.files;
    if (!file) {
        return;
    }

    const transfer = new DataTransfer();
    transfer.items.add(file);
    fileInput.files = transfer.files;
    fileInput.dispatchEvent(new Event("change", { bubbles: true }));
});

uploadForm.addEventListener("submit", () => {
    predictButton.disabled = true;
    predictButton.querySelector(".button-label").hidden = true;
    predictButton.querySelector(".button-arrow").hidden = true;
    predictButton.querySelector(".button-loading").hidden = false;
});

document.querySelectorAll(".confidence-fill").forEach((fill) => {
    const confidence = Number.parseFloat(fill.dataset.confidence);
    if (Number.isFinite(confidence)) {
        const safeConfidence = Math.min(100, Math.max(0, confidence));
        requestAnimationFrame(() => {
            fill.style.width = `${safeConfidence}%`;
        });
    }
});
