'''
extract EXIF infomation, record it in csv,generate geojson file, and make thumb photos
'''
from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS
import os
import pandas as pd
from geojson import Feature, FeatureCollection, Point
def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()
def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging
def get_decimal_from_dms(dms, ref):

    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)

def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return lat,lon
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
def make_thumbnail(folderpath,savepath,filename):
    imagepath=folderpath+filename
    img = Image.open(imagepath)

    (width, height) = img.size
    if width > height:
        ratio = 450 / width
    else:
        ratio = 450 / height

    img.thumbnail((round(width * ratio), round(height * ratio)), Image.LANCZOS)
    img.save(savepath+ filename)
#df=pd.DataFrame(columns=['Name','Lat','Lon'])

csvpath='D:\HK B\SiteVisitPlanPreparation\Photos\JSVisulization\photoinfo_updated.csv'
exportpath='D:\HK B\SiteVisitPlanPreparation\Photos\JSVisulization\photoinfo_updated0601.csv'
pathcollection=[
    'D:\HK B\SiteVisitPlanPreparation/NorthDistrict/NorthDistrict/NorthDistrict/',
     'D:\HK B\SiteVisitPlanPreparation\ShamshuiPo\ShamShuiPo\ShamShuiPo/',
     # 'D:\HK B\SiteVisitPlanPreparation\ShunTinEstate\ShunTinEstate/'
                ]
thumbphotopath='D:\HK B\SiteVisitPlanPreparation\Photos\JSVisulization\ThumbPhoto/'
geojsonpath='photo_updated.geojson'
df=pd.read_csv(csvpath)
for path in pathcollection:
    photolist=os.listdir(path)







    for name in photolist:
        try:
            make_thumbnail(path, thumbphotopath, name)
            # make thumbnail
            filepath=path+name
            #print(filepath)
            exif = get_exif(filepath)
            geotags = get_geotagging(exif)
            lat,lon=get_coordinates(geotags)
            #print(latlon)

            new_row=pd.Series({'Name':name,'Lat':lat,'Lon':lon})
            df=df.append(new_row,ignore_index=True)
        except:
            print(name+' error')

    df.to_csv(exportpath,index=None)
    dataframe_to_geojson(df, geojsonpath)