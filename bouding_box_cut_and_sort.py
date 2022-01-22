import json
import os
from PIL import Image


def cut_save_image_train(annot: str, img_path: str, save_path: str, left: int, top: int, right: int, bottom: int):
    image = Image.open(img_path)
    cut_image = image.crop((left, top, right, bottom))
    split_path = img_path.split('/')
    if len(split_path) == 1:
        split_path = img_path.split('\\')
    name = split_path[-1].split(".")[0] + "-bb-" \
           + str(left) + "x" \
           + str(top) + "-" \
           + str(abs(right - left)) + "-" \
           + str(abs(bottom - top)) + ".png"
    if not os.path.exists(save_path + "\\train"):
        os.mkdir(save_path + "\\train")
    if not os.path.exists(save_path + "\\train\\" + annot):
        os.mkdir(save_path + "\\train\\" + annot)
    print(name)
    cut_image.save(save_path + "\\train\\" + annot + "\\" + name)


def save_image_test(annot: str, img_path: str, save_path: str):
    if not os.path.exists(save_path + "\\test"):
        os.mkdir(save_path + "\\test")
    if not os.path.exists(save_path + "\\test\\" + annot):
        os.mkdir(save_path + "\\test\\" + annot)
    split_path = img_path.split('/')
    if len(split_path) == 1:
        split_path = img_path.split('\\')
    name = split_path[-1]
    image = Image.open(img_path)
    image.save(save_path + "\\test\\" + annot + "\\" + name)


def treatment_annotate_images(json_path: str, save_path: str, type: str):
    f = open(json_path)
    json_data = json.load(f)
    if len(json_data) != 0:
        for image in json_data:
            if os.path.exists(json_data[image]["path"]):
                path_img = json_data[image]["path"]
                if len(json_data[image]["annotations"]) != 0:
                    for i in range(len(json_data[image]["annotations"])):
                        annot = json_data[image]["annotations"][i]["title"]
                        top = min(json_data[image]["annotations"][i]["box"]["top_left"]["ord"],
                                  json_data[image]["annotations"][i]["box"]["bottom_right"]["ord"])
                        right = max(json_data[image]["annotations"][i]["box"]["bottom_right"]["abs"],
                                    json_data[image]["annotations"][i]["box"]["top_left"]["abs"])
                        bottom = max(json_data[image]["annotations"][i]["box"]["bottom_right"]["ord"],
                                     json_data[image]["annotations"][i]["box"]["top_left"]["ord"])
                        left = min(json_data[image]["annotations"][i]["box"]["top_left"]["abs"],
                                   json_data[image]["annotations"][i]["box"]["bottom_right"]["abs"])
                        if type == "train":
                            cut_save_image_train(annot, path_img, save_path, left, top, right, bottom)
                        elif type == "test":
                            save_image_test(annot, path_img, save_path)


if __name__ == '__main__':
    define_json_path = "C:\\Users\\julie\\Documents\\M1_Project\\NNL_Mask\\Project\\Mask_Train\\annotations.json"
    define_save_path = "Mask_Recognition/dataset"
    type_save = "train"  # ou train

    treatment_annotate_images(define_json_path, define_save_path, type_save)
