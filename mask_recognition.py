import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import graphviz
import pydot
from importlib import reload
import os

reload(keras.utils)
from tensorflow.keras.utils import plot_model

class MaskRecognitionModel:
    model: keras.Model
    name: str

    def __init__(self, name_or_path: str, mode:str):
        """If called with 'New' as a second parameter, it will define a new model named after the first parameter.\n
        If called with 'Load' as a second parameter, it will load the model at the path given in the first parameter."""
        image_size = (150, 150)
        if mode == "new" or mode == "New":
            self.name = name_or_path
            self.model = self.define_model(input_shape=image_size + (3,), num_classes=2)
        elif mode == "load" or mode == "Load":
            if os.path.isfile(name_or_path):
                self.model = self.load_model(name_or_path)


    # Function to modify for the test
    def define_model(self, input_shape, num_classes):
        inputs = keras.Input(shape=input_shape)

        data_augmentation = keras.Sequential(
            [
                keras.layers.RandomFlip("horizontal"),
                keras.layers.RandomRotation(0.1),
            ]
        )

        # Image augmentation block
        x = data_augmentation(inputs)

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


    def load_model(self, model_path:str):
        """Calls Keras' load_model method and stores the returned result as the current model.
        Literally what loading a model means."""
        self.name = model_path.split(f"{os.path.sep}")[-1].split(".")[0] # normalement c'est le dernier nom du path, sans extension (même si un model n'a pas d'extension actuellemnt)
        return keras.models.load_model(model_path)


    def save_model(self, path_save:str):
        self.model.save(path_save, save_format='h5')


    def train_model(self, path_train: str, path_valid: str):
        image_size = (150, 150)
        batch_size = 64

        # Generate dataset
        train_ds = tf.keras.preprocessing.image_dataset_from_directory(
            path_train,
            validation_split=0.2,
            subset="training",
            seed=1337,
            image_size=image_size,
            batch_size=batch_size)

        val_ds = tf.keras.preprocessing.image_dataset_from_directory(
            path_valid,
            validation_split=0.2,
            subset="validation",
            seed=1337,
            image_size=image_size,
            batch_size=batch_size)

        # Data augmentation : introduce diversity with random transformation
        data_augmentation = keras.Sequential(
            [keras.layers.RandomFlip("horizontal"),
             keras.layers.RandomRotation(0.1)
             ]
        )

        plot_model(self.model, show_shapes=True)

        epochs = 20

        callbacks = [
            keras.callbacks.ModelCheckpoint("save_at_{epoch}.h5"),
        ]
        self.model.compile(
            optimizer=keras.optimizers.Adam(1e-3),
            loss="binary_crossentropy",
            metrics=["accuracy"],
        )
        self.model.fit(
            train_ds, epochs=epochs, callbacks=callbacks, validation_data=val_ds,
        )


    def predict(self, filename: str, mode: str):
        score = self.test_image(filename)
        if mode == "categories":
            if score > 0.5:
                return "no mask"
            else:
                return "mask"
        elif mode == "probabilities":
            return("This image is %.2f percent mask and %.2f percent no mask."
                  % (100 * (1 - score), 100 * score))


    def test_image(self, img_path: str):
        # Run with new

        image_size = (150, 150)

        img = keras.preprocessing.image.load_img(
            img_path,
            target_size=image_size
        )
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)  # Create batch axis

        predictions = self.model.predict(img_array)

        # score = predictions[0]
        # print(
        #    "This image is %.2f percent mask and %.2f percent no mask."
        #    % (100 * (1 - score), 100 * score)
        # )
        return predictions[0]


    def test_multiple_image(self, path_dataset: str):
        path_sep = os.path.sep
        list_category = os.listdir(path_dataset)
        TP = 0
        TN = 0
        FP = 0
        FN = 0
        total = 0
        for category in list_category:
            for image in os.listdir(path_dataset + path_sep + category):
                total += 1
                score = self.test_image(path_dataset + path_sep + category + path_sep + image)
                if category == "mask":
                    if score <= 0.5:
                        TP += 1
                    else:
                        FP += 1
                if category == "no_mask":
                    if score > 0.5:
                        TN += 1
                    else:
                        FN += 1
        accuracy = (TP + TN) / total
        recall = TP / (TP + TN)
        precision = TP / (TP + FP)
        print(f"TP: {TP} // TN: {TN} // FP: {FP} // FN: {FN} // Total: {total}")
        print(f"Accuracy: {accuracy} // Recall: {recall} // Precision: {precision}")


    # if __name__ == '__main__':
        # Creer le model
        # setup_model("C:\\Users\\julie\\Documents\\M1_Project\\test_nnl\\Train",
        #              "C:\\Users\\julie\\Documents\\M1_Project\\test_nnl\\Validation",
        #              r"./mask_model")

        # Prédire une image
        # predict("C:\\Users\\julie\\Documents\\M1_Project\\NNL_Mask\\Images\\Images from 0 to 99\\maksssksksss4.png",
        #        "probabilities",
        #        "C:\\Users\\julie\\Documents\\M1_Project\\NNL_Mask\\Mask_Recognition\\mask_model")

        # Prédire plusieurs images, mesures
        # test_multiple_image("C:\\Users\\julie\\Documents\\M1_Project\\test_nnl\\Validation",
        #                    "C:\\Users\\julie\\Documents\\M1_Project\\NNL_Mask\\Mask_Recognition\\mask_model")


