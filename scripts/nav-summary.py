import re # regex operations
import sys # to return 0
import os # loop over files
import shutil # move files
import time # measure duration
from bs4 import BeautifulSoup # manage html file to add/remove classes to elements

# goal : update the navigation summary on each html page

# replace in a file
def set_nav_summary(filename):
    
    # define regex
    NUMBER_CHAPTER_REGEX = r"(<strong aria-hidden=\"true\">([0-9]+\.)+</strong>)"
    
    # Safely read the input filename using 'with'
    s= ""
    with open(filename, 'r', encoding="utf8") as f:
        s = f.read()

    # safe exit
    if (s == ""):
        return

    # get the chapters in the nav section
    number_chapters = re.findall(NUMBER_CHAPTER_REGEX, s)
    # remove numbers in chapter title
    for number in number_chapters:
        str_to_replace = number[0] # first element of the regex tuple
        str_replacement = ""
        s = s.replace(str_to_replace, str_replacement)

    # open the nav for the current page 
    # convert the string to a xml structure
    soup = BeautifulSoup(s, 'lxml')

    # iterate over the xml and add chevron (svg element)
    string_svg = '<svg class="icon nav-svg-rotate-0" viewBox="0 0 512 512" width="20px" height="20px"><path d="M233.4 406.6c12.5 12.5 32.8 12.5 45.3 0l192-192c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L256 338.7 86.6 169.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l192 192z" fill="currentColor"></path></svg>'

    all_li = soup.find('nav').find_all('li')
    for li in all_li:
        # (for all li) remove the expanded class if any
        li_classes = li.get('class', [])
        if 'expanded' in li_classes:
            li_classes.remove('expanded')
            li['class'] = li_classes
        # Filter the list items based on the condition (next sibling is also <li> without class)
        sigling_li = li.find_next_sibling('li')
        if sigling_li and len(sigling_li.get('class', [])) == 0:
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
                sigling_li = parent_li.find_previous_sibling('li')
                if sigling_li:
                    sigling_li['class'].append('expanded')
                    # force chevron open
                    chevron_svg = sigling_li.find('svg', recursive=False)
                    if chevron_svg:
                        chevron_svg['class'].append('nav-svg-rotate-90')
            # find next parent
            parent_li = parent_li.find_parent('li')

    # convert the html back to a string
    s = str(soup)

    # Safely write the changed content
    with open(filename, 'w', encoding="utf8") as f:
        f.write(''.join(s))

# entry point
start = time.time()
book_root = "./../book/"
nb_files=0
for root, dirs, files in os.walk(book_root, topdown=False):
   for filename in files:
        if filename.endswith(".html"):
            set_nav_summary(os.path.join(root, filename))
            nb_files+=1

end = time.time()
print(f"[{str(round(end - start, 1))} sec] NAV SUMMARY UPDATE : {nb_files} updated")

# safe return
sys.exit(0)