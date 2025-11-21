
# =========================================================
# import section
import re 
import sys 
import os 
import time
import shutil
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

            # -----------------------------------------------------------------
            # name specific settings
            #if (filepath.name == "xxx.html"): content = yyy(content)

            # -----------------------------------------------------------------                    
            # Save the updated content
            with open(filepath, 'w', encoding="utf8") as f:
                f.write(content)

            # update the navigation summary
            #python3 -m nav-summary.py || true
            ## update summary title and subtitle
            #python3 -m summary_title.py || true
            # fix link format (remove '.html' endings for external links) on each book/**/*.html page generated by mdbook
            #python3 -m link.py  || true # must be after rating to prevent the top title to have a subtitle "user find this page useful !"
            # update the home page
            #python3 -m home.py || true
            # update the dev team page
            #python3 -m devteam.py || true
            # update the roadmap page
            #python3 -m roadmap.py || true
            # update lets make a game page
            #python3 -m lets_make_a_game.py || true
            # update installation page
            #python3 -m installation.py || true
            # update rpg power forge overview page
            #python3 -m overview.py || true
            # update the footer part
            #python3 -m footer.py || true
            # update community join button
            #python3 -m join-community.py || true
            # update devlog embedded videos
            #python3 -m devlogs.py || true
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
