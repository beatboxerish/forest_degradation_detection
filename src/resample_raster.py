from src.utils.gis_utils import resample_raster, get_resolution_from_resolution_file_path
import rasterio

input_raster = "/Users/ishannangia/Desktop/AllBands_stnlMar2024.tif"
output_raster = "/Users/ishannangia/Desktop/AllBands_stnlMar2024_resampled.tif"
scale_raster_path = "/Users/ishannangia/Desktop/TfW/tifs and labels/restorationSite.tif"

# either specify the scale explicitly
# scale = 10
# or calculate the scale using another file
crs_in_use = rasterio.open(input_raster).crs
# res_target, _ = get_resolution_from_resolution_file_path(scale_raster_path, crs_in_use)
res_target = 0.1
res_source, _ = get_resolution_from_resolution_file_path(input_raster, crs_in_use)
scale = res_source/res_target
# print(res_target, res_source, scale)

resample_raster(input_raster, output_raster, scale)
