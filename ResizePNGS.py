from PIL import Image
from resizeimage import resizeimage

png_path = ("/Users/lornerutherford/Pictures/20211007_HighResChannel/calculus/")

for file_name in png_path:
    f_img = png_path+'/'+file_name
    if f_img.endswith(".png"):
        img = Image.open(f_img)
        img = resizeimage.resize_width(img, 2000)
        img.save(f_img)
