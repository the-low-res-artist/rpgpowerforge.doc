
# =========================================================
# website configuration
from config import config


# =========================================================
# constant values
SRC_ROOT = "/home/www-data/rpgpowerforge/src/"


# =========================================================
# set the hall of fame
def hall_of_fame(content):

    # init
    str_to_replace = "SUPPORTER_LIST_GOES_HERE"
    list_replacement = []
    supporters = sorted(config.supporters, key=lambda d: d['name'])

    # compute hall of fame
    for sup in supporters:
        name = sup["name"]
        sub_str = f"* **{name}**"
        if "link" in sup:
            link = sup["link"]
            link_text = link.replace("http://", "").replace("https://", "")
            sub_str = f"{sub_str} : [{link_text}]({link})"
        list_replacement.add(sub_str)

    str_replacement = "\n".join(list_replacement)
    return content.replace(str_to_replace, str_replacement)


# =========================================================
# set external links
def external_links(filepath, content):

    # init
    str_to_replace = "(link_patreon)"
    str_replacement = f"({config.link_patreon})"

    return content.replace(str_to_replace, str_replacement)


# =========================================================
# set glossary terms
def glossary(filepath, content):

    # find all matches
    matches = re.findall(config.glossary_regex, s)

    # safe exit
    if (len(matches) == 0):
        return

    for match in matches:
        str_to_replace=match[0]
        word=match[1]
        glossary_entry=word.lower()
        str_replacement="[<span style=\"color:" + config.glossary_color + "\">" + word + "</span>][" + glossary_entry + "]"
        content = content.replace(str_to_replace, str_replacement)

    # create the glossary file next to filename (if not yet)
    glossary_filepath = os.path.dirname(filepath) + "/glossary.md"
    if not os.path.isfile(glossary_filepath):
        # create the glossary file at this location
        with open(glossary_filepath, 'w', encoding="utf8") as f:
            for entry in config.glossary_list:
                for key in entry:
                    # line sample : [pivot]: ## "A point placed on a sprite or prefab"
                    line = f'[{key}]: ## \"{entry[key]}\"\n'
                    f.write(line)

    # add the glossary file
    return content + '\n\n{{#include glossary.md}}'


# =========================================================
# set variables
def variables(content):

    for key, value in config.md_variables.items():
        str_to_replace = key
        str_replacement = value
        content = content.replace(str_to_replace, str_replacement)

    return content


# =========================================================
# set the page summary
def summary(content):

    # search titles (example : '## Create a project on itchio')
    summary = ""
    with open(filename, 'r', encoding="utf8") as f:
        for line in f.readlines():
            # remove last \n
            line=line[:-1]
            # skip summary itself
            if (line == "## Summary"):
                continue
            # initialisation
            title=""
            offset=0
            # test title
            if line.startswith("## "):
                title=line[3:]
            if line.startswith("### "):
                title=line[4:]
                offset=4
            if line.startswith("#### "):
                title=line[5:]
                offset=8
            # append title (if found)
            if (len(title) > 0):
                link=title.lower().replace(" ","-").replace("(","").replace(")","")
                summary += ' '*offset + f"- [{title}](#{link})\n"

    # update summary (if found)
    if (len(summary) > 0):
        str_to_replace = '## Summary'
        str_replacement = '## Summary\n' + summary
        content = content.replace(str_to_replace, str_replacement)

    return content


# =========================================================
# highlight terms (bold)
def highlight_terms(content):

    for term in config.highlight_terms:
        pattern=term
        str_replacement=f"**{term}**"
        content = re.sub('pattern', str_replacement, content)

    return content


# =========================================================
# highlight actions (underline)
def highlight_actions(content):

    # find all matches
    matches = re.findall(config.action_regex, s)

    # safe exit
    if (len(matches) == 0):
        return

    for match in matches:
        str_to_replace=match[0]
        action=match[1]
        str_replacement=f"<span style=\"text-decoration: underline;\">{action}</span>"
        content = content.replace(str_to_replace, str_replacement)

    return content


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
        # iterate all files, find md files
        for root, dirs, files in os.walk(SRC_ROOT, topdown=False):
            for filename in files:
                if filename.endswith(".md"):
                    
                    # -----------------------------------------------------------------
                    # md file !
                    filepath = os.path.join(root, filename)
                    content = ""
                    with open(filename, 'r', encoding="utf8") as f:
                        content = f.read()

                    # -----------------------------------------------------------------
                    # general settings
                    content = external_links(content)
                    content = glossary(filepath, content)
                    content = variables(content)
                    content = highlight_terms(content)
                    content = highlight_actions(content)
                    content = summary(content)

                    # -----------------------------------------------------------------
                    # name specific settings
                    if (filename == "hall_of_fame.md"): content = hall_of_fame(content)

                    # -----------------------------------------------------------------                    
                    # Save the updated content
                    with open(filepath, 'w', encoding="utf8") as f:
                        f.write(s)

    except Exception as e:
        pass

    finally:
        # duration & exit
        end = time.time()
        print(f"Script duration : {str(round(end - start, 1))} sec")
        return 0

# =========================================================
# entry point
if __name__ == "__main__":
    sys.exit(main())













import re # regex operations
import sys # to return 0
import os # loop over files
from config import config
import time # measure duration

# goal : ???

# replace in a file
def set_???(filename):

    # Safely read the input filename using 'with'
    s= ""
    with open(filename, 'r', encoding="utf8") as f:
        s = f.read()

    # safe exit
    if (s == ""):
        return

    str_to_replace = ""
    str_replacement = ""
    s = s.replace(str_to_replace, str_replacement)


    # Safely write the changed content
    with open(filename, 'w', encoding="utf8") as f:
        f.write(s)


# entry point
start = time.time()
src_root = "./../src/" ???
nb_files=0
for root, dirs, files in os.walk(src_root, topdown=False):
   for filename in files:
        if filename.endswith(".md"): ???
            set_???(os.path.join(root, filename))
            nb_files+=1

end = time.time()
print(f"[{str(round(end - start, 1))} sec] ??? UPDATE : {nb_files} updated")

# safe return
sys.exit(0)