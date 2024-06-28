from mhadei_restoration.utils.coco_to_labelme_utils import CocoDatasetHandler


images_folder_path = '../data/original-data/images_orthos-test-dd'  # all images are stored here
coco_file_path = '../results/three_dis_dd_test_data_coco.json'  # COCO for above images
output_folder = '/Users/ishannangia/Desktop/three_dis_dd_labelme_files/'  # where to store output files + images

ds = CocoDatasetHandler(coco_file_path, images_folder_path)
ds.coco2labelme()
ds.save_labelme(ds.labelme.keys(), output_folder)
