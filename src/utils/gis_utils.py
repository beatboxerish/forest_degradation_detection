import geopandas as gpd
import rasterio
from rasterio import transform, features
from rasterio.enums import Resampling
from rasterio.warp import calculate_default_transform, reproject
import pandas as pd
from glob import glob
import os


def get_vectors_from_folders(folders_with_vectors):
    files = []
    for folder in folders_with_vectors:
        site_name = folder.strip("/").split("/")[-1].split("_")[0]  # super custom way to remove unwanted files
        vector_path = os.path.join(folder, "*.geojson")
        new_files = glob(vector_path)
        new_files = [i for i in new_files if site_name not in i.strip('/').split("/")[-1]]  # super custom way
        files.extend(new_files)
    return files


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


# TODO: crs_in_use should be replaced by unit like metres/decimal degrees
def get_resolution_from_resolution_file_path(res_file_path, crs_in_use):
    ds = rasterio.open(res_file_path)
    crs = ds.crs
    transformed_ds = transform_crs(ds, crs_in_use, 'del_this.tif')
    pixel_size_x, pixel_size_y = transformed_ds.res
    return pixel_size_x, pixel_size_y


# TODO: hold output tif in memory if no path given
def transform_crs(data_to_transform, dst_crs, output_tif_path):
    # calculating transform along with other parameters for conversion
    transform, width, height = calculate_default_transform(data_to_transform.crs, dst_crs,
                                                           data_to_transform.width, data_to_transform.height,
                                                           *data_to_transform.bounds)

    new_kwargs = data_to_transform.meta.copy()
    new_kwargs.update({
        'crs': dst_crs,
        'transform': transform,
        'width': width,
        'height': height
    })

    # implementing the reprojection
    with rasterio.open(output_tif_path, 'w', **new_kwargs) as dst:
        for i in range(1, data_to_transform.count + 1):
            reproject(
                source=rasterio.band(data_to_transform, i),
                destination=rasterio.band(dst, i),
                src_transform=data_to_transform.transform,
                src_crs=data_to_transform.crs,
                dst_transform=transform,
                dst_crs=dst_crs,
                resampling=Resampling.nearest
            )
    return rasterio.open(output_tif_path)


def write_vector_to_raster(output_raster_path, out_meta, gdf, class_col_name):
    with rasterio.open(output_raster_path, 'w+', **out_meta) as out:
        out_arr = out.read(1)

        # this is where we create a generator of geom, value pairs to use in rasterizing
        shapes = ((geom, value) for geom, value in zip(gdf.geometry, gdf[class_col_name]))

        burned = features.rasterize(shapes=shapes, fill=0, out=out_arr, transform=out.transform)
        out.write_band(1, burned)
    return None


def resample_raster(input_raster_path, output_raster_path, scale_factor=1):
    with rasterio.open(input_raster_path) as dataset:
        # resample data to target shape
        data = dataset.read(
            out_shape=(
                dataset.count,
                int(dataset.height * scale_factor),
                int(dataset.width * scale_factor)
            ),
            resampling=Resampling.bilinear
        )

        # TODO: check the -1, -2 below. Seems fishy
        dst_transform = dataset.transform * dataset.transform.scale(
            (dataset.width / data.shape[-1]),
            (dataset.height / data.shape[-2])
        )

        dst_kwargs = dataset.meta.copy()
        dst_kwargs.update(
            {
                "transform": dst_transform,
                "width": data.shape[-1],
                "height": data.shape[-2],
            }
        )

        with rasterio.open(output_raster_path, "w", **dst_kwargs) as dst:
            # iterate through bands
            for i in range(data.shape[0]):
                dst.write(data[i], i+1)
    return None
