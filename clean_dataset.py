import os

dataset_path = "dataset"

classes = [
    "Tomato___Early_blight",
    "Tomato___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy"
]

target_counts = {
    "Tomato___Early_blight": 500,
    "Tomato___healthy": 500,
    "Potato___Early_blight": 500,
    "Potato___Late_blight": 500,
    "Potato___healthy": 152
}

for class_name in classes:

    folder = os.path.join(dataset_path, class_name)

    images = [
        file for file in os.listdir(folder)
        if file.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    target = target_counts[class_name]

    if len(images) > target:

        extra_images = images[target:]

        for image in extra_images:
            os.remove(os.path.join(folder, image))

        print(f"{class_name}: Removed {len(extra_images)} extra image(s)")

    else:
        print(f"{class_name}: No extra images")

print("\n✅ Dataset cleaned!")