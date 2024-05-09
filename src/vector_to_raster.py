from src.utils.gis_utils import *


def map_name_to_class(x):
    if 'Bare' in x:
        return 1
    elif 'Canopy' in x:
        return 2
    elif 'Plantation' in x:
        return 3
    elif 'Invasive' in x:
        return 4
    elif 'Creeper' in x:
        return 5
    elif 'Cane' in x:
        return 6

    # if 'Vegetated' in x:
    #     return 1
    # elif 'Shaded' in x:
    #     return 2
    # elif 'Bare' in x:
    #     return 3
    # elif 'Plantation' in x:
    #     return 4
    # elif 'Invasive' in x:
    #     return 5
    # elif 'Creeper' in x:
    #     return 6
    # elif 'Cane' in x:
    #     return 7
    return 0


# TODO: Convert below paths from relative to full inside of functions
# input variables
vector_folders = ["/Users/ishannangia/Desktop/TfW/tifs and labels/restorationSite_tifs/",
                  "/Users/ishannangia/Desktop/TfW/tifs and labels/burntSite_tifs/",
                  "/Users/ishannangia/Desktop/TfW/tifs and labels/chromoStrobeSite_tifs/",
                  "/Users/ishannangia/Desktop/TfW/tifs and labels/plantationSite_tifs/"]
extent_file_path = "/Users/ishannangia/Desktop/TfW/MhadeiAoi/MhadeiAoi.shp"
output_raster_path = "/Users/ishannangia/github_repos/Mhadei_Restoration/results/full_raster.tif"
res_file_path = "/Users/ishannangia/Desktop/TfW/tifs and labels/restorationSite.tif"
res = 0.00001  # desired resolution
class_col_name = 'classes'

# main processes
vector_paths = get_vectors_from_folders(vector_folders)
gdf = form_gdf_from_vector_files(vector_paths)
gdf[class_col_name] = gdf.name.apply(map_name_to_class)
res, _ = get_resolution_from_resolution_file_path(res_file_path)
out_meta = get_meta_data_for_transform(extent_file_path, res)
write_vector_to_raster(output_raster_path, out_meta, gdf, class_col_name)

