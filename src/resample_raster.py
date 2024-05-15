from src.utils.gis_utils import resample_raster, get_resolution_from_resolution_file_path

input_raster = "/Users/ishannangia/Desktop/AllBands_stnlMar2024.tif"
output_raster = "/Users/ishannangia/Desktop/plantationSite_x_1920_y_0_resampled.tif"
scale_raster_path = "/Users/ishannangia/Desktop/plantationSite_x_1920_y_0.tif"
scale = 1

res_target, _ = get_resolution_from_resolution_file_path(scale_raster_path)
res_source, _ = get_resolution_from_resolution_file_path(input_raster)

# scale = res_source/res_target

print(res_target, res_source, scale)
resample_raster(input_raster, output_raster, scale)
