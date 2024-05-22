from PIL import Image
import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import torch
import numpy as np
import os
import shutil
from pathlib import Path
import supervision as sv
import torch

from src.utils.general_utils import (load_image_with_pil, load_image_with_cv,
                                     get_names_from_names_with_extension, get_image_paths_from_folder,
                                     get_images_from_paths)
from src.utils.general_utils import open_yaml_file, save_yaml_file
from src.utils.yolo_utils import create_labels_images

ALL_COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255), (255, 0, 255),
    (0, 255, 0), (0, 255, 255), (255, 255, 0)
]


def get_bboxes_masks_on_image(original_image_path, save_image_path, model):
    results = get_results_on_image(original_image_path, model)[0]

    current_bboxes_n = results.boxes.xyxyn
    current_classes = results.boxes.cls

    # dictionary of ID to class name
    current_name_map = results.names

    current_masks = results.masks
    if current_masks is None:
        print('No masks found in results file...')
        return None
    current_masks_xy = [i.xy[0] for i in current_masks]

    class_to_color_map = get_class_to_color_map(current_name_map)
    color_class_legend = build_color_class_legend(current_name_map, class_to_color_map)
    image_with_bboxes = get_bboxes_on_image(original_image_path, current_bboxes_n,
                                            current_classes, class_to_color_map)
    image_with_masks = get_masks_on_image(original_image_path, current_masks_xy,
                                          current_classes, class_to_color_map)
    image_comparison_plot = display_images_comparison(original_image_path, image_with_bboxes,
                                                      image_with_masks)
    image_comparison_plot.savefig(save_image_path)
    color_class_legend.savefig(
        get_names_from_names_with_extension([save_image_path])[0] + "_legend.jpg"
    )
    return None


def build_color_class_legend(current_name_map, class_to_color_map):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    legend_elements = []
    for idx in range(len(current_name_map.keys())):
        class_name = current_name_map[idx]
        class_color = class_to_color_map[idx]
        class_color = [i/255 for i in class_color]
        patch = Patch(facecolor=class_color, label=class_name, edgecolor='black')
        legend_elements.append(patch)
    ax.legend(handles=legend_elements, loc='center')
    return fig


def get_results_on_image(image_path, model, show_labels=True, conf=0.25, iou=0.3, imgsz=640):
    results = model.predict(
        image_path, save=False, plots=False,
        line_width=3, show_conf=False, show_labels=show_labels,
        conf=conf, iou=iou, imgsz=imgsz
    )
    return results


def get_bboxes_on_image(original_image_path, bboxes, detected_classes, class_to_color_map):
    _, image_rgb, __ = load_image_with_cv(original_image_path)
    image_with_bboxes = draw_bboxes_xyxyn(bboxes, image_rgb, class_to_color_map, detected_classes)
    image_with_bboxes = Image.fromarray(image_with_bboxes)
    return image_with_bboxes


def draw_bboxes_xyxyn(bboxes, img, class_to_color_map, all_classes):
    drawn_img = img.copy()
    for box_idx, box in enumerate(bboxes):
        x, y, x1, y1 = box
        x, x1 = x*img.shape[1], x1*img.shape[1]
        y, y1 = y*img.shape[0], y1*img.shape[0]
        current_class = all_classes[box_idx].item()
        current_color = class_to_color_map[current_class]
        cv2.rectangle(drawn_img, (int(x), int(y)), (int(x1), int(y1)), current_color, 10)
    return drawn_img


def get_masks_on_image(original_image_path, masks, current_classes, class_to_color_map):
    _, image_rgb, __ = load_image_with_cv(original_image_path)
    image_with_masks = draw_masks(masks, image_rgb, class_to_color_map, current_classes)
    image_with_masks = Image.fromarray(image_with_masks)
    return image_with_masks


def draw_masks(masks, image_rgb, class_to_color_map, current_classes):
    image_rgb = image_rgb.copy()
    for class_idx, current_class in enumerate(current_classes):
        current_class = int(current_class.item())
        current_mask = masks[class_idx].astype(int)
        image_rgb = cv2.drawContours(image_rgb, [current_mask],
                                     0, class_to_color_map[current_class], 10)
    return image_rgb


def get_class_to_color_map(id_to_class_name_map):
    total_classes = len(id_to_class_name_map.keys())
    current_colors = ALL_COLORS[:total_classes]
    class_to_color_map = {i: j for i, j in enumerate(current_colors)}
    return class_to_color_map


def display_images_comparison(original_image, image_with_bboxes,
                              image_with_masks):
    if type(original_image) is str:
        original_image = load_image_with_pil(original_image)
    fig, ax = plt.subplots(1, 3, figsize=(15, 6))
    ax[0].imshow(original_image)
    ax[1].imshow(image_with_bboxes)
    ax[2].imshow(image_with_masks)
    return fig


def get_comparison_image_with_original_labels(
        original_image_path, original_label_path,
        save_image_path, model, conf=0.25, iou=0.3,
        imgsz=640):
    # predicted information
    results = get_results_on_image(original_image_path, model, conf=conf,
                                   iou=iou, imgsz=imgsz)[0]

    # dictionary of ID to class name
    current_name_map = results.names
    class_to_color_map = get_class_to_color_map(current_name_map)
    color_class_legend = build_color_class_legend(current_name_map, class_to_color_map)

    current_classes = results.boxes.cls
    current_masks = results.masks
    current_masks_xy = [i.xy[0] for i in current_masks]

    # true information
    true_classes, true_seg_points = get_classes_segmentations_from_label_file(original_label_path)
    true_classes = torch.tensor(true_classes)
    height, width = results[0].orig_img.shape[0], results[0].orig_img.shape[1]
    true_seg_points = [np.array([[width*i[0], height*i[1]] for i in individual_seg_points])
                       for individual_seg_points in true_seg_points]

    # generating masks and plots
    image_with_predicted_masks = get_masks_on_image(original_image_path, current_masks_xy,
                                                    current_classes, class_to_color_map)
    image_with_true_masks = get_masks_on_image(original_image_path, true_seg_points,
                                               true_classes, class_to_color_map)
    image_comparison_plot = display_images_comparison(original_image_path, image_with_true_masks,
                                                      image_with_predicted_masks)

    image_comparison_plot.savefig(save_image_path)
    color_class_legend.savefig(
        get_names_from_names_with_extension([save_image_path])[0] + "_legend.jpg"
    )

    return image_comparison_plot


def get_classes_segmentations_from_label_file(labels_for_image):
    with open(labels_for_image, "r") as f:
        labels = f.read().strip()
    line_list = labels.split("\n")
    classes = []
    all_seg_points = []
    for _, line in enumerate(line_list):
        seg_points = []
        individual_numbers = [float(i) for i in line.split(" ")]
        classes.append(individual_numbers[0])
        individual_numbers = individual_numbers[1:]
        for idx in range(0, len(individual_numbers), 2):
            seg_points.append([individual_numbers[idx], individual_numbers[idx+1]])
        all_seg_points.append(np.array(seg_points))

    return classes, all_seg_points


def get_results_of_image_with_labels(model,
                                     img_address,
                                     label_address,
                                     original_data_yaml_address,
                                     prediction_save_path):
    # create val yaml
    val_data_yaml, val_data_yaml_address, val_parent_folder = (
        create_yaml_for_val(original_data_yaml_address)
    )
    # create dirs
    val_data_yaml = create_val_dirs(val_data_yaml, val_data_yaml_address,
                                    val_parent_folder)
    # move image and labels
    shutil.copyfile(img_address, os.path.join(val_data_yaml["val"],
                                              'images',
                                              img_address.split('/')[-1]))
    shutil.copyfile(label_address, os.path.join(val_data_yaml["val"],
                                                'labels',
                                                label_address.split('/')[-1]))

    # get results
    results = model.val(data=val_data_yaml_address,
                        save_json=True)
    shutil.copyfile(
        os.path.join(results.save_dir, 'predictions.json'),
        os.path.join(prediction_save_path, 'predictions.json')
    )
    # remove val dir and val only file
    shutil.rmtree(val_data_yaml['val'])
    os.remove(val_data_yaml_address)
    # TODO: Change below
    shutil.rmtree(results.save_dir)
    return results


def create_yaml_for_val(original_data_yaml_address):
    yaml_file = open_yaml_file(original_data_yaml_address)
    del yaml_file['test'], yaml_file['train']
    val_yaml_address = get_val_yaml_address(original_data_yaml_address)
    val_parent_folder = "/".join(yaml_file['val'].split("/")[:-1])
    return yaml_file, val_yaml_address, val_parent_folder


def get_val_yaml_address(original_yaml_address):
    full_path = original_yaml_address.split("/")[:-1]
    full_path.append('val_only.yaml')
    full_path = "/".join(full_path)
    return full_path


def create_val_dirs(data_yaml, data_yaml_address, parent_folder="."):
    test_with_labels_path = os.path.join(parent_folder, "test_with_labels")
    Path(test_with_labels_path).mkdir(parents=True, exist_ok=True)
    create_labels_images(test_with_labels_path)
    data_yaml['val'] = test_with_labels_path
    data_yaml['train'] = ""
    save_yaml_file(data_yaml, data_yaml_address)
    return data_yaml


def get_coco_file_on_images_without_labels(test_folder_path, save_output_path, model, test_param_dict):
    test_folder_image_paths = get_image_paths_from_folder(test_folder_path)
    # results = model.predict(test_folder_image_paths, **test_param_dict)
    results = get_model_predictions(model, test_folder_image_paths, test_param_dict)
    all_detections = []
    for j, result in enumerate(results):
        all_detections.append(sv.Detections.from_ultralytics(result))
    # TODO: Check if below is the right way to get class list
    save_results_as_coco(all_detections, test_folder_image_paths, class_list=results[0].names.values(),
                         save_path=save_output_path)
    return None


def save_results_as_coco(results, image_paths,  class_list, save_path):
    # creating detections and saving the inference results with coco format
    name_image_dict = {}
    name_detections_dict = {}

    images = get_images_from_paths(image_paths)
    image_names = get_names_from_names_with_extension(image_paths)
    # TODO: below should be changed
    image_names = [image_name + '.tif' for image_name in image_names]
    for j, img_name in enumerate(image_names):
        if results[j].mask is not None:
            name_image_dict[img_name] = images[j]
            name_detections_dict[img_name] = results[j]

    inference_dataset = sv.DetectionDataset(class_list, name_image_dict, name_detections_dict)
    inference_dataset.as_coco(annotations_path=save_path,
                              approximation_percentage=0.95)
    return None


def get_model_predictions(model, folder_of_images, test_dict):
    results = model.predict(
        folder_of_images, **test_dict
    )
    results = preprocess_masks(results)
    return results


def preprocess_masks(results):
    xy = []
    for result_idx, result in enumerate(results):
        all_masks = result.masks
        if all_masks:
            all_masks_data = all_masks.data.int().cpu().numpy().astype("uint8")
            for mask_idx, mask in enumerate(all_masks_data):
                mask_shape = mask.shape
                cnt, heir = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                # if contours are present, find the biggest one
                if len(cnt) > 1:
                    # find the biggest one by the area
                    c = max(cnt, key=cv2.contourArea)
                    # make new variables
                    xy = c.reshape(-1, 2)
                    xyn = xy.copy()
                    xyn[:, 0], xyn[:, 1] = xyn[:, 0]/mask_shape[0], xyn[:, 1]/mask_shape[1]
                    new_mask_data = mask.copy()
                    new_mask_data[:, :] = 0
                    cv2.drawContours(new_mask_data, [c], -1, 1, thickness=cv2.FILLED)
                    # TODO: Update boxes object too using below data
                    # TODO: Check if original mask was in cpu or cuda and change it acc. here
                    new_mask_data = torch.from_numpy(new_mask_data)
                    # update old variables
                    all_masks.data[mask_idx].xy = xy
                    all_masks.data[mask_idx].xyn = xyn
                    cloned_all_masks_data = all_masks.data.clone()
                    cloned_all_masks_data[mask_idx] = new_mask_data
                    all_masks.data = cloned_all_masks_data
                    results[result_idx].masks = all_masks
    return results
