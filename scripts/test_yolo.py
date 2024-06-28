from mhadei_restoration.utils.test_utils import (get_bboxes_masks_on_image,
                                                 get_comparison_image_with_original_labels,
                                                 get_results_of_image_with_labels,
                                                 get_coco_file_on_images_without_labels)
from mhadei_restoration.utils.yolo_utils import load_yolo

# test_image_path = "../data/Yolo-2/val/images/burntSite_x_1920_y_1920.tif"
# test_image_label_path = "../data/Yolo-2/val/labels/burntSite_x_1920_y_1920.txt"
# save_image_path = "../results/testing_this.png"
# original_data_yaml_address = "../data/Yolo-3/data.yaml"
# save_results_path = '../results/'
# model_path = '../models/yolo-10_05.pt'
#
# model = load_yolo(model_path)
#
# getting output image for test data with no labels
# get_bboxes_masks_on_image(test_image_path, save_image_path, model)

# getting output image for test data with labels
# get_comparison_image_with_original_labels(test_image_path, test_image_label_path,
#                                           save_image_path, model)

# getting results object for image with labels
# results = get_results_of_image_with_labels(model,
#                                            test_image_path,
#                                            test_image_label_path,
#                                            original_data_yaml_address,
#                                            save_results_path)

# simple testing without validation. In the case where no data labels are present.
test_folder_path = "../data/original-data/images_orthos-test-dd"  # folder containing test images
save_output_path = '../results/three_dis_dd_test_data_coco.json'
model_path = '../models/three_dis.pt'

model = load_yolo(model_path)

test_param_dict = dict(
    save=True,
    plots=True,
    show_labels=False,
    line_width=0,
    conf=0.05,
    imgsz=640,
    show_conf=False,
    iou=0.01
)
get_coco_file_on_images_without_labels(test_folder_path, save_output_path, model, test_param_dict)
