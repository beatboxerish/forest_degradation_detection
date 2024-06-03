from glob import glob
import shutil

from mhadei_restoration.utils.general_utils import save_yaml_file
from mhadei_restoration.utils.coco_utils import read_coco_file, preprocess_labels
from mhadei_restoration.utils.yolo_utils import (get_new_data_yaml, create_new_directory_structure,
                                                 copy_and_move_images, create_and_move_annotations,
                                                 get_cross_val_image_names)


annotation_file = ("/Users/ishannangia/github_repos/Mhadei_Restoration/data/"
                     "original-data/annotation_files_coco-images_orthos/final_iteration.json")
image_source_folder = ("/Users/ishannangia/github_repos/Mhadei_Restoration/data/"
                       "original-data/images_orthos/")
target_parent_folder = '/Users/ishannangia/github_repos/Mhadei_Restoration/data/Yolo-Four-DIs-Final-Iteration'


# TODO: allow for stratified sampling of images
label_dict = {
    "Distorted Image": "Distorted Image",
    'Canopy Gap: Shaded': 'Canopy Gap: Shaded',
    'Canopy Gap: Vegetated': 'Canopy Gap: Vegetated',
    "Canopy Gap: Bare Land": 'Canopy Gap: Bare Land',
    'Plantation': 'Plantation',
    # 'Potential Invasive': 'Potential Invasive',
    # 'Potential Creeper': 'Potential Creeper',
    # 'Cane': 'Cane'
}

preprocess_dict = {
    "train_size": 0.7,
    "val_size": 0.3,
    "test_size": 0,
    "labels": label_dict,
    'k': 3
}

# grabbing all images
image_source_addresses = glob(f"{image_source_folder}/*")

# loading the coco file
coco_file = read_coco_file(annotation_file)

# preprocessing labels of coco files and take the first file
coco_file = preprocess_labels([coco_file], preprocess_dict)[0]

# using cross validation to get image names
train_image_dict, val_image_dict, test_image_dict = get_cross_val_image_names(coco_file, preprocess_dict)

for key in train_image_dict.keys():
    current_parent_folder = target_parent_folder + "-" + str(key)
    train_image_names = train_image_dict[key]
    val_image_names = val_image_dict[key]
    test_image_names = test_image_dict[key]

    # data yaml creation. Needed for training YOLO
    data_yaml = get_new_data_yaml(coco_file)

    # creating new directory structure for dataset
    create_new_directory_structure(data_yaml, current_parent_folder, train=True, val=True, test=True)

    # copy and move images from source to target
    copy_and_move_images(image_source_folder, train_image_names, val_image_names, test_image_names,
                         current_parent_folder, data_yaml)

    # transfer annotations
    create_and_move_annotations(coco_file, current_parent_folder,
                                train_image_names, val_image_names, test_image_names)
    shutil.rmtree("new_dir")

    # save new data yaml file
    save_yaml_address = f'{current_parent_folder}/data.yaml'
    save_yaml_file(data_yaml, save_yaml_address)
