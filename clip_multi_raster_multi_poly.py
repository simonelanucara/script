import os
from osgeo import gdal, ogr

#def ClipRasterWithPolygon():
#	os.system("gdalwarp -crop_to_cutline -cutline" + polyPath + rasterPath + outhPath)
#	os.system("gdalwarp -crop_to_cutline -cutline /home/jovyan/work/ClippingFeatures/106/clip.shp /home/jovyan/work/infolder/S2_20160718_022_32TQQ3_A_NDVI.tif /home/jovyan/work/ClippingFeatures/106/raster.tif")

def CreateClippingPolygons(inPath, field):
	inPath = ('/home/jovyan/work/shp/jolanda_pianocolt_grano_duro_date.shp')
	driverSHP = ogr.GetDriverByName("Esri Shapefile")
	ds = ogr.Open(inPath)
	if ds is None:
		print ('layer not open')
	else:
		lyr = ds.GetLayer()
		spatialRef = lyr.GetSpatialRef()
		for feature in lyr:
			fieldVal=feature.GetField('fid')
			os.mkdir("ClippingFeatures/" + str(fieldVal))
			outds = driverSHP.CreateDataSource("ClippingFeatures/" + str(fieldVal) + "/clip.shp")
			outlyr = outds.CreateLayer(str(fieldVal) + "/clip.shp", srs=spatialRef, geom_type=ogr.wkbPolygon)
			outDfn = outlyr.GetLayerDefn()
			ingeom = feature.GetGeometryRef()
			outFeat = ogr.Feature(outDfn)
			outFeat.SetGeometry(ingeom)
			outlyr.CreateFeature(outFeat)

def ClipRaster(inPath, fid):
	inPath = ('/home/jovyan/work/shp/jolanda_pianocolt_grano_duro_date.shp')
	driverSHP = ogr.GetDriverByName("Esri Shapefile")
	ds = ogr.Open(inPath)
	if ds is None:
		print ('layer not open')
	else:
		lyr = ds.GetLayer()
		spatialRef = lyr.GetSpatialRef()
		for feature in lyr:
			fieldVal=feature.GetField('fid')
			clipshape = ("/home/jovyan/work/ClippingFeatures/" + str(fieldVal) + "/clip.shp")
			for sentinel in os.listdir('/home/jovyan/work/infolder/'):
				if sentinel.endswith('.tif'):
					rastername = sentinel
				raster = ('/home/jovyan/work/infolder/'+ str(rastername))
				output = ("/home/jovyan/work/ClippingFeatures/" + str(fieldVal) + "/" + str(fieldVal) + "_" +  str(rastername))
				os.system("gdalwarp -crop_to_cutline -cutline " + clipshape + " " + raster + " " + output)
#run
os.mkdir("ClippingFeatures")
CreateClippingPolygons("nome_poligoni.shp", "nome_12")
ClipRaster("nome_raster.shp", "nome_12")
