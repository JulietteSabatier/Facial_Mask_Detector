import PIL.Image
import numpy as np
import tensorflow as tf
from tensorflow import keras, resource
import matplotlib
import graphviz
import pydot
import cv2
import os
from matplotlib import pyplot as plt
from mtcnn.mtcnn import MTCNN
from PIL import Image


# Function to modify for the test
def define_model(input_shape, num_classes):
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

    my_model.add(keras.layers.Conv2D(filters=32, kernel_size=(5, 5), padding="same", activation="relu"))
    my_model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))

    my_model.add(keras.layers.Conv2D(filters=64, kernel_size=(3, 3), padding="same", activation="relu"))
    my_model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))

    my_model.add(keras.layers.Conv2D(filters=128, kernel_size=(3, 3), padding="same", activation="relu"))
    my_model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))
    my_model.add(keras.layers.Dropout(0.25))

    my_model.add(keras.layers.Flatten())
    my_model.add(keras.layers.Dense(num_classes))
    my_model.add(keras.layers.Activation("sigmoid"))

    return my_model


def create_model(path_train: str, path_valid: str, path_save):
    image_size = (150, 150)
    batch_size = 64

    # Generate dataset
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        directory=path_train,
        labels='inferred',
        label_mode='categorical',
        validation_split=0.2,
        subset='training',
        seed=1337,
        image_size=image_size,
        batch_size=batch_size
    )
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        directory=path_valid,
        labels='inferred',
        label_mode='categorical',
        validation_split=0.2,
        subset='validation',
        seed=1337,
        image_size=image_size,
        batch_size=batch_size
    )
    model = define_model(input_shape=image_size, num_classes=2)
    # plot_model(model, show_shapes=True)

    epochs = 30

    model.compile(
        optimizer=keras.optimizers.Adam(1e-3),
        loss='binary_crossentropy',
        metrics=["accuracy"],
    )
    model.fit(
        train_ds, epochs=epochs, validation_data=val_ds
    )

    model.save(path_save, save_format='h5')


def test_image(img_path: str, model_path: str):
    # Run with new
    image = cv2.imread("C:/Users/julie/Documents/M1_Project/NNL_Mask/Images/Images from 0 to 99/maksssksksss11.png")
    blob  = cv2.dnn.blobFromImage(cv2.resize(image,(300,300)),1.0,(300,300), (104.0,177.0,123.0))
    net = cv2.dnn.readNetFromCaffe("../architecture.txt", "../weights.caffemodel")
    net.setInput(blob)
    detections = net.forward()
    print(detections)
    (height, width) = image.shape[:2]
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the
        # prediction
        confidence = detections[0, 0, i, 2]

        # greater than the minimum confidence
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
            (x1, y1, x2, y2) = box.astype("int")

            # draw the bounding box of the face along with the associated
            # probability
            text = "{:.2f}%".format(confidence * 100) + " ( " + str(y2 - y1) + ", " + str(x2 - x1) + " )"
            y = y1 - 10 if y1 - 10 > 10 else y1 + 10
            cv2.rectangle(image, (x1, y1), (x2, y2),
                          (0, 0, 255), 2)
            cv2.putText(image, text, (x1, y),
                        cv2.LINE_AA, 0.45, (0, 0, 255), 2)

    # show the output image
    cv2.imshow("Output", image)
    cv2.waitKey(0)

    # Ne supporte pas le chemin avec \\ il faut /
    #image = plt.imread("C:/Users/julie/Documents/M1_Project/NNL_Mask/Images/Images from 0 to 99/maksssksksss23.png")

    #img1 = Image.open("C:/Users/julie/Documents/M1_Project/NNL_Mask/Images/Images from 0 to 99/maksssksksss23.png")


    #pixels = np.asarray(img1)

    #detector = MTCNN()
    #faces = detector.detect_faces(np.asarray(image))
    #for face in faces:
    #    print(face)


    #image_size = (150, 150)

    # img = keras.preprocessing.image.load_img(
    #    img_path,
    #    target_size=image_size
    # )
    # img_array = keras.preprocessing.image.img_to_array(img)
    # img_array = tf.expand_dims(img_array, 0)  # Create batch axis

    # model = keras.models.load_model(model_path)

    # predictions = model.predict(img_array)
    # return predictions[0]


def test_multiple_image(path_dataset: str, path_model: str):
    list_category = os.listdir(path_dataset)

    TP = 0
    TN = 0
    FP = 0
    FN = 0
    total = 0
    for category in list_category:
        for image in os.listdir(path_dataset + "\\" + category):
            print(image)
            total += 1
            score = test_image(path_dataset + "\\" + category + "\\" + image, path_model)[0]
            if category == "mask":
                if score <= 0.5:
                    TP += 1
                    print("mask, find mask")
                else:
                    FP += 1
                    print("mask, find no mask")
            if category == "no_mask":
                if score > 0.5:
                    TN += 1
                    print("no mask, find no mask")
                else:
                    FN += 1
                    print("no mask, find mask")
    accuracy = (TP + TN) / total
    recall = TP / (TP + TN)
    precision = TP / (TP + FP)
    print("TP:" + str(TP) + " // TN:" + str(TN) + " // FP:" + str(FP) + " // FN:" + str(FN) + "// Total: " + str(total))
    print("Accuracy: " + str(accuracy) + " // Recall: " + str(recall) + " // Precision: " + str(precision))


def predict(filename: str, mode: str, model_path: str):
    score = test_image(filename, model_path)[0]
    if mode == "categories":
        if score > 0.5:
            print("no mask")
        else:
            print("mask")
    elif mode == "probabilities":
        print("This image is %.2f percent mask and %.2f percent no mask."
              % (100 * (1 - score), 100 * score))


if __name__ == '__main__':
    # Creer le model
    # create_model("C:\\Users\\julie\\Documents\\M1_Project\\test_nnl\\Train",
    #             "C:\\Users\\julie\\Documents\\M1_Project\\test_nnl\\Validation",
    #             r"./mask_model")

    # Prédire une image
    # predict("C:\\Users\\julie\\Documents\\M1_Project\\NNL_Mask\\Images\\Images from 0 to 99\\maksssksksss4.png",
    #        "probabilities",
    #        "C:\\Users\\julie\\Documents\\M1_Project\\NNL_Mask\\Mask_Recognition\\mask_model")

    test_image("C:\\Users\\julie\\Documents\\M1_Project\\NNL_Mask\\Images\\Images from 0 to 99\\maksssksksss4.png",
               "C:\\Users\\julie\\Documents\\M1_Project\\NNL_Mask\\Mask_Recognition\\mask_model")

    # !!!! Broken ne sais pas pourquoi, ne pas utiliser
    # Prédire plusieurs images, mesures
    # test_multiple_image("C:\\Users\\julie\\Documents\\M1_Project\\test_nnl\\Validation",
    #                    "C:\\Users\\julie\\Documents\\M1_Project\\NNL_Mask\\Mask_Recognition\\mask_model")
