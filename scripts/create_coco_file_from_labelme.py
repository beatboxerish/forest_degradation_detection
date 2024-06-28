import labelme2coco

# folder containing annotations for images
input_folder_path = ("/Users/ishannangia/github_repos/Mhadei_Restoration/data/"
                     "original-data/annotation_files_labelme-images_orthos/")

# folder to save output file in
output_folder_path = ("/Users/ishannangia/github_repos/Mhadei_Restoration/"
                      "data/original-data/annotation_files_coco-images_orthos/")

# output coco file name
output_dataset_name = "final_iteration"

# conversion
labelme2coco.convert(input_folder_path, output_folder_path, dataset_name=output_dataset_name)
