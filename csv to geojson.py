
    #Actually Works

import csv, json
from geojson import Feature, FeatureCollection, Point

features = []
with open('JSVisulization/photoinfo_updated.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for Image, latitude, longitude, in reader:
        try:
            latitude, longitude = map(float, (latitude, longitude))
            features.append(
                Feature(
                    geometry = Point((longitude, latitude)),
                    properties = {
                        'Image': Image,
                        #'Imagepath': Imagepath
                }
            )
        )
        except:
            print(Image+ ' error')

collection = FeatureCollection(features)
with open("JSVisulization/photo_updated.geojson", "w") as f:
    f.write('%s' % collection)
