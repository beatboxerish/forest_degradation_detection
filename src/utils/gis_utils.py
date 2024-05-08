import geopandas as gpd
import rasterio
from rasterio import transform, features
import pandas as pd


def form_gdf_from_vector_files(vector_paths):
    gdf_list = []
    for vector_path in vector_paths:
        gdf = gpd.read_file(vector_path)
        gdf_list.append(gdf)

    main_gdf = gpd.GeoDataFrame(pd.concat(gdf_list, ignore_index=True))
    return main_gdf


def get_meta_data_for_transform(extent_file_path, res):
    extent_file = gpd.read_file(extent_file_path)
    bbox = extent_file.total_bounds
    xmin, ymin, xmax, ymax = bbox

    w = (xmax - xmin) // res
    h = (ymax - ymin) // res

    out_meta = {
        "driver": "GTiff",
        "dtype": "uint8",
        "height": h,
        "width": w,
        "count": 1,
        "crs": extent_file.crs,
        "transform": transform.from_bounds(xmin, ymin, xmax, ymax, w, h),
        "compress": 'lzw'
    }
    return out_meta


def get_resolution_from_resolution_file_path(res_file_path):
    ds = rasterio.open(res_file_path)
    pixel_size_x, pixel_size_y = ds.res
    return pixel_size_x, pixel_size_y


def write_vector_to_raster(output_raster_path, out_meta, gdf, class_col_name):
    with rasterio.open(output_raster_path, 'w+', **out_meta) as out:
        out_arr = out.read(1)

        # this is where we create a generator of geom, value pairs to use in rasterizing
        shapes = ((geom, value) for geom, value in zip(gdf.geometry, gdf[class_col_name]))

        burned = features.rasterize(shapes=shapes, fill=0, out=out_arr, transform=out.transform)
        out.write_band(1, burned)
    return None
