import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import graphviz
import pydot
from importlib import reload

reload(keras.utils)
from tensorflow.keras.utils import plot_model


# Create the dataset
def load_images_in_dataset(path: str):
    return keras.preprocessing.image_dataset_from_directory(
        path,
        label="inferred", label_mode="int", class_name=["mask", "no_mask"],
        color_mode="rgb",
        batch_size=64, image_size=(150, 150))


def pre_treat_images(dataset):
    cropper = keras.layers.CenterCrop(height=150, width=150)
    scaler = keras.layers.Rescaling(scale=1.0 / 255)

    return scaler(cropper(dataset))


def model(input_shape, num_classes):
    inputs = keras.Input(shape=input_shape)
    # Image augmentation block
    x = keras.data_augmentation(inputs)

    # Entry block
    x = keras.layers.Rescaling(1.0 / 255)(x)
    x = keras.layers.Conv2D(32, 3, strides=2, padding="same")(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.Activation("relu")(x)

    x = keras.layers.Conv2D(64, 3, padding="same")(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.Activation("relu")(x)

    previous_block_activation = x  # Set aside residual

    for size in [128, 256, 512, 728]:
        x = keras.layers.Activation("relu")(x)
        x = keras.layers.SeparableConv2D(size, 3, padding="same")(x)
        x = keras.layers.BatchNormalization()(x)

        x = keras.layers.Activation("relu")(x)
        x = keras.layers.SeparableConv2D(size, 3, padding="same")(x)
        x = keras.layers.BatchNormalization()(x)

        x = keras.layers.MaxPooling2D(3, strides=2, padding="same")(x)

        # Project residual
        residual = keras.layers.Conv2D(size, 1, strides=2, padding="same")(
            previous_block_activation
        )
        x = keras.layers.add([x, residual])  # Add back residual
        previous_block_activation = x  # Set aside next residual

    x = keras.layers.SeparableConv2D(1024, 3, padding="same")(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.Activation("relu")(x)

    x = keras.layers.GlobalAveragePooling2D()(x)
    if num_classes == 2:
        activation = "sigmoid"
        units = 1
    else:
        activation = "softmax"
        units = num_classes

    x = keras.layers.Dropout(0.5)(x)
    outputs = keras.layers.Dense(units, activation=activation)(x)
    return keras.Model(inputs, outputs)

def create_model():
    image_size = (150, 150)
    batch_size = 32

    # Generate dataset
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        "C:\\Users\\julie\\Documents\\M1_Project\\test_nnl\\Train",
        validation_split=0.2,
        subset="training",
        seed=1337,
        image_size=image_size,
        batch_size=batch_size
    )
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        "C:\\Users\\julie\\Documents\\M1_Project\\test_nnl\\Validation",
        validation_split=0.2,
        subset="validation",
        seed=1337,
        image_size=image_size,
        batch_size=batch_size
    )

    # plt.figure(figsize=(10, 10))
    # for images, labels in train_ds.take(1):
    #    for i in range(9):
    #        ax = plt.subplot(3, 3, i+1)
    #        plt.imshow(images[i].numpy().astype("uint8"))
    #        plt.title(int(labels[i]))
    #        plt.axis("off")
    # plt.show()

    # Data augmentation : introduce diversity with random transformation

    data_augmentation = keras.Sequential(
        [keras.layers.RandomFlip("horizontal"),
         keras.layers.RandomRotation(0.1)
         ]
    )

    # plt.figure(figsize=(10, 10))
    # for images, labels in train_ds.take(1):
    #    for i in range(9):
    #        augmented_images = data_augmentation(images)
    #        ax = plt.subplot(3, 3, i+1)
    #        plt.imshow(augmented_images[0].numpy().astype("uint8"))
    #        plt.axis("off")
    # plt.show()

    #
    model = keras.model(input_shape=image_size + (3,), num_classes=2)
    plot_model(model, show_shapes=True)

    epochs = 50

    callbacks = [
        keras.callbacks.ModelCheckpoint("save_at_{epoch}.h5"),
    ]
    model.compile(
        optimizer=keras.optimizers.Adam(1e-3),
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )
    model.fit(
        train_ds, epochs=epochs, callbacks=callbacks, validation_data=val_ds,
    )

    model.save(r"./test_save ", save_format='h5')


if __name__ == '__main__':
    # Run with new

    image_size = (150, 150)

    img = keras.preprocessing.image.load_img(
        "C:\\Users\\julie\\Documents\\M1_Project\\NNL_Mask\\Images\\Images from 0 to 99\\maksssksksss14 .png", target_size=image_size
    )
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create batch axis

    model = keras.models.load_model("./test_save")

    predictions = model.predict(img_array)
    score = predictions[0]
    print(
        "This image is %.2f percent mask and %.2f percent no mask."
        % (100 * (1 - score), 100 * score)
    )


