from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS
import os
import pandas as pd
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
df=pd.DataFrame(columns=['Name','Lat','Lon'])
csvpath='D:\HK B\SiteVisitPlanPreparation\Photos\JSVisulization\photoinfo_updated.csv'
pathcollection=['D:\HK B\SiteVisitPlanPreparation\Butterfly/',
      'D:\HK B\SiteVisitPlanPreparation\YAUOI\YauOiPhoto\Yau OI/',
      'D:\HK B\SiteVisitPlanPreparation\LongPing\LongPingPhotos\Estate Photo/']
for path in pathcollection:
    photolist=os.listdir(path)







    for name in photolist:
        try:

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

    df.to_csv(csvpath,index=None)