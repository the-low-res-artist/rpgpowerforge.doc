
# =========================================================
# import section
import re 
import sys 
import os 
import time
import shutil
import random
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup

from config import config


# =========================================================
# constant values
BOOK_ROOT = "/home/www-data/rpgpowerforge/book"
CSS_ROOT = "/home/www-data/rpgpowerforge/book/custom-css"
JS_ROOT = "/home/www-data/rpgpowerforge/book/custom-js"
NUMBER_CHAPTER_REGEX = r"(<strong aria-hidden=\"true\">([0-9]+\.)+</strong>)"

# =========================================================
# set css references
def custom_css(filepath, content):

    # add custom .css scripts at the end of the file
    css_links = []

    # -----------------------------------------------------------------
    # iterate all files, find css files
    for css_filepath in Path(CSS_ROOT).rglob("*.css"):

        css_webpath = str(css_filepath).replace(BOOK_ROOT, config.website_root)

        # skip black list css files
        if css_filepath.name in config.css_black_list:
            continue

        # add if in common list
        if css_filepath.name in config.css_common_list:
            css_links.append(f"<link rel=\"stylesheet\" href=\"{css_webpath}\">")

        # also add if the css file has the same name as the current html file
        else:

            html_filename = filepath.stem
            # index and home are the same page
            if html_filename == "index":
                html_filename = "home"

            if css_filepath.stem == html_filename:
                css_links.append(f"<link rel=\"stylesheet\" href=\"{css_webpath}\">")

    str_to_replace = "<!-- Custom theme stylesheets -->"
    str_replacement = "<!-- Custom theme stylesheets -->\n" + '\n'.join(css_links)

    return content.replace(str_to_replace, str_replacement)


# =========================================================
# set js references
def custom_js(filepath, content):

    # add custom .js scripts at the end of the file
    js_links = []

    # -----------------------------------------------------------------
    # iterate all files, find js files
    for js_filepath in Path(JS_ROOT).rglob("*.js"):

        js_webpath = str(js_filepath).replace(BOOK_ROOT, config.website_root)

        # skip black list css files
        if js_filepath.name in config.js_black_list:
            continue

        # add if in common list
        if js_filepath.name in config.js_common_list:
            js_links.append(f"<script src=\"{js_webpath}\" type=\"text/javascript\" charset=\"utf-8\"></script>")

        # also add if the css file has the same name as the current html file
        else:

            html_filename = filepath.stem
            # index and home are the same page
            if html_filename == "index":
                html_filename = "home"

            if js_filepath.stem == html_filename:
                js_links.append(f"<link rel=\"stylesheet\" href=\"{js_webpath}\">")

    str_to_replace = "<!-- Custom JS scripts -->"
    str_replacement = "<!-- Custom JS scripts -->\n" + '\n'.join(js_links)

    return content.replace(str_to_replace, str_replacement)


# =========================================================
# set nav
def nav(content):

    # get the chapters in the nav section
    number_chapters = re.findall(NUMBER_CHAPTER_REGEX, content)

    # remove numbers in chapter title
    for number in number_chapters:
        str_to_replace = number[0] # first element of the regex tuple
        content = content.replace(str_to_replace, "")

    # Patreon nav link
    str_to_replace = "<div> link_patreon</div>"
    str_replacement = f"<a href=\"" + config.md_variables["PATREON_WEBSITE_LINK"] + "\" target=\"_blank\"> Donation (Patreon)</a>"
    content = content.replace(str_to_replace, str_replacement)

    # open the nav for the current page 
    # convert the string to a xml structure
    soup = BeautifulSoup(content, 'lxml')

    # iterate over the xml and add chevron (svg element)
    string_svg = '<svg class="icon nav-svg-rotate-0" viewBox="0 0 512 512" width="20px" height="20px"><path d="M233.4 406.6c12.5 12.5 32.8 12.5 45.3 0l192-192c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L256 338.7 86.6 169.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l192 192z" fill="currentColor"></path></svg>'

    # no nav ? skip
    if (soup.find('nav') == None):
        return content

    all_li = soup.find('nav').find_all('li')
    for li in all_li:
        # (for all li) remove the expanded class if any
        li_classes = li.get('class', [])
        if 'expanded' in li_classes:
            li_classes.remove('expanded')
            li['class'] = li_classes
        # Filter the list items based on the condition (next sibling is also <li> without class)
        sibling_li = li.find_next_sibling('li')
        if sibling_li and len(sibling_li.get('class', [])) == 0:
            # instanciate the svg each tiem to create a deep copy
            li.append(BeautifulSoup(string_svg, 'html.parser').svg)

    # find the <a> element (current page active in nav bar)
    a_element = soup.find('a', class_="active")
    
    # iterate over parents (li elements) and add the class "expanded" to open them
    if a_element:
        # Traverse up to all parent <li> elements and add the 'expanded' class
        parent_li = a_element.find_parent('li')
        while parent_li:
            existing_classes = parent_li.get('class', [])
            # found ("no class" li = current section)
            if len(existing_classes) == 0:
                # get above sibling => li which hold the chevron element (svg)
                # force section open ("expanded" class to li)
                sibling_li = parent_li.find_previous_sibling('li')
                if sibling_li:
                    sibling_li['class'].append('expanded')
                    # force chevron open
                    chevron_svg = sibling_li.find('svg', recursive=False)
                    if chevron_svg:
                        chevron_svg['class'].append('nav-svg-rotate-90')
            # find next parent
            parent_li = parent_li.find_parent('li')

    # convert the html back to a string
    return str(soup)


# =========================================================
# set title icon
def title_icon(content):

    str_to_replace = "<ol class=\"chapter\">"
    str_replacement = f"\
    <div class=\"summary-title-container\">\
      <img src=\"https://rpgpowerforge.com/media/logo/nav-logo.png\" alt=\"product logo\" class=\"nav-logo\">\
      <div class=\"summary-title\">{config.doc_website_title}</div>\
      <div class=\"summary-subtitle\">{config.doc_website_subtitle}</div>\
    </div>\
    <ol class=\"chapter\">"
    
    return content.replace(str_to_replace, str_replacement)


# =========================================================
# set the home page
def home(content):

    str_to_replace = "CARDS_GO_HERE"
    str_replacement = f"<div class=\"cards\">\
            <div class=\"card card1\" onclick=\"window.location.href = 'https://rpgpowerforge.com/doc/installation/installation.html';\" style=\"cursor: pointer;\">\
                <div class=\"card-image\"><img alt=\"Background image of Unity 2022.3\" src=\"https://rpgpowerforge.com/media/home/card_unity.jpg\"></img></div>\
                <div class=\"card-text\"><h3>Installation</h3><p>RPG Power Forge is your powerful Unity package to make RPG without coding. Grab the requirements and start a new project !</p></div>\
            </div>\
            <div class=\"card card2\" onclick=\"window.location.href = 'https://rpgpowerforge.com/doc/getting_started/lets_make_a_game.html';\" style=\"cursor: pointer;\">\
                <div class=\"card-image\"><img alt=\"Image of a pixelart game mockup\" src=\"https://rpgpowerforge.com/media/home/card_getting_started.png\"></img></div>\
                <div class=\"card-text\"><h3>Getting started !</h3><p>Begin your RPG journey with all the online help you need !</p></div>\
            </div>\
            <div class=\"card card3\" onclick=\"window.location.href = '" + config.md_variables["DISCORD_WEBSITE_LINK"] + "';\" style=\"cursor: pointer;\">\
                <div class=\"card-image\"><img alt=\"Image of a chad in front of a computer\" src=\"https://rpgpowerforge.com/media/home/card_community.jpg\"></img></div>\
                <div class=\"card-text\"><h3>Community</h3><p>Join the dev team and users on Discord. We will listen to your feedback and try to improve our product in the right direction !</p></div>\
            </div>\
        </div>"

    return content.replace(str_to_replace, str_replacement)


# =========================================================
# set the devteam page
def devteam(content):

    # prepare cool tags
    tags_gif = ""
    for tag in config.tags_gif:
        # same color for same tag name
        random.seed(hash(tag))
        tags_gif += f"<div class=\"tag\" style=\"background-color:{random.choice(config.tags_colors)}\">{tag}</div>"
    tags_gif = f"<div class=\"tags_container\">{tags_gif}</div>"

    tags_chiw = ""
    for tag in config.tags_chiw:
        random.seed(hash(tag))
        tags_chiw += f"<div class=\"tag\" style=\"background-color:{random.choice(config.tags_colors)}\">{tag}</div>"
    tags_chiw = f"<div class=\"tags_container\">{tags_chiw}</div>"

    tags_noiracide = ""
    for tag in config.tags_noiracide:
        random.seed(hash(tag))
        tags_noiracide += f"<div class=\"tag\" style=\"background-color:{random.choice(config.tags_colors)}\">{tag}</div>"
    tags_noiracide = f"<div class=\"tags_container\">{tags_noiracide}</div>"

    # setup cards
    str_to_replace = "CARDS_GO_HERE"
    str_replacement = f"<div class=\"cards\">\
            <div class=\"card card1\">\
                <div class=\"card-image\"><img src=\"https://rpgpowerforge.com/media/dev_team/card_gif.png\"></img></div>\
                <div class=\"card-text\"><h3>{config.title_gif}</h3>{tags_gif}<p> - <i>{config.description_gif}</i></p></div>\
            </div>\
            <div class=\"card card2\">\
                <div class=\"card-image\"><img src=\"https://rpgpowerforge.com/media/dev_team/card_chiw.png\"></img></div>\
                <div class=\"card-text\"><h3>{config.title_chiw}</h3>{tags_chiw}<p> - <i>{config.description_chiw}</i></p></div>\
            </div>\
            <div class=\"card card3\">\
                <div class=\"card-image\"><img src=\"https://rpgpowerforge.com/media/dev_team/card_noiracide.png\"></img></div>\
                <div class=\"card-text\"><h3>{config.title_noiracide}</h3>{tags_noiracide}<p> - <i>{config.description_noiracide}</i></p></div>\
            </div>\
        </div>"

    return content.replace(str_to_replace, str_replacement)


# =========================================================
# let's make a game page
def lets_make_a_game(content):

    # prepare funny tags
    tags_2d = ""
    for tag in config.tags_2d:
        tags_2d += f"<div class=\"tag\" style=\"background-color:ForestGreen\">{tag}</div>"
    tags_2d = f"<div class=\"tags_container\">{tags_2d}</div>"

    tags_3d = ""
    for tag in config.tags_3d:
        tags_3d += f"<div class=\"tag\" style=\"background-color:Chocolate\">{tag}</div>"
    tags_3d = f"<div class=\"tags_container\">{tags_3d}</div>"

    tags_4d = ""
    for tag in config.tags_4d:
        tags_4d += f"<div class=\"tag\" style=\"background-color:Crimson\">{tag}</div>"
    tags_4d = f"<div class=\"tags_container\">{tags_4d}</div>"

    # setup cards
    str_to_replace = "CARDS_GO_HERE"
    str_replacement = f"<div class=\"cards\">\
            <div class=\"card card1\" onclick=\"window.location.href = 'https://cursoreffects.com/';\" style=\"cursor: pointer;\">\
                <div class=\"card-image\"><img src=\"https://rpgpowerforge.com/media/lets_make_a_game/card_2d.png\"></img></div>\
                <div class=\"card-text\"><h3>{config.title_2d}</h3>{tags_2d}<p>{config.description_2d}</p></div>\
            </div>\
            <div class=\"card card2\" onclick=\"window.location.href = 'https://jacksonpollock.org/';\" style=\"cursor: pointer;\">\
                <div class=\"card-image\"><img src=\"https://rpgpowerforge.com/media/lets_make_a_game/card_3d.png\"></img></div>\
                <div class=\"card-text\"><h3>{config.title_3d}</h3>{tags_3d}<p>{config.description_3d}</p></div>\
            </div>\
            <div class=\"card card3\" onclick=\"window.location.href = 'https://burymewithmymoney.com/';\" style=\"cursor: pointer;\">\
                <div class=\"card-image\"><img src=\"https://rpgpowerforge.com/media/lets_make_a_game/card_4d.png\"></img></div>\
                <div class=\"card-text\"><h3>{config.title_4d}</h3>{tags_4d}<p>{config.description_4d}</p></div>\
            </div>\
        </div>"

    return content.replace(str_to_replace, str_replacement)


# =========================================================
# set installation page
def installation(content):

    # prepare funny tags
    tags_install_unity = ""
    for tag in config.tags_install_unity:
        tags_install_unity += f"<div class=\"tag\" style=\"background-color:SlateBlue\">{tag}</div>"
    tags_install_unity = f"<div class=\"tags_container\">{tags_install_unity}</div>"

    tags_dl_rpgpowerforge = ""
    for tag in config.tags_dl_rpgpowerforge:
        tags_dl_rpgpowerforge += f"<div class=\"tag\" style=\"background-color:RoyalBlue\">{tag}</div>"
    tags_dl_rpgpowerforge = f"<div class=\"tags_container\">{tags_dl_rpgpowerforge}</div>"

    tags_create_project = ""
    for tag in config.tags_create_project:
        tags_create_project += f"<div class=\"tag\" style=\"background-color:DodgerBlue\">{tag}</div>"
    tags_create_project = f"<div class=\"tags_container\">{tags_create_project}</div>"

    # setup cards
    str_to_replace = "CARDS_GO_HERE"
    str_replacement = f"<div class=\"cards\">\
            <div class=\"card card1\" onclick=\"window.location.href = 'https://rpgpowerforge.com/doc/installation/installation_unity.html';\" style=\"cursor: pointer;\">\
                <div class=\"card-image\"><img src=\"https://rpgpowerforge.com/media/installation/card_unity.png\"></img></div>\
                <div class=\"card-text\"><h3>{config.title_install_unity}</h3>{tags_install_unity}<p>{config.description_install_unity}</p></div>\
            </div>\
            <div class=\"card card2\" onclick=\"window.location.href = 'https://rpgpowerforge.com/doc/installation/download_rpg_power_forge.html';\" style=\"cursor: pointer;\">\
                <div class=\"card-image\"><img src=\"https://rpgpowerforge.com/media/installation/card_rpf.png\"></img></div>\
                <div class=\"card-text\"><h3>{config.title_dl_rpgpowerforge}</h3>{tags_dl_rpgpowerforge}<p>{config.description_dl_rpgpowerforge}</p></div>\
            </div>\
            <div class=\"card card3\" onclick=\"window.location.href = 'https://rpgpowerforge.com/doc/installation/create_new_project.html';\" style=\"cursor: pointer;\">\
                <div class=\"card-image\"><img src=\"https://rpgpowerforge.com/media/installation/card_new_project.png\"></img></div>\
                <div class=\"card-text\"><h3>{config.title_create_project}</h3>{tags_create_project}<p>{config.description_create_project}</p></div>\
            </div>\
        </div>"

    return content.replace(str_to_replace, str_replacement)


# =========================================================
# set footer section
def footer(content):

    links=[
        {
            "href":config.md_variables["PATREON_WEBSITE_LINK"],
            "img":"footer/patreon.png",
            "alt":"Patreon link"
        },
        {
            "href":config.md_variables["TWITTER_WEBSITE_LINK"],
            "img":"footer/x.png",
            "alt":"X/Twitter link"
        },
        {
            "href":config.md_variables["YOUTUBE_WEBSITE_LINK"],
            "img":"footer/youtube.png",
            "alt":"Youtube link"
        },
    ]

    list_links = []
    for link in links:
        l = f"<div class=\"footer-link\">\
          <a href=\"" + link["href"] + "\" target=\"_blank\"><img src=\"https://rpgpowerforge.com/media/" + link["img"] + "\" alt=\"" + link["alt"] + "\" /></a>\
        </div>"
        list_links.append(l)
    html_links = ' '.join(list_links)

    footer=f"<p>{html_links}</p>\
    <p>Copyright © {datetime.now().year} - {datetime.now().year + 1} RPG Power Forge<br>\
    \"RPG Power Forge\" is a trademark.<br>\
    Other names or brands are trademarks of their respective owners.</p>\
    <p>Last update : {datetime.now().strftime(f'%A %d %B %Y')}</p>"

    str_to_replace="</main>"
    str_replacement=f"</main><div class=\"footer-container\"><div class=\"footer-text\">{footer}</div></div>"

    return content.replace(str_to_replace, str_replacement)


# =========================================================
# set back to hero page
def header(content):

    # init
    svg = "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"-50 0 512 512\" width=\"20\" height=\"20\"><!--!Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path fill=\"#ffffff\" d=\"M438.6 278.6c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L338.8 224 32 224c-17.7 0-32 14.3-32 32s14.3 32 32 32l306.7 0L233.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l160-160z\"/></svg>"

    # update the top bar section
    str_to_replace = "<h1 class=\"menu-title\">RPG Power Forge</h1>"
    str_replacement = f"<h1 class=\"menu-title\"><a href=\"https://rpgpowerforge.com\">RPG Power Forge</a></h1><div class=\"join-community-container\"><div class=\"join-community-text\"><a href=\"" + config.md_variables["PATREON_WEBSITE_LINK"] + f"\" target=\"_blank\">{svg}&nbsp;&nbsp;&nbsp;Get Early Access&nbsp;&nbsp;&nbsp;{svg}</a></div></div>"
    
    return content.replace(str_to_replace, str_replacement) 

# =========================================================
# set media src path absolute
def media_path(content):

    # init
    soup = BeautifulSoup(content, "lxml")
    pattern = re.compile(r'^(?:\./|\.\./)+')

    # Update all <img> tags
    for img in soup.find_all("img"):
        src = img.get("src")
        if src and not config.website_root in src:
            cleaned_src = pattern.sub("", src)  # remove leading relative paths
            img["src"] = config.website_root + "/" + cleaned_src.lstrip("/")

    return str(soup)


# =========================================================
# set devlogs
def devlogs(content):

    # init
    str_to_replace = "DEVLOGS_GO_HERE"
    str_replacement = ""

    devlog_id = 1
    for dev in config.devlogs:
        title = dev["title"]
        src = dev["iframe_src"]
        devlog_str = f"<h3>Devlog #{devlog_id} : {title}</h3>\n<iframe width=\"100%\" height=\"400\" src=\"{src}\" title=\"YouTube video player\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share\" referrerpolicy=\"strict-origin-when-cross-origin\" allowfullscreen></iframe>\n"       
        str_replacement = f"{str_replacement}\n{devlog_str}"
        devlog_id += 1

    return content.replace(str_to_replace, str_replacement)


# =========================================================
# set devlogs
def favicon():

    # update the favicon file
    for ext in ["png", "svg"]:
        src = f"{BOOK_ROOT}/media/icons/32x32.{ext}"
        dst = f"{BOOK_ROOT}/doc/favicon.{ext}"
        shutil.copy(src, dst)

# =========================================================
# entry point
def main():
    
    # -----------------------------------------------------------------
    # init
    start = time.time()

    # -----------------------------------------------------------------
    # try to run all pre build functions
    try:
        
        # -----------------------------------------------------------------
        # iterate all files, find html files
        file_count = 0
        for filepath in Path(BOOK_ROOT).rglob("*.html"):
                    
            # -----------------------------------------------------------------
            # html file !
            file_count += 1
            content = ""
            with open(filepath, 'r', encoding="utf8") as f:
                content = f.read()

            # -----------------------------------------------------------------
            # general settings
            content = custom_css(filepath, content)
            content = custom_js(filepath, content)
            content = nav(content)
            content = title_icon(content)
            content = footer(content)
            content = header(content)
            content = media_path(content)
            favicon()
            
            # -----------------------------------------------------------------
            # name specific settings
            if (filepath.name == "home.html" or filepath.name == "index.html"): content = home(content)
            if (filepath.name == "devteam.html"): content = devteam(content)
            if (filepath.name == "lets_make_a_game.html"): content = lets_make_a_game(content)
            if (filepath.name == "installation.html"): content = installation(content)
            if (filepath.name == "devlogs.html"): content = devlogs(content)

            # -----------------------------------------------------------------                    
            # Save the updated content
            with open(filepath, 'w', encoding="utf8") as f:
                f.write(content)

            # update the roadmap page
            #python3 -m roadmap.py || true
            # update features progress
            #python3 -m features.py || true


    except Exception as e:
        print(e)

    finally:
        # duration & exit
        end = time.time()
        print(f"{file_count} files updated in {str(round(end - start, 1))} sec")
        return 0

# =========================================================
# entry point
if __name__ == "__main__":
    sys.exit(main())
