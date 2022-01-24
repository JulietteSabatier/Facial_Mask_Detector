import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import graphviz
import pydot
from importlib import reload
import os
import cv2
import PIL.Image as Image
reload(keras.utils)


class MaskRecognitionModel:
    model: keras.Model
    name: str

    def __init__(self, name_or_path: str, mode: str):
        """If called with 'New' as a second parameter, it will define a new model named after the first parameter.\n
        If called with 'Load' as a second parameter, it will load the model at the path given in the first parameter."""
        image_size = (150, 150)
        if mode == "new" or mode == "New":
            self.name = name_or_path
            self.model = self.define_model(input_shape=image_size + (3,), num_classes=1)
        elif mode == "load" or mode == "Load":
            if os.path.isfile(name_or_path):
                self.model = self.load_model(name_or_path)

    # Function to modify for the test
    def define_model(self, input_shape: (int, int), num_classes: int):
        """ Define all the layers of the model we want to create """
        my_model = keras.Sequential(
            [
                keras.layers.RandomFlip("horizontal"),
                keras.layers.RandomRotation(0.1),
            ]
        )

        # filters : peu au début puis de plus en plus, faire par *2
        # kernel_size : (impair, impair) <=3 pour des images < 128x128 et <=7 pour plus grand, baisser la taille
        # strides : mostly (1,1) default, sometimes (2,2) in replacement of MaxPooling2D
        # padding : "same" -> volume size equivalent recommended , "valid" -> natural reduce of spacial dimension

        my_model.add(keras.layers.Conv2D(filters=32, kernel_size=(3, 3), padding="same", activation="relu"))
        my_model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))

        my_model.add(keras.layers.Conv2D(filters=64, kernel_size=(3, 3), padding="same", activation="relu"))
        my_model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))

        my_model.add(keras.layers.Conv2D(filters=128, kernel_size=(3, 3), padding="same", activation="relu"))
        my_model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))

        my_model.add(keras.layers.Dropout(0.2))

        my_model.add(keras.layers.Flatten())
        my_model.add(keras.layers.Dense(num_classes))
        my_model.add(keras.layers.Activation("sigmoid"))

        return my_model


    def load_model(self, model_path: str):
        """Calls Keras' load_model method and stores the returned result as the current model.
        Literally what loading a model means."""
        self.name = model_path.split(f"{os.path.sep}")[-1].split(".")[
            0]  # normalement c'est le dernier nom du path, sans extension (même si un model n'a pas d'extension actuellemnt)
        return keras.models.load_model(model_path)

    def save_model(self, path_save: str):
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

        # plot_model(self.model, show_shapes=True)

        epochs = 50

        self.model.compile(
            optimizer=keras.optimizers.Adam(1e-3),
            loss="binary_crossentropy",
            metrics=["accuracy"],
        )
        history = self.model.fit(
            train_ds, epochs=epochs, validation_data=val_ds,
        )

        acc = history.history['accuracy']
        val_acc = history.history['val_accuracy']
        loss = history.history['loss']
        val_loss = history.history['val_loss']

        epochs_range = range(epochs)

        plt.figure(figsize=(15, 15))
        plt.subplot(2, 2, 1)
        plt.plot(epochs_range, acc, label='Training Accuracy')
        plt.plot(epochs_range, val_acc, label='Validation Accuracy')
        plt.legend(loc='lower right')
        plt.title('Training and Validation Accuracy')

        plt.subplot(2, 2, 2)
        plt.plot(epochs_range, loss, label='Training Loss')
        plt.plot(epochs_range, val_loss, label='Validation Loss')
        plt.legend(loc='upper right')
        plt.title('Training and Validation Loss')
        plt.show()

    def predict(self, filename: str, mode: str):
        """ Function which predict if the image at the path filename contain a mask or not.
        Given the mode: probabilities or categories
        it will return the probabilities of each possibility or the category  """
        score = self.test_image(filename)
        if mode == "categories":
            if score > 0.5:
                return "no mask"
            else:
                return "mask"
        elif mode == "probabilities":
            return ("This image is %.2f percent mask and %.2f percent no mask."
                    % (100 * (1 - score), 100 * score))

    def test_image(self, img_path: str):
        """ Function which return the result of the model we create """
        # Run with new

        image_size = (150, 150)

        img = keras.preprocessing.image.load_img(
            img_path,
            target_size=image_size
        )
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)  # Create batch axis

        predictions = self.model.predict(img_array)

        return predictions[0]

    def image_detection(self, img_path: str, mode: str):
        """ Function which detect the faces in the given image.
        After that it crop the founded faces and use the function predict of our model,
        which give us it's prediction.
        Given the model it will set a text who give the category or the probabilities of each categories.
        Then it will print the image with a rectangle where the face is detected
        and the text with the necessary informations. """

        image = cv2.imread(img_path)
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
        net = cv2.dnn.readNetFromCaffe("architecture.txt", "weights.caffemodel")
        net.setInput(blob)
        detections = net.forward()
        (height, width) = image.shape[:2]
        for i in range(0, detections.shape[2]):

            # extract the confidence (i.e., probability) associated with the
            # prediction
            prediction = detections[0, 0, i, 2]

            # greater than the minimum confidence
            if prediction > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
                (x1, y1, x2, y2) = box.astype("int")

                if (x1 >= 0 and x2 >= 0 and x1 <= width and x2 <= width
                        and y1 >= 0 and y2 >= 0 and y1 <= height and y2 <= height):

                    pil_img = Image.open(img_path)
                    crop_img = Image.Image.crop(pil_img, (x1, y1, x2, y2))
                    crop_img.save("crop_img.png")
                    img = keras.preprocessing.image.load_img(
                        img_path,
                        target_size=(150, 150)
                    )
                    os.remove("crop_img.png")
                    img_array = tf.expand_dims(img, 0)  # Create batch axis
                    mask_predict = self.model.predict(img_array)[0]
                    result = ""
                    if mode == "categories":
                        if mask_predict > 0.5:
                            result = "no mask"
                        else:
                            result = "mask"
                    elif mode == "probabilities":
                        result = str(100 * (1 - mask_predict)) \
                                 + " % mask and " + str(100 * mask_predict) + " % no mask."

                    y = y1 - 10 if y1 - 10 > 10 else y1 + 10

                    cv2.rectangle(image, (x1, y1), (x2, y2),
                                  (0, 0, 255), 2)
                    cv2.putText(image, result, (x1, y),
                                cv2.LINE_AA, 0.35, (0, 0, 255), 2)

        cv2.imshow("Output", image)
        cv2.waitKey(0)
