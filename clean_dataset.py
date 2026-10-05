from pathlib import Path
from PIL import Image

folders = ["Cat", "Dog"]
valid_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}

converted = 0
deleted = 0

for folder in folders:
    folder_path = Path(folder)

    print(f"\nChecking {folder}...")

    for file in folder_path.rglob("*"):
        if not file.is_file():
            continue

        if file.suffix.lower() not in valid_extensions:
            continue

        try:
            # Open image
            with Image.open(file) as img:
                img.load()

                # Convert everything to standard RGB
                rgb = img.convert("RGB")

                # Rewrite original file as standard JPEG
                temp_file = file.with_suffix(".clean.jpg")
                rgb.save(temp_file, "JPEG", quality=95)

            # Replace original with cleaned image
            file.unlink()
            clean_file = file.with_suffix(".clean.jpg")
            clean_file.rename(file)

            converted += 1
            print(f"Fixed: {file}")

        except Exception as e:
            print(f"BAD IMAGE: {file}")
            print(f"Reason: {e}")

            try:
                file.unlink()
                deleted += 1
                print("Deleted.")
            except Exception as delete_error:
                print(f"Could not delete: {delete_error}")

print("\n================================")
print("DATASET CLEANING COMPLETE")
print("Images converted:", converted)
print("Bad images deleted:", deleted)
print("================================")