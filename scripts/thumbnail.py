import re # regex operations
import sys # to return 0
import os # loop over files
import shutil # move files
from PIL import ImageFont, ImageDraw, Image
import time # measure duration

# goal : add a nice thumbnail to html output pages

# slip evenly a sentence string (for title)
def split_string_equally(input_string):
    total_chars = len(input_string)
    half_chars = total_chars // 2

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

# add a cool title to the thumbnail
def get_new_thumbnail_image(filename, title, file_template):
    basename = os.path.basename(filename)
    
    # open template image
    with Image.open(file_template) as image:

        # get the image
        draw = ImageDraw.Draw(image)

        # text to draw
        subtitle = "User manual"

        # create 2 fonts
        font_title = ImageFont.truetype("./../resources/mont.otf", 110)
        font_subtitle = ImageFont.truetype("./../resources/mont.otf", 50)
        front_color = (255, 255, 255, 255)
        back_color = (0, 0, 0, 255)

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
            
        # save
        output_filename = str(hash(title))
        thumbnail_path = f"./../media/thumbnail/thumbnail_{output_filename}.jpg"
        image.save(thumbnail_path)

    return thumbnail_path.replace("./../", "https://rpgpowerforge.com/")

# replace in a file
def set_thumbnail(filename):

    # Safely read the input filename using 'with'
    s= ""
    with open(filename, 'r', encoding="utf8") as f:
        s = f.read()

    # safe exit
    if (s == ""):
        return

    # get file title
    titles = re.findall("<h1.+?><a.+?>(.+?)</a>", s)
    if len(titles) > 0:
        title = titles[0].replace("<strong>", "").replace("</strong>", "")
    else:
        title = "Documentation"

    file_url=filename.replace('./../book/', 'https://rpgpowerforge.com/')
    description="The awesome documentation for the Unity package : RPG Power Forge"
    image= get_new_thumbnail_image(filename, title, "./../media/thumbnail/thumbnail_template.png")
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

    # Safely write the changed content
    with open(filename, 'w', encoding="utf8") as f:
        f.write(s)

# entry point
start = time.time()
book_root = "./../book/"
nb_files=0
for root, dirs, files in os.walk(book_root, topdown=False):
   for filename in files:
        if filename.endswith(".html"):
            set_thumbnail(os.path.join(root, filename))
            nb_files+=1

end = time.time()
print(f"[{str(round(end - start, 1))} sec] THUMBNAILS UPDATE : {nb_files} updated")

# safe return
sys.exit(0)