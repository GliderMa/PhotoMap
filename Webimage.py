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
path='D:\OneDrive - The University Of Hong Kong\Co-work\SiteVisit\TaiWoHauPhoto/Panorama/'
savepath='PanoramaPhoto/'
photolist=os.listdir(path)
for item in photolist:
    make_thumbnail(path,savepath,item,size=1000)