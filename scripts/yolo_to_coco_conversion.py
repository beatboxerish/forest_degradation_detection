# source code taken from here: https://github.com/ultralytics/ultralytics/pull/7458/files

import glob
import json
import os

import numpy as np
from PIL import Image

from mhadei_restoration.utils.general_utils import open_yaml_file


# TODO: Clean this and all code relevant to getting labelme files from yolo
def get_categories(yaml_file):
    data = open_yaml_file(yaml_file)
    classes = data["names"]
    class_dict = dict()
    for i_idx, i_class in enumerate(classes):
        class_dict[i_class] = i_idx + 1
    return class_dict


# Function to convert YOLO annotations to COCO format
def yolo_to_coco(yolo_annotation, image_id, img_width, img_height, ann_id_start):
    annotations = []
    for ann_line in yolo_annotation.splitlines():
        cat_id = int(ann_line[0]) + 1
        parts = ann_line[1:].strip().split()
        xs, ys = [float(x) for x in parts[0::2]], [float(x) for x in parts[1::2]]
        xs, ys = [int(img_width*x) for x in xs], [int(img_height*y) for y in ys]
        new_parts = []
        for x, y in zip(xs, ys):
            new_parts.append(x)
            new_parts.append(y)

        # get bbox
        minx = np.inf
        maxx = 0
        for x in xs:
            if x<minx:
                minx = x
            if x>maxx:
                maxx = x
        miny = np.inf
        maxy = 0
        for y in ys:
            if x < miny:
                miny = y
            if y > maxy:
                maxy = y

        x_top_left = minx
        y_top_left = miny
        width = maxx-minx
        height = maxy-miny

        annotations.append(
            {
                "id": ann_id_start,
                "image_id": image_id,
                "category_id": cat_id,  # Assuming 'person' category
                "bbox": [x_top_left, y_top_left, width, height],
                "area": width * height,
                "iscrowd": 0,
                'segmentation':[new_parts]
            }
        )
        ann_id_start += 1

    return annotations, ann_id_start


# Configuration
data_yaml = '../data/Yolo-Three-DIs-Final-Train-Val/data.yaml'  # input data.yaml file from yolo dataset
yolo_labels_dir = "../data/Yolo-Three-DIs-Final-Train-Val/val/labels"  # Path containing your YOLO .txt files
output_json_path = "../data/Yolo-Three-DIs-Final-Train-Val-val.json"  # Output COCO format JSON file

# initialize COCO dataset structure
coco_dataset = {
    "info": {},
    "licenses": [],
    "images": [],
    "annotations": [],
    "categories": []
}

# form the current categories
cat_dict = get_categories(data_yaml)
coco_dataset["categories"] = []
for k, v in cat_dict.items():
    current_cat_dict = dict()
    current_cat_dict['id'] = v
    current_cat_dict['name'] = k
    current_cat_dict["supercategory"] = "common-objects"
    coco_dataset["categories"].append(current_cat_dict)


# Iterate over YOLO label files and convert annotations
annotation_id = 1  # Starting ID for COCO annotations
for idx, label_file in enumerate(glob.glob(os.path.join(yolo_labels_dir, "*.txt"))):
    image_id = idx + 1
    image_file = label_file.replace('txt', 'tif').replace('labels', "images")
    img_width, img_height = Image.open(image_file).size

    with open(label_file, "r") as file:
        yolo_annotation = file.read()

    coco_anns, annotation_id = yolo_to_coco(yolo_annotation, image_id, img_width, img_height, annotation_id)
    coco_dataset["annotations"].extend(coco_anns)

    coco_dataset["images"].append(
        {
            "id": image_id,
            "width": img_width,
            "height": img_height,
            "file_name": os.path.basename(image_file),  # Adjust image file extension
        }
    )

# Save the COCO dataset to a JSON file
with open(output_json_path, "w") as f:
    json.dump(coco_dataset, f, indent=4)

print(f"Converted annotations have been saved to {output_json_path}")
