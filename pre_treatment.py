import json
import os.path

from PIL import Image


def cut_save_image(img_path: str, save_path: str, left: int, top: int, right: int, bottom: int):
    image = Image.open(img_path)
    cut_image = image.crop((left, top, right, bottom))
    name = img_path.split("/")[-1].split(".")[0] + "-bb-" \
           + str(left) + "x" \
           + str(top) + "-" \
           + str(abs(right - left)) + "-" \
           + str(abs(bottom - top)) + ".png"
    split_path = save_path.split("\\")
    path = ""
    for i in range(len(split_path)-1):
        path += split_path[i]+"\\"
    cut_image.save(path + "\\" + name)


def read_json_and_cut(json_path: str, save_path: str):
    f = open(json_path)
    json_data = json.load(f)
    if len(json_data) != 0:
        for image in json_data:
            if os.path.exists(json_data[image]["path"]):
                path_img = json_data[image]["path"]
                img = Image.open(path_img)
                if len(json_data[image]["annotations"]) != 0:
                    for i in range(len(json_data[image]["annotations"])):
                        top = min(json_data[image]["annotations"][i]["box"]["top_left"]["ord"],
                                  json_data[image]["annotations"][i]["box"]["bottom_right"]["ord"])
                        right = max(json_data[image]["annotations"][i]["box"]["bottom_right"]["abs"],
                                    json_data[image]["annotations"][i]["box"]["top_left"]["abs"])
                        bottom = max(json_data[image]["annotations"][i]["box"]["bottom_right"]["ord"],
                                     json_data[image]["annotations"][i]["box"]["top_left"]["ord"])
                        left = min(json_data[image]["annotations"][i]["box"]["top_left"]["abs"],
                                   json_data[image]["annotations"][i]["box"]["bottom_right"]["abs"])
                        cut_save_image(path_img, save_path + "\\" + image + ".png", left, top, right, bottom)


if __name__ == '__main__':
    read_json_and_cut(r"C:\Users\julie\Documents\M1_Project\NNL_Mask\Project\test\annotations.json",
                      r"C:\Users\julie\Documents\M1_Project\test")
