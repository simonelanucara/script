# Bulk import geojson from a dir to postgis using ogr2ogr

#search all files in a directory
for var in YOUR DIR *.geojson
do
echo "importing $var to DB..."
sudo ogr2ogr -f "PostgreSQL" PG:"host='YOUR HOSTNAME' user='YOUR USERNAME' port='PORT' dbname='DBNAME' password='PASSWORD'" $var -nln TABLENAME -update -append
done
