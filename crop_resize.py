from PIL import Image
import os
from pathlib import Path


def process_images(input_folder: str, output_folder: str):
    """
    Process all 1080x1920 PNG images:
    - Crop centered to 887x1920
    - Resize to 1242x2688
    - Save to output folder
    """
    input_path = Path(input_folder)
    output_path = Path(output_folder)

    # Create output folder if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)

    # Supported extensions (case insensitive)
    valid_extensions = {'.png'}

    processed = 0
    skipped = 0

    for file in input_path.iterdir():
        if file.is_file() and file.suffix.lower() in valid_extensions:
            try:
                with Image.open(file) as img:

                    # Verify original size
                    if img.size != (1080, 1920):
                        print(f"Skipping {file.name}: Expected 1080x1920, got {img.size}")
                        skipped += 1
                        continue

                    # Crop centered: 887x1920
                    original_width = 1080
                    crop_width = 887
                    left = (original_width - crop_width) // 2  # 96
                    right = left + crop_width  # 983

                    cropped = img.crop((left, 0, right, 1920))

                    # Resize to 1242x2688
                    resized = cropped.resize((1242, 2688), Image.LANCZOS)

                    # Save with same filename
                    output_file = output_path / file.name
                    resized.save(output_file, format='PNG', optimize=True)

                    print(f"Processed: {file.name}")
                    processed += 1

            except Exception as e:
                print(f"Error processing {file.name}: {e}")
                skipped += 1

    print(f"\nDone! Processed: {processed} | Skipped: {skipped}")


if __name__ == "__main__":
    # === CONFIGURE THESE PATHS ===
    INPUT_FOLDER = "Input"  # Change to your input folder path
    OUTPUT_FOLDER = "Output"  # Change to your output folder path

    process_images(INPUT_FOLDER, OUTPUT_FOLDER)