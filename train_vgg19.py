import tensorflow as tf
from tensorflow.keras.applications import VGG19
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import shutil

# Buat subset dataset biar ringan
def create_subset_dataset(original_dir, subset_dir, num_images_per_class=100):
    if not os.path.exists(subset_dir):
        os.makedirs(subset_dir)
        for split in ['train', 'val']:
            for label in ['NORMAL', 'PNEUMONIA']:
                src_dir = os.path.join(original_dir, split, label)
                dst_dir = os.path.join(subset_dir, split, label)
                os.makedirs(dst_dir)
                images = os.listdir(src_dir)[:num_images_per_class]
                for img in images:
                    shutil.copy(os.path.join(src_dir, img), dst_dir)

# Setup subset
original_dir = '/home/ghost00/Pneumonia-detection/pneumonia-prediction/chest_xray'
subset_dir = '/home/ghost00/Pneumonia-detection/pneumonia-prediction/chest_xray_subset'
create_subset_dataset(original_dir, subset_dir, num_images_per_class=100)

# Load VGG19
base_model = VGG19(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
for layer in base_model.layers:
    layer.trainable = False

# Tambah layer
x = Flatten()(base_model.output)
x = Dense(512, activation='relu')(x)
x = Dropout(0.5)(x)
x = Dense(128, activation='relu')(x)
output = Dense(2, activation='softmax')(x)
model = Model(inputs=base_model.input, outputs=output)

# Compile
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Data generator
train_datagen = ImageDataGenerator(rescale=1./255)
val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    f'{subset_dir}/train',
    target_size=(224, 224),
    batch_size=8,  # Kurangin batch size
    class_mode='categorical'
)
val_generator = val_datagen.flow_from_directory(
    f'{subset_dir}/val',
    target_size=(224, 224),
    batch_size=8,
    class_mode='categorical'
)

# Latih
model.fit(
    train_generator,
    epochs=3,  # Kurangin epoch
    validation_data=val_generator
)

# Simpen
model.save('/home/ghost00/Pneumonia-detection/pneumonia-prediction/vgg19_model.h5')

print("Model saved as vgg19_model.h5")
