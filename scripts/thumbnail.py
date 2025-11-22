
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
from bs4 import BeautifulSoup
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
# helper to raw text in a bounding box
def draw_text_in_box(draw, box, text, font_path, max_font_size, fill):

    x, y, w, h = box

    # Try decreasing font sizes until the text fits
    font_size = max_font_size
    while font_size > 5:
        font = ImageFont.truetype(font_path, font_size)

        # Word-wrapping: split into lines that fit width
        lines = []
        current = ""
        for word in text.split():
            test_line = current + " " + word if current else word
            if draw.textbbox((0,0), test_line, font=font)[2] <= w:
                current = test_line
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)

        # Measure height
        line_height = draw.textbbox((0,0), "Ay", font=font)[3]
        total_height = line_height * len(lines)

        if total_height <= h:
            break  # it fits

        font_size -= 1  # shrink and try again

    # Draw each line
    cy = y
    for line in lines:
        line_width = draw.textbbox((0,0), line, font=font)[2]
        cx = x
        draw.text((cx, cy), line, font=font, fill=fill, stroke_width = 5, stroke_fill="black")
        cy += line_height

# =========================================================
# add a cool title to the thumbnail
def get_new_thumbnail_image(filepath, title, file_template):
    basename = os.path.basename(filepath)
    
    # ------------------------------------------------------------
    # open template image
    with Image.open(file_template) as image:

        # get the image
        draw = ImageDraw.Draw(image)

        # font settings
        font_box = (27, 360, 715, 235)
        font_text = title
        font_path = f"{BOOK_ROOT}/resources/mont.otf"
        font_color = (255, 255, 255, 255)
        font_max_size = 100

        draw_text_in_box(draw, font_box, font_text, font_path, font_max_size, font_color)
            
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
    content = ""
    with open(filepath, 'r', encoding="utf8") as f:
        content = f.read()

    # safe exit
    if (content == ""):
        return

    # ------------------------------------------------------------
    # Get the soup
    soup = BeautifulSoup(content, 'lxml')

    # ------------------------------------------------------------
    # get file title
    title = "Documentation"
    for h1 in soup.find_all("h1"):
        a = h1.find("a", class_="header")
        if a:                           # keep only h1 that contains <a class="header">
            title = a.get_text(strip=True)
            break

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
    content = content.replace(str_to_replace, str_replacement)

    # ------------------------------------------------------------
    # Safely write the changed content
    with open(filepath, 'w', encoding="utf8") as f:
        f.write(content)

# =========================================================
# entry point
if __name__ == "__main__":

    start = time.time()

    # ------------------------------------------------------------
    # iterate all files, find html files
    file_count = 0
    for filepath in Path(BOOK_ROOT).rglob("*.html"):
        set_thumbnail(str(filepath))
        file_count+=1

    end = time.time()
    print(f"{file_count} thumbnails created in {str(round(end - start, 1))} sec")

    # safe return
    sys.exit(0)