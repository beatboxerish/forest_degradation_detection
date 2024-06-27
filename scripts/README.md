This folder contains different scripts that can be run independently of each other but might need the 
output of another script as an input to run properly.
All of these depend on the code in the mhadei_restoration folder in this repo.

Something to note is that for a lot of this workflow, the python library fiftyone might be used. 
fiftyone is super easy to use and I discovered it long after writing this code so didn't end up using it.

The scripts have been described below in no particular order:

* coco2labelme: Converts coco formatted instance segmentation annotations to labelme formatted files
* correct_coco_file: When converting from labelme annotations to COCO format, there were some problems with the 
coco file the code was creating. Thus, chose to edit the labelme based coco file with this script.
* create_coco_file_from_labelme: Create coco annotations file from a group of labelme annotations
* create_yolo_dataset_from_coco: Creates yolo formatted files with train, val, test sets from a given COCO file
* resample_raster: Allows one to change the resolution of the raster file being used to match another files resolution
or a manually inputted resolution
* test_yolo: Runs inference using a trained yolov8 model on given images
* vector_to_raster: Converts raster file from different vector objects
* yolo_from_coco_crossval: Uses cross-validation to create yolo formatted datasets for running cross-validation
* yolo_to_coco_conversion: Convert yolo formatted output into coco formatted annotations

