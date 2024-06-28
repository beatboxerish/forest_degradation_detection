from mhadei_restoration.utils.gis_utils import *
import geopandas as gpd


# change the below mapping depending on how you want to map degradation indicator names to classes
def map_name_to_class(x):
    if 'Bare' in x:
        return 1
    elif 'Shaded' in x:
        return 2
    elif 'Vegetated' in x:
        return 3
    elif 'Plantation' in x:
        return 4
    elif 'Invasive' in x:
        return 5
    elif 'Creeper' in x:
        return 6
    elif 'Cane' in x:
        return 7
    return 0


# TODO: Convert below paths from relative to full inside of functions
# input variables
# different site-specific folders which contain vector files
vector_folders = ["/Users/ishannangia/Desktop/TfW/tifs and labels/restorationSite_tifs/",
                  "/Users/ishannangia/Desktop/TfW/tifs and labels/burntSite_tifs/",
                  "/Users/ishannangia/Desktop/TfW/tifs and labels/chromoStrobeSite_tifs/",
                  "/Users/ishannangia/Desktop/TfW/tifs and labels/plantationSite_tifs/"]
# file to understand extent of the final raster that will be created
extent_file_path = "/Users/ishannangia/Desktop/TfW/MhadeiAoi/MhadeiAoi.shp"
# raster path to be outputted
output_raster_path = "/Users/ishannangia/Desktop/TfW/all_true_dis.tif"
class_col_name = 'classes'

# if using resolution from file
res_file_path = "/Users/ishannangia/Downloads/AllBands_stnlMar2024_resampled_10cm.tif"
res, _ = get_resolution_from_resolution_file_path(res_file_path, gpd.read_file(extent_file_path).crs)
# if using resolution value directly
# res = 0.00001  # desired resolution

# main processes
vector_paths = get_vectors_from_folders(vector_folders)
gdf = form_gdf_from_vector_files(vector_paths)
gdf[class_col_name] = gdf.name.apply(map_name_to_class)
out_meta = get_meta_data_for_transform(extent_file_path, res)
write_vector_to_raster(output_raster_path, out_meta, gdf, class_col_name)
