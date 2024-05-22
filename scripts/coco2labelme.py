from mhadei_restoration.utils.coco_to_labelme_utils import CocoDatasetHandler


coco_file_path = '../results/yolo_to_coco_trial.json'
images_folder_path = '../data/Yolo-iteration-II/train/images'
output_folder = '/Users/ishannangia/Desktop/del_this/'

ds = CocoDatasetHandler(coco_file_path, images_folder_path)
ds.coco2labelme()
ds.save_labelme(ds.labelme.keys(), output_folder)
