import os
from src.utils.coco_utils import read_coco_file, save_coco_file


parent_folder = ("/Users/ishannangia/github_repos/Mhadei_Restoration/data/"
                 "original-data/annotation_files_coco-images_orthos/")
file_name = "iteration-II.json"
current_annotation_file_address = os.path.join(parent_folder, file_name)

# loading the coco file. Only loads 1 file for now.
coco_file = read_coco_file(current_annotation_file_address)

"""
Had to edit the labelme based coco file created manually. 
The code for labelme2coco works but takes the ImagePath parameter from the labelme json as the file_name.
Sometimes the labelme file is saving weird names in the ImagePath. Like full paths. Will have to check when
and why. If we are using '/' in file names, the below will create a huge problem!
There are some \\ for some reason too in some of the ImagePaths. Will be correcting them too
"""
for idx, image in enumerate(coco_file['images']):
    coco_file["images"][idx]["file_name"] = image["file_name"].split("/")[-1]
    if "\\" in image["file_name"]:
        coco_file["images"][idx]["file_name"] = image["file_name"].split("\\")[-1]
save_coco_file(coco_file, current_annotation_file_address)
