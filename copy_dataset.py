import os
import shutil

# Location of the original PlantVillage dataset
SOURCE = r"C:\Users\Athra\Downloads\PlantVillage-Dataset-master\PlantVillage-Dataset-master\raw\color"

# Your project's dataset folder
DESTINATION = "dataset"

# Number of images to copy from each class
LIMIT = 500

classes = [
    "Tomato___Early_blight",
    "Tomato___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy"
]

for class_name in classes:

    source_folder = os.path.join(SOURCE, class_name)
    destination_folder = os.path.join(DESTINATION, class_name)

    os.makedirs(destination_folder, exist_ok=True)

    images = [
        file for file in os.listdir(source_folder)
        if file.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    selected_images = images[:LIMIT]

    print(f"\nProcessing: {class_name}")
    print(f"Available images: {len(images)}")
    print(f"Copying images: {len(selected_images)}")

    for image in selected_images:

        source_file = os.path.join(source_folder, image)
        destination_file = os.path.join(destination_folder, image)

        shutil.copy2(source_file, destination_file)

print("\n✅ Dataset copying completed!")