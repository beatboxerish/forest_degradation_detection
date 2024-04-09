from src.utils.test_utils import get_bboxes_masks_on_image
from src.utils.yolo_utils import load_yolo


test_image_path = "../data/Yolo-2/test/images/chromoStrobeSite_x_1920_y_1920.tif"
save_image_path = "../results/testing_this.png"
model_path = '../models/yolo-2_best.pt'

model = load_yolo(model_path)

get_bboxes_masks_on_image(test_image_path, save_image_path, model)

