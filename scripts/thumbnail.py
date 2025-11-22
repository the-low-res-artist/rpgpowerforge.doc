
# =========================================================
# import section
import re 
import sys 
import os 
import time
import shutil
import random
from PIL import ImageFont, ImageDraw, Image
from datetime import datetime
from pathlib import Path

from config import config


# =========================================================
# constant values
BOOK_ROOT = "/home/www-data/rpgpowerforge/book"


# =========================================================
# slip evenly a sentence string (for title)
def split_string_equally(input_string):
    total_chars = len(input_string)
    half_chars = total_chars // 2

    # ------------------------------------------------------------
    # Find the closest space to half_chars
    offset = 0
    index = 0
    space_found = False
    while not space_found:
        index = half_chars + offset
        # found
        if input_string[index] == ' ':
            space_found = True
        else:
            if offset == 0:
                offset += 1
            elif offset > 0:
                offset = (offset * -1)
            elif offset < 0:
                offset = (offset * -1) + 1
    
    first_half = input_string[:index]
    second_half = input_string[(index+1):] #skip first space

    return first_half, second_half


# =========================================================
# add a cool title to the thumbnail
def get_new_thumbnail_image(filepath, title, file_template):
    basename = os.path.basename(filepath)
    
    # ------------------------------------------------------------
    # open template image
    with Image.open(file_template) as image:

        # get the image
        draw = ImageDraw.Draw(image)

        # text to draw
        subtitle = "User manual"

        # create 2 fonts
        font_title = ImageFont.truetype(f"{BOOK_ROOT}/resources/mont.otf", 110)
        font_subtitle = ImageFont.truetype(f"{BOOK_ROOT}/resources/mont.otf", 50)
        front_color = (255, 255, 255, 255)
        back_color = (0, 0, 0, 255)

        # ------------------------------------------------------------
        # case if short title
        if (len(title) <= 12) or (not ' ' in title):
            # title
            for x in range(-4,5,2):
                for y in range(-4, 5, 2):
                    draw.text((20+x, 400+y), title, font=font_title, fill=back_color)
            draw.text((20, 400), title, font=font_title, fill=front_color)

            # subtitle
            for x in range(-4,5,2):
                for y in range(-4, 5, 2):
                    draw.text((23+x, 500+y), subtitle, font=font_subtitle, fill=back_color)
            draw.text((23, 500), subtitle, font=font_subtitle, fill=front_color)
        
        # ------------------------------------------------------------
        # case long titles
        else:
            title_row1, title_row2 = split_string_equally(title)
            # title row 1
            for x in range(-4,5,2):
                for y in range(-4, 5, 2):
                    draw.text((20+x, 350+y), title_row1, font=font_title, fill=back_color)
                    draw.text((20+x, 450+y), title_row2, font=font_title, fill=back_color)
            draw.text((20, 350), title_row1, font=font_title, fill=front_color)
            draw.text((20, 450), title_row2, font=font_title, fill=front_color)
            
        # ------------------------------------------------------------
        # save
        output_filename = str(hash(title))
        thumbnail_path = f"{BOOK_ROOT}/media/thumbnail/thumbnail_{output_filename}.jpg"
        image.save(thumbnail_path)

    return thumbnail_path.replace(BOOK_ROOT, config.website_root)


# =========================================================
# replace in a file
def set_thumbnail(filepath):

    # ------------------------------------------------------------
    # Safely read the input file using 'with'
    s= ""
    with open(filepath, 'r', encoding="utf8") as f:
        s = f.read()

    # safe exit
    if (s == ""):
        return

    # ------------------------------------------------------------
    # get file title
    titles = re.findall("<h1.+?><a.+?>(.+?)</a>", s)
    if len(titles) > 0:
        title = titles[0].replace("<strong>", "").replace("</strong>", "")
    else:
        title = "Documentation"

    file_url = filepath.replace(BOOK_ROOT, config.website_root)
    description="The awesome documentation for the Unity package : RPG Power Forge"
    image= get_new_thumbnail_image(filepath, title, f"{BOOK_ROOT}/media/thumbnail/thumbnail_v3.jpg")
    title="RPG Power Forge documentation site"
    author="@rpgpowerforge"
    site="rpgpowerforge.com"

    thumbnail = f"<!-- Custom HTML thumbnail image and metadata -->\
    <meta property=\"og:image\" content=\"{image}\">\
    <meta property=\"og:image:width\" content=\"1200\">\
    <meta property=\"og:image:height\" content=\"630\">\
    <meta property=\"og:image:type\" content=\"image/jpeg\">\
    \
    <meta property=\"og:site_name\" content=\"{site}\">\
    <meta property=\"og:locale\" content=\"en_EN\">\
    <meta property=\"og:title\" content=\"{title}\">\
    <meta property=\"og:description\" content=\"{description}\">\
    <meta property=\"og:url\" content=\"{file_url}\">\
    <meta property=\"og:type\" content=\"article\">\
    \
    <meta property=\"og:rating\" content=\"1\">\
    <meta property=\"og:rating_scale\" content=\"2\">\
    <meta property=\"og:rating_count\" content=\"3\">\
    \
    <meta name=\"twitter:card\" content=\"summary_large_image\">\
    <meta name=\"twitter:site\" content=\"{author}\">\
    <meta name=\"twitter:creator\" content=\"{author}\">\
    <meta name=\"twitter:url\" content=\"{file_url}\">\
    <meta name=\"twitter:title\" content=\"{title}\">\
    <meta name=\"twitter:description\" content=\"{description}\">\
    <meta name=\"twitter:image\" content=\"{image}\">\
    <meta property=\"twitter:url\" content=\"{file_url}\">\
    <meta property=\"twitter:title\" content=\"{title}\">\
    <meta property=\"twitter:description\" content=\"{description}\">\
    <meta property=\"twitter:image\" content=\"{image}\">"

    str_to_replace = "</head>"
    str_replacement = f"{thumbnail}</head>"
    s = s.replace(str_to_replace, str_replacement)

    # ------------------------------------------------------------
    # Safely write the changed content
    with open(filepath, 'w', encoding="utf8") as f:
        f.write(s)

# =========================================================
# entry point
if __name__ == "__main__":
    
    start = time.time()

    # ------------------------------------------------------------
    # iterate all files, find html files
    file_count = 0
    for filepath in Path(BOOK_ROOT).rglob("*.html"):
        set_thumbnail(filepath)
        file_count+=1
        sys.exit(0)

    end = time.time()
    print(f"{file_count} thumbnails created in {str(round(end - start, 1))} sec")

    # safe return
    sys.exit(0)