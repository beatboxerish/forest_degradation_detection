from PIL import Image
import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from src.utils.general_utils import (load_image_with_pil, load_image_with_cv,
                                     get_names_from_names_with_extension)

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
    fig, ax = plt.subplots(1, 3, figsize=(30, 90))
    ax[0].imshow(original_image)
    ax[1].imshow(image_with_bboxes)
    ax[2].imshow(image_with_masks)
    return fig
