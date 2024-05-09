import labelme2coco

input_folder_path = ("/Users/ishannangia/github_repos/Mhadei_Restoration/data/"
                     "original-data/annotation_files_labelme-images_orthos/")
output_folder_path = ("/Users/ishannangia/github_repos/Mhadei_Restoration/"
                      "data/original-data/annotation_files_coco-images_orthos/")
dataset_name = "iteration-II"

# conversion
labelme2coco.convert(input_folder_path, output_folder_path, dataset_name=dataset_name)
