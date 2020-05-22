import os
import pandas as pd
from geojson import Feature, FeatureCollection, Point


def grab_lat_lon(filename):

    segments=filename.split(' ')
    lon=float(segments[0])
    small_segments=segments[-1].split('.JPG')
    lat=float(small_segments[0])
    #print(filename, ' lat= ',lat, type(lat),' lon= ',lon,type(lon))
    return lat,lon
#only works for specific df as Name,LAT,LON
def dataframe_to_geojson(df,geojsonpath):
    features=[]
    for i in range(0,len(df),1):
        try:

            latitude=df.at[i,'Lat']
            longitude=df.at[i,'Lon']
            #print ('mark', latitude,longitude)
            features.append(
                Feature(
                    geometry = Point((longitude, latitude)),
                    properties = {
                        'Image': df.at[i,'Name'],
                        #'Imagepath': Imagepath
                }
            )
        )
        except:
            print(df.at[i,'Name']+ ' error')
    collection = FeatureCollection(features)
    with open(geojsonpath, "w") as f:
        f.write('%s' % collection)

df=pd.DataFrame(columns=['Name','Lat','Lon'])
panoramaimage_path='D:\OneDrive - The University Of Hong Kong\Co-work\SiteVisit\TaiWoHauPhoto/panorama/'
#csvpath='D:\HK B\SiteVisitPlanPreparation\Photos\JSVisulization\panorama.csv'
geojsonpath='panorama.geojson'

photolist=os.listdir(panoramaimage_path)
for item in photolist:
    lat,lon=grab_lat_lon(item)
    new_row = pd.Series({'Name': item, 'Lat': lat, 'Lon': lon})
    df = df.append(new_row, ignore_index=True)
print(df)
dataframe_to_geojson(df,geojsonpath)

