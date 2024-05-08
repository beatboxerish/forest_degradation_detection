from src.utils.gis_utils import *


def map_name_to_class(x):
    if 'Vegetated' in x:
        return 1
    elif 'Shaded' in x:
        return 2
    elif 'Bare' in x:
        return 3


# TODO: Convert below paths from relative to full inside of functions
# input variables
vector_paths = ["/Users/ishannangia/Desktop/TfW/tifs and labels/restorationSite_tifs/Canopy Gap: Bare Land.geojson",
                "/Users/ishannangia/Desktop/TfW/tifs and labels/restorationSite_tifs/Canopy Gap: Shaded.geojson",
                "/Users/ishannangia/Desktop/TfW/tifs and labels/restorationSite_tifs/Canopy Gap: Vegetated.geojson"]
extent_file_path = "/Users/ishannangia/Desktop/TfW/MhadeiAoi/MhadeiAoi.shp"
output_raster_path = "/Users/ishannangia/github_repos/Mhadei_Restoration/results/vec2raster.tif"
res_file_path = "/Users/ishannangia/Desktop/TfW/tifs and labels/restorationSite.tif"
res = 0.00001  # desired resolution
class_col_name = 'classes'

# main processes
gdf = form_gdf_from_vector_files(vector_paths)
gdf[class_col_name] = gdf.name.apply(map_name_to_class)
res, _ = get_resolution_from_resolution_file_path(res_file_path)
out_meta = get_meta_data_for_transform(extent_file_path, res)
write_vector_to_raster(output_raster_path, out_meta, gdf, class_col_name)

