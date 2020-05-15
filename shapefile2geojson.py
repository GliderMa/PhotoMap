import geopandas as gpd
path='D:\HK B\SiteVisitPlanPreparation\Photos/'
read_shapefilepath='Planter_edit_coord.shp'
export_path='D:\HK B\SiteVisitPlanPreparation\Photos\JSVisulization/'
geojson_name='Planter.geojson'
df=gpd.read_file(path+read_shapefilepath)
df.to_file(export_path+geojson_name, driver='GeoJSON')