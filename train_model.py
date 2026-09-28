import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import os
import json

# -----------------------------
# 1. Dataset settings
# -----------------------------

DATASET_PATH = "dataset"
IMG_SIZE = (224, 224)
BATCH_SIZE = 16
SEED = 123


# -----------------------------
# 2. Load dataset
# -----------------------------

train_dataset = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.2,
    subset="training",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.2,
    subset="validation",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

class_names = train_dataset.class_names

print("\nClasses:")
for i, name in enumerate(class_names):
    print(i, ":", name)


# -----------------------------
# 3. Save class names
# -----------------------------

with open("class_names.json", "w") as file:
    json.dump(class_names, file)

print("\n✅ Class names saved!")


# -----------------------------
# 4. Improve dataset performance
# -----------------------------

AUTOTUNE = tf.data.AUTOTUNE

train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
validation_dataset = validation_dataset.prefetch(buffer_size=AUTOTUNE)


# -----------------------------
# 5. Data augmentation
# -----------------------------

data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1)
])


# -----------------------------
# 6. Load MobileNetV2
# -----------------------------

base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(224, 224, 3)
)

base_model.trainable = False


# -----------------------------
# 7. Create AI model
# -----------------------------

inputs = layers.Input(shape=(224, 224, 3))

x = data_augmentation(inputs)

x = preprocess_input(x)

x = base_model(x, training=False)

x = layers.GlobalAveragePooling2D()(x)

x = layers.Dropout(0.2)(x)

outputs = layers.Dense(
    len(class_names),
    activation="softmax"
)(x)

model = models.Model(inputs, outputs)


# -----------------------------
# 8. Compile model
# -----------------------------

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)


# -----------------------------
# 9. Show model information
# -----------------------------

model.summary()


# -----------------------------
# 10. Train the model
# -----------------------------

print("\n🌱 Starting training...\n")

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=10
)


# -----------------------------
# 11. Save trained model
# -----------------------------

os.makedirs("model", exist_ok=True)

model.save("model/plant_disease_model.keras")

print("\n✅ Model training completed!")
print("✅ Model saved to:")
print("model/plant_disease_model.keras")