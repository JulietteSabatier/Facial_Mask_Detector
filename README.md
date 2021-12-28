# Facial Mask Detector Help

## Before running code:
Please run the following command:
- python -m pip install -r requirement.txt

## Create a project
### Description
Permit to save all the information in one directory. 
Use mainly to save the image and prevent the fact that the user may want to delete the image in his initial directory.

A project is a directory containing 2 files **annotations.json**, **categories.json** and a directory named **Images**, 
he is contained in the directory **Project**.

### Presentation in the application
At the launch of the program a popup appears it contains one button and a list of project names.

You can create a project by pressing the button **Create Project**. Another popup appears to aks how you would name
the project and by clicking on **OK**.

You can open an existing project with a double click on the name of the project you want to open.

During the annotation process you can save your project with the menu bar **Project > Save**.
You can also close your project, in order to open another one. When you close the project he is automatically saved.

## MenuBar

### Images
In order to load one or multiple images have to use the menu bar **Images > Load**.

You can also choose to save all the images of the application wherever you want with the menu bar **Images > Save**.

### Categories
With the menubar **Cateogries > Import** you can import a list of categories written on a json or a csv file.
The csv delimiter should be a **;**.
The json file should be like **{"categories":  ["mask", "head", "hair", "kid"]}**.

With the menubar **Categories > Show All**, a popup will appear, containing a list of all the categories.
With the right click on a category a menu appears and permit you to delete or rename the chosen category.

With the menubar **Categories > Create New**, a popup will appear, by entering the name you want it will create the 
category with this name.

With the menubar **Categories > Save**, you can choose to save the categories in a csv file wherever you want.

### Annotations

With the menubar **Annotations > Save**, you could choose to save all the annotations in a json file wherever you want.

With the menubar **Annotations > Load**, you can load annotations from a json file.
The json should be like:
```json 
{"maksssksksss200": {
    "path": "Project/Test/Images/maksssksksss200.png", 
    "annotations": [{
        "title": "kid", 
        "box": {
            "top_left": {"abs": 88.0597014925373, "ord": 75.3731343283582}, 
            "bottom_right": {"abs": 197.0149253731343, "ord": 195.52238805970148}}}]
    },
 "maksssksksss202": {
    "path": "Project/Test/Images/maksssksksss202.png", 
    "annotations": []
    }
}
```

## Main window

### Left Side: List of images

#### Choose the image to annotate
In order to choose the image you want to annotate or modify the annotations, 
you have to double-click on the name of the image.

#### Delete an image
In order to delete an image you have to make a right-click on the name of the image and choose the menu **Delete**.

#### Rename an image
In order to rename an image you have to make a right-click on the name of the image and choose the menu **Rename**

### Right Side: Annotate Image

#### Create an annotation
In order to create an annotation you have to draw a rectangle on the image, by pressing the left-click,
move the mouse and release the click wherever you want. 
After this process, a popup will appear with the coordinate of the annotation and a comboBox
to choose the category of the annotation.
This popup contain a button **Save** which save the chosen category for the annotation and a button **Delete**
which delete the annotation.


#### Modify an annotation
A **double click** inside an annotation permit to fire a popup (the same from the create an annotation) in order to change
the category or delete the annotation.





