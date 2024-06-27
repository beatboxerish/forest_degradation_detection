# Forest Degradation Detection

This repo contains python code for a [TfW](https://www.techforwildlife.com/) project where we were using satellite+drone images to detect 
degradation in Mhadei Wildlife Sanctuary.

This repo contains the following:
* jupyter_notebooks: Jupyter notebooks that were used for particular processes, in particular, for training
the final instance segmentation models and using them for inference. If you are looking to train a model, 
then use this folder. You should be able to easily run these notebooks on Google Colab.
* mhadei_restoration: This contains the config along with all the utils need for scripts to run.
* scripts: The main scripts used for running different processes, converting data formats, processing
vectors and rasters, etc. These should be looked at for anything related to processing of data. They contain
most of the final non-ML usable code.