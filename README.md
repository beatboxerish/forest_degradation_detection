# Forest Degradation Detection

This repo contains python code for a [TfW](https://www.techforwildlife.com/) project where we were using satellite+drone images to detect 
degradation in Mhadei Wildlife Sanctuary.

We used conda to create and manage environments. 

For running the code in the scripts folder of this project, one can create an env by installing miniconda/anaconda 
and:
`conda create --name <env> --file requirements.txt`

For running the code in the preprocessing jupyter notebooks, one can create an env by installing miniconda/anaconda 
and:
`conda create --name <env> --file jupyternb_requirements.txt`

This repo contains the following:
* jupyter_notebooks: Jupyter notebooks that were used for preprocessing and modelling purposes.
* mhadei_restoration: This contains the config along with all the utils need for scripts to run.
* scripts: The main scripts used for running different processes, converting data formats, processing
vectors and rasters, etc. These should be looked at for anything related to processing of data. They contain
most of the final non-ML usable code.

A brief description of different files is given in their respective folders. However, to understand the full pipeline
of steps along with when to use which piece of code, follow the below writeup.

---
The following is the sequence in which we approached the modelling of our images. This short writeup is ideally for
someone who has read or has access to our paper or is planning to work with the code. 
Otherwise, it will be tough to follow the sequence, establish context, understand the terms and motivation, etc.

**Dividing a larger TIFF file into smaller TIFF files**

This is usually the first step before labelling and training of any model. Code snippet for this is present
in the Common Preprocessing Functions.ipynb. However before this, it is prudent, but optional, to ensure that all 
orthomosaics are following the same CRS. Code for that conversion is also present in the same notebook.

**Labelling of Orthomosaics**
This happened in LabelMe for us. No code here helps in the labelling process itself.

**Conversion from LabelMe to Other Formats**
Once we get the annotations in LabelMe's format, we have two downstream tasks where these annotations will flow to:
The instance segmentation modelling and satellite modelling.

* For satellite modelling: These labels need to be converted into vectors that can be shared with the satellite
modelling team to include them along with other inputs to the model. This can be done by consulting 
Common Preprocessing Functions.ipynb. 
* For instance segmentation modelling: To convert these annotations into coco and yolo formats, one can use
files from the scripts folder. In particular, create_coco_file_from_labelme.py -> correct_coco_file.py gets you 
the correct coco file. To convert into yolo dataset either create_yolo_dataset_from_coco.py or yolo_from_coco_crossval.py
could be used depending on whether one simply wants to divide the coco data into train, test, and val or wants to 
perform cross-validation.

**Removal of Distorted Image Sections from TIFFs**
The areas we labelled with 'distorted image' as the class need to be removed from the main large orthomosaics 
that we have been dividing and labelling. These corresponded to the site-specific orthomosaics for us. 
Thus, post conversion of the LabelMe annotations to geojsons, we can use those geojsons in the notebook 
Removing Vector Portions from TIFs.ipynb to perform the removal. These files are then sent to the satellite modelling
process to be used as the base TIFFs.

**Modelling**
By now we have the yolo datasets created along with coco files. Both of these will allow us to train our
models. The training code is in training_code.ipynb and detecttree2.ipynb

**Model Inference**
For getting inferences using the trained models:
* yolo: use test_yolo.py
* mask r-cnn: use the detectree2 notebook itself

**Postprocessing**
Once we have the predictions, they will be downloaded in a coco format or yolo format. Yolo predictions 
can be converted into coco using yolo_to_coco_conversion. Post getting everything in coco, we can convert these 
final annotation files back into labelme format using coco2labelme.py.

That's pretty much it! Once we have the labelme files we can convert them back into geojsons and vectors using the
above steps and can send the final predictions as geojsons to the satellite modelling team.