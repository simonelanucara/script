import glob
import os

import gdal
import numpy as np

directory_to_check = "/home/jovyan/work/ClippingFeatures/" # Which directory do you want to start with?

def subdirname():
    for dir in os.listdir('/home/jovyan/work/ClippingFeatures/'):
        dirname = dir

def my_function(directory):
      # get rasters' file names
    fnames = glob.glob('*.tif')

# read general properties of the first raster (assuming all the rasters share these properties)
    ds = gdal.Open(fnames[0], 0)
    gt = ds.GetGeoTransform()
    sr = ds.GetProjection()
    xsize = ds.RasterXSize
    ysize = ds.RasterYSize
    nd = ds.GetRasterBand(1).GetNoDataValue()
    del ds

# read each raster and create a 3D array
    arrays = []
    for fn in fnames:
       ds = gdal.Open(fn, 0)
       arr = ds.ReadAsArray()  # 2D array (rows by columns)
       arrays.append(arr)
       del ds
    arr = np.stack(arrays)  # 3D array (date by rows by columns)

# mask the array to exclude values outside a defined range
    mask = (arr < 0) & (arr > 10000)
    arr = np.ma.array(arr, mask=mask)

# get maximum value for each pixel
    arr = np.max(arr, axis=0)

# fill the array with the NoData value
    arr = arr.filled(nd)

# create the output raster
#    out_fn = 'max_values_ndvi.tif'
    out_fn = (str(dirname) + '_max_values_ndvi.tif')
    driver = gdal.GetDriverByName('GTiff')
    out_ds = driver.Create(out_fn, xsize, ysize, 1, gdal.GDT_Float32)  # you might want to change the pixel type
    out_ds.SetGeoTransform(gt)
    out_ds.SetProjection(sr)
    out_band = out_ds.GetRasterBand(1)
    out_band.SetNoDataValue(nd)
    out_band.WriteArray(arr)

# save and close output file
    out_band.FlushCache()
    del out_ds, out_band

# Get all the subdirectories of directory_to_check recursively and store them in a list:
    directories = [os.path.abspath(x[0]) for x in os.walk(directory_to_check)]
    directories.remove(os.path.abspath(directory_to_check)) # If you don't want your main directory included

for i in directories:
      os.chdir(i)         # Change working Directory
      my_function(i)      # Run your function
