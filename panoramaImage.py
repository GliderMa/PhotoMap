'''
extract xy infomation from file name, generate geojson file, and make thumb photos
'''
import pandas as pd
from geojson import Feature, FeatureCollection, Point
from PIL import Image
import os

def make_thumbnail(folderpath,savepath,filename,size):
    imagepath=folderpath+filename
    img = Image.open(imagepath)

    (width, height) = img.size
    if width > height:
        ratio = size / width
    else:
        ratio = size / height

    img.thumbnail((round(width * ratio), round(height * ratio)), Image.LANCZOS)
    img.save(savepath+ filename)

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
panoramaimage_path_collection=[
    'D:\OneDrive - The University Of Hong Kong\Co-work\SiteVisit\TaiWoHauPhoto/panorama/',
    'D:\OneDrive - The University Of Hong Kong\Co-work\SiteVisit/20200527_ChukYuen_LowerWongTaiSin_LokFu\panorama/',
    'D:\OneDrive - The University Of Hong Kong\Co-work\SiteVisit/20200604_MeiLam_LungHang\Panorama/',
    'D:\OneDrive - The University Of Hong Kong\Co-work\SiteVisit/20200605_KwaiFong_ShekLei1\Panorama/',
    ]
#csvpath='D:\HK B\SiteVisitPlanPreparation\Photos\JSVisulization\panorama.csv'
geojsonpath='panorama.geojson'
panorama_savepath='PanoramaPhoto/'
for panoramaimage_path in panoramaimage_path_collection:

    photolist=os.listdir(panoramaimage_path)
    for item in photolist:
        make_thumbnail(panoramaimage_path, panorama_savepath, item,size=1000)
        lat,lon=grab_lat_lon(item)
        new_row = pd.Series({'Name': item, 'Lat': lat, 'Lon': lon})
        df = df.append(new_row, ignore_index=True)
print(df)
dataframe_to_geojson(df,geojsonpath)

