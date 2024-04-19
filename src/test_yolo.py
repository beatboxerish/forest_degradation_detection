from src.utils.test_utils import (get_bboxes_masks_on_image,
                                  get_comparison_image_with_original_labels,
                                  get_results_of_image_with_labels)
from src.utils.yolo_utils import load_yolo

test_image_path = "../data/Yolo-2/val/images/burntSite_x_1920_y_1920.tif"
test_image_label_path = "../data/Yolo-2/val/labels/burntSite_x_1920_y_1920.txt"
save_image_path = "../results/testing_this.png"
model_path = '../models/yolo-2_best.pt'
original_data_yaml_address = "../data/Yolo-3/data.yaml"
save_results_path = '../results/'

model = load_yolo(model_path)

# getting output image for test data with no labels
# get_bboxes_masks_on_image(test_image_path, save_image_path, model)

# getting output image for test data with labels
# get_comparison_image_with_original_labels(test_image_path, test_image_label_path,
#                                           save_image_path, model)

# getting results object for image with labels
results = get_results_of_image_with_labels(model,
                                           test_image_path,
                                           test_image_label_path,
                                           original_data_yaml_address,
                                           save_results_path)

