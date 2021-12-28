# Facial Mask Detector Help

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
...

## Main window

### Left Side: List of images

#### Choose the image to annotate
#### Delete an image
#### Rename an image


### Right Side: Annotate Image

#### Create an annotation

#### Modify an annotation





