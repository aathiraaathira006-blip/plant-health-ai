import os

dataset_path = "dataset"

classes = [
    "Tomato___Early_blight",
    "Tomato___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy"
]

print("\n🌱 Plant Disease Dataset Check\n")

total = 0

for class_name in classes:

    folder = os.path.join(dataset_path, class_name)

    images = [
        file for file in os.listdir(folder)
        if file.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    print(f"{class_name}: {len(images)} images")

    total += len(images)

print("\nTotal images:", total)