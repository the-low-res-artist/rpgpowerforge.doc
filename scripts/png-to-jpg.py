
import re # regex operations
import sys # to return 0
import os # loop over files
from config import config
from PIL import ImageFont, ImageDraw, Image
import time # measure duration

# goal : to find and replace all png call image by a jpg alternative

# replace in a file
def set_png_to_jpg(filename):

    # Safely read the input filename using 'with'
    s= ""
    with open(filename, 'r', encoding="utf8") as f:
        s = f.read()

    # safe exit
    if (s == ""):
        return

    # find all images call in the md file
    images_path = re.findall(r"!\[.+?\]\(.+?(media.+?\.png)\)", s)

    # iterate images
    for png_image_path in images_path:

        #skip images that are meant to be downloaded by user
        # images in "user_resources/""
        if "user_resources" in png_image_path:
            continue

        # skip buttons
        if "clickable_buttons" in png_image_path:
            continue

        input_path = f"./../{png_image_path}"
        # open png and save a jpg
        with Image.open(input_path) as image:
            jpg_image_path = png_image_path.replace(".png", ".jpg")
            output_path = f"./../{jpg_image_path}"
            image.convert('RGB').save(output_path, format="JPEG", quality=80)
            # replace path in md file if this is a success AND jpg is lighter
            png_size_byte = os.path.getsize(input_path) 
            jpg_size_byte = os.path.getsize(output_path) 
            # jpg wins !
            if (jpg_size_byte < png_size_byte):
                s = s.replace(png_image_path, jpg_image_path)


    # Safely write the changed content
    with open(filename, 'w', encoding="utf8") as f:
        f.write(s)


# entry point
start = time.time()
src_root = "./../src/"
nb_files=0
for root, dirs, files in os.walk(src_root, topdown=False):
   for filename in files:
        if filename.endswith(".md"):
            set_png_to_jpg(os.path.join(root, filename))
            nb_files+=1

end = time.time()
print(f"[{str(round(end - start, 1))} sec] PNG TO JPG UPDATE : {nb_files} updated")

# safe return
sys.exit(0)