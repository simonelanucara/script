import os
import glob
import gdal
import numpy as np
from sklearn import cluster

directory_to_check = "/home/jovyan/work/ClippingFeatures/" # Which directory do you want to start with?

def my_function(directory):
# get rasters' file names
    fnames = glob.glob('*_max_values_ndvi.tif')
# read general properties of the first raster (assuming all the rasters share these properties)
    ds = gdal.Open(fnames[0], 0)
    gt = ds.GetGeoTransform()
    sr = ds.GetProjection()
    xsize = ds.RasterXSize
    ysize = ds.RasterYSize
    nd = ds.GetRasterBand(1).GetNoDataValue()
    del ds
    
    arrays = []
    for fn in fnames:
        ds = gdal.Open(fn, 0)
        arr = ds.ReadAsArray()  # 2D array (rows by columns)
        arrays.append(arr)
        del ds
#    arr = np.stack(arrays)  # 3D array (date by rows by columns)
    X = arr.reshape((-1,1))
#calculate k_means

    k_means = cluster.KMeans(n_clusters=4)
    k_means.fit(X)

    X_cluster = k_means.labels_
    X_cluster = X_cluster.reshape(arr.shape)
    
    [cols, rows] = arr.shape
# create the output raster
    out_fn = ('k_means_max_values_ndvi.tif')
    driver = gdal.GetDriverByName('GTiff')
    out_ds = driver.Create(out_fn, rows, cols, 1, gdal.GDT_Byte)  # you might want to change the pixel type
    out_ds.SetGeoTransform(gt)
    out_ds.SetProjection(sr)
    out_band = out_ds.GetRasterBand(1)
    out_band.SetNoDataValue(nd)
    out_band.WriteArray(X_cluster)
#    outDataRaster.GetRasterBand(1).WriteArray(X_cluster)
    
directories = [os.path.abspath(x[0]) for x in os.walk(directory_to_check)]
directories.remove(os.path.abspath(directory_to_check)) # If you don't want your main directory included

for i in directories:
      os.chdir(i)         # Change working Directory
      my_function(i)      # Run your function
