import shutil
import yaml
from PIL import Image
import cv2
import os
from glob import glob

# TODO: read global variables from config file
POSSIBLE_IMAGE_EXTENSIONS = ["tif", "TIF", "jpg", "JPG", "png", "PNG"]


def convert_to_single_list(list_of_lists):
    new_list_of_lists = []
    for single_list_to_convert in list_of_lists:
        new_list = []
        for item in single_list_to_convert:
            new_list.extend(item)
        new_list_of_lists.append(new_list)
    return new_list_of_lists


def get_names_from_names_with_extension(full_names):
    names = []
    if len(full_names):
        names = [i.split(".")[:-1] for i in full_names]
        names = [".".join(i) for i in names]
    return names


def copy_images(source_images, target_images):
    for idx, image in enumerate(source_images):
        target_image = target_images[idx]
        shutil.copyfile(image, target_image)
    return None


def open_yaml_file(original_data_yaml_address):
    with open(original_data_yaml_address, 'r') as infile:
        yaml_file = yaml.load(infile, Loader=yaml.SafeLoader)
    return yaml_file


def save_yaml_file(yaml_file, save_yaml_address):
    with open(save_yaml_address, 'w') as outfile:
        yaml.dump(yaml_file, outfile, default_flow_style=False)


def load_image_with_pil(original_image_path):
    img = Image.open(original_image_path)
    return img


def load_image_with_cv(original_image_path):
    image_bgr = cv2.imread(original_image_path)
    original_image_size = image_bgr.shape[1], image_bgr.shape[0]

    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    return image_bgr, image_rgb, original_image_size


def get_image_paths_from_folder(folder):
    all_images = []
    for extension in POSSIBLE_IMAGE_EXTENSIONS:
        current_extension_images = glob(os.path.join(folder, f"*.{extension}"))
        all_images.extend(current_extension_images)
    return all_images


def get_images_from_paths(paths, cv=True):
    images = []
    for path in paths:
        if not cv:
            img = load_image_with_pil(path)
        else:
            image_bgr, img, original_image_size = load_image_with_cv(path)
        images.append(img)
    return images
