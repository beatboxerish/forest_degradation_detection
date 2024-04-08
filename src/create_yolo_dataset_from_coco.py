from glob import glob
import shutil

from src.utils.general_utils import save_yaml_file
from src.utils.coco_utils import read_coco_file, preprocess_labels
from src.utils.yolo_utils import (get_new_data_yaml, create_new_directory_structure,
                                  get_train_test_val_image_names, copy_and_move_images,
                                  create_and_move_annotations)


annotation_folder = ("/Users/ishannangia/github_repos/Mhadei_Restoration/data/"
                     "original-data/annotation_files_coco-images_orthos/")
image_source_folder = ("/Users/ishannangia/github_repos/Mhadei_Restoration/data/"
                       "original-data/images_orthos/")
target_parent_folder = '/Users/ishannangia/github_repos/Mhadei_Restoration/data/Yolo-2'

label_dict = {
    "Distorted Image": "Distorted Image",
    'Canopy Gap: Shaded': 'Canopy Gap',
    'Canopy Gap: Vegetated': 'Canopy Gap',
    "Canopy Gap: Bare Land": 'Canopy Gap',
    'Canopy Gap: Unknown': "Canopy Gap"
}

preprocess_dict = {
    "train_size": 20,
    "val_size": 5,
    "test_size": 3,
    "labels": label_dict,
}

# grabbing all image and annotation file addresses
image_source_addresses = glob(f"{image_source_folder}/*")
annotation_files = glob(f"{annotation_folder}/*")

# loading the coco file. Only loads 1 file for now.
coco_file = read_coco_file(annotation_files[0])

# preprocessing labels of coco files and take the first file
coco_file = preprocess_labels([coco_file], preprocess_dict)[0]

# data yaml creation. Needed for training YOLO
data_yaml = get_new_data_yaml(coco_file)

# creating new directory structure for dataset
create_new_directory_structure(data_yaml, target_parent_folder, train=True, val=True, test=True)

# copy and move images from source to target
train_image_names, val_image_names, test_image_names = get_train_test_val_image_names(coco_file, preprocess_dict)
copy_and_move_images(image_source_folder, train_image_names, val_image_names, test_image_names,
                     target_parent_folder, data_yaml)

# transfer annotations
create_and_move_annotations(coco_file, target_parent_folder,
                            train_image_names, val_image_names, test_image_names)
shutil.rmtree("new_dir")

# save new data yaml file
save_yaml_address = f'{target_parent_folder}/data.yaml'
save_yaml_file(data_yaml, save_yaml_address)
