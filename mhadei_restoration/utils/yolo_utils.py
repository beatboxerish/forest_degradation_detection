import os
import random
import shutil
from pathlib import Path
from ultralytics import YOLO

from mhadei_restoration.utils.general_utils import copy_images, get_names_from_names_with_extension
from mhadei_restoration.utils.coco_utils import save_coco_file
from mhadei_restoration.JSON2YOLO.general_json2yolo import convert_coco_json


def get_train_test_val_image_names(coco_file, preprocess_dict):
    """
    Divides the images in supplied coco file into train, test, and val based
    on preprocess_dict
    :param coco_file:
    :param preprocess_dict:
    :return:
    """
    # TODO: create check to ensure train and val sizes are defined in preprocess dict
    train_images = val_images = test_images = []
    images = [image['file_name'] for image in coco_file["images"]]

    train_size = int(preprocess_dict['train_size'] * len(images))
    if preprocess_dict['test_size']:
        val_size = int(preprocess_dict['val_size'] * len(images))
        test_size = len(images) - train_size - val_size
    else:
        val_size = len(images) - train_size
        test_size = 0

    current_images = images.copy()
    train_images = random.sample(current_images, train_size)

    current_images = list(set(current_images) - set(train_images))
    val_images = random.sample(current_images, val_size)

    current_images = list(set(current_images) - set(val_images))
    if test_size:
        test_images = random.sample(current_images, test_size)
    return train_images, val_images, test_images


def copy_and_move_images(image_source_folder, train_image_names, val_image_names, test_image_names,
                         target_parent_folder, data_yaml):
    if len(train_image_names):
        train_image_sources = [os.path.join(image_source_folder, train_image) for train_image in train_image_names]
        train_image_targets = get_train_test_val_image_locations(data_yaml, train_image_names, 'train',
                                                                 target_parent_folder)
        copy_images(train_image_sources, train_image_targets)

    if len(val_image_names):
        val_image_sources = [os.path.join(image_source_folder, val_image) for val_image in val_image_names]
        val_image_targets = get_train_test_val_image_locations(data_yaml, val_image_names, 'val',
                                                               target_parent_folder)
        copy_images(val_image_sources, val_image_targets)
    if len(test_image_names):
        test_image_sources = [os.path.join(image_source_folder, test_image) for test_image in test_image_names]
        test_image_targets = get_train_test_val_image_locations(data_yaml, test_image_names, 'test',
                                                                target_parent_folder)
        copy_images(test_image_sources, test_image_targets)
    return None


def create_and_move_annotations(coco_file, target_parent_folder,
                                train_images, val_images, test_images):

    temp_folder = "./temp_coco_dir"
    Path(temp_folder).mkdir(parents=True, exist_ok=True)
    save_coco_file(coco_file, os.path.join(temp_folder, 'temp_coco.json'))
    convert_coco_json(json_dir=temp_folder, use_segments=True, cls91to80=False)
    shutil.rmtree(temp_folder)

    train_names = get_names_from_names_with_extension(train_images)
    val_names = get_names_from_names_with_extension(val_images)
    test_names = get_names_from_names_with_extension(test_images)

    source_dir = os.path.join("new_dir/labels", os.listdir('new_dir/labels')[0])
    move_label_type(source_dir, train_names, "train", target_parent_folder)
    move_label_type(source_dir, val_names, "val", target_parent_folder)
    move_label_type(source_dir, test_names, "test", target_parent_folder)
    return None


def move_label_type(source_dir, image_names, image_type, target_parent_folder):
    for image_name in image_names:
        source_file_path = os.path.join(source_dir, image_name + '.txt')
        destination_file_path = os.path.join(target_parent_folder,
                                             image_type,
                                             "labels",
                                             source_file_path.split('/')[-1])
        if os.path.isfile(destination_file_path):
            os.remove(destination_file_path)
        shutil.move(source_file_path, destination_file_path)
    return None


def get_train_test_val_image_locations(data_yaml, image_names, type_of_image, target_parent_folder):
    image_locations = [os.path.join(target_parent_folder, data_yaml[type_of_image], "images", image_name) for image_name
                       in image_names]
    return image_locations


def get_new_data_yaml(coco_file):
    data_yaml = dict()
    data_yaml['names'] = [cat['name'] for cat in coco_file['categories']]
    data_yaml['nc'] = len(data_yaml['names'])
    return data_yaml


def create_new_directory_structure(data_yaml, parent_folder, train=True, val=True, test=True):
    train_path = os.path.join(parent_folder, "train")
    val_path = os.path.join(parent_folder, "val")
    test_path = os.path.join(parent_folder, "test")

    # creation of directories
    Path(parent_folder).mkdir(parents=True, exist_ok=True)
    if train:
        Path(train_path).mkdir(parents=True, exist_ok=True)
        create_labels_images(train_path)
        data_yaml['train'] = train_path

    if val:
        Path(val_path).mkdir(parents=True, exist_ok=True)
        create_labels_images(val_path)
        data_yaml['val'] = val_path

    if test:
        Path(test_path).mkdir(parents=True, exist_ok=True)
        create_labels_images(test_path)
        data_yaml['test'] = test_path

    return None


def create_labels_images(parent):
    Path(os.path.join(parent, 'labels')).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(parent, 'images')).mkdir(parents=True, exist_ok=True)
    return None


def load_yolo(model_address):
    model = YOLO(model_address)
    return model

