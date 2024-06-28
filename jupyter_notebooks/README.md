These are the Jupyter notebooks that contain snippets of code that has been used in this project.

They broadly cover two different areas: ML code and Preprocessing Code

**ML**

This is the instance segmentation model specific code that can be run on colab notebooks easily.
* training_code: Contains the YOLO-related code
* detecttree2: Contains the Mask R-CNN-related code

**Preprocessing**

These are general preprocessing functions that are super important in our pipeline. Since these area jupyter notebooks
which were being run locally, one would need to install the libraries being used in these notebooks before running
them.
* Common Preprocessing Functions: A bunch of preprocessing functions that have been used to process TIFFs, labels,
and vectors.
* Removing Vector Portions from TIFs: Code to help one remove any given area present in a given geojson/vector file
from a given TIFF.
