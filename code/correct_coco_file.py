from glob import glob
from code.utils.coco_utils import read_coco_file, save_coco_file


annotation_folder = ("/Users/ishannangia/github_repos/Mhadei_Restoration/data/"
                     "original-data/annotation_files_coco-images_orthos/")

annotation_files = glob(f"{annotation_folder}/*")
current_annotation_file_address = annotation_files[0]

# loading the coco file. Only loads 1 file for now.
coco_file = read_coco_file(current_annotation_file_address)

"""
Had to edit the labelme based coco file created manually. 
The code for labelme2coco seems to work but creates an error.
Not sure if this a problem or not.
"""
coco_file["images"][0]["file_name"] = coco_file["images"][0]["file_name"].split("/")[-1]
save_coco_file(coco_file, current_annotation_file_address)
