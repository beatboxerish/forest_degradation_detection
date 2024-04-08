import shutil
import yaml


def convert_to_single_list(list_of_lists):
    new_list_of_lists = []
    for single_list_to_convert in list_of_lists:
        new_list = []
        for item in single_list_to_convert:
            new_list.extend(item)
        new_list_of_lists.append(new_list)
    return new_list_of_lists


def get_names_from_names_with_extension(full_names):
    names = [i.split(".")[0] for i in full_names]
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
