
# =========================================================
# import section
import re 
import sys 
import os 
import time
import json
import requests
from pathlib import Path

from config import config


# =========================================================
# constant values
SRC_ROOT = "/home/www-data/rpgpowerforge/src/"
PATREON_API_BASE_URL = "https://www.patreon.com/api/oauth2/v2"
PATREON_CAMPAIGN_ID = "12005895"
ACCESS_TOKEN = "_YNczPWoKiY4-tXsfexmqACPX7iTSBjPX8Uwa2eH1Kk"

# =========================================================
# set the hall of fame
def hall_of_fame(content):

    # -------------------------------------------------------------
    # compute special thanks
    str_to_replace = "SPECIAL_THANKS_LIST_GOES_HERE"
    list_replacement = []
    for sup in config.special_thanks:
        name = sup["name"]
        link = sup["link"]
        comment = sup["comment"]
        list_replacement.append(f"* **{name}**, {comment}\n    * contact : [{link}](https://{link})")

    str_replacement = "\n".join(list_replacement)
    content = content.replace(str_to_replace, str_replacement)

    # -------------------------------------------------------------
    # contact Patreon 
    include = "pledge_history&fields%5Bmember%5D=full_name"
    token = os.getenv("PATREON_ACCESS_TOKEN_ALL_OF_FAME")
    url = f"{PATREON_API_BASE_URL}/campaigns/{PATREON_CAMPAIGN_ID}/members?include={include}"
    headers = { "Authorization": f"Bearer {ACCESS_TOKEN}" }

    all_members = []
    all_events = []

    # results are received by page
    while url:
        print("Fetching:", url)
        resp = requests.get(url, headers=headers)
        data = resp.json()

        # Merge data
        all_members.extend(data.get("data", []))
        all_events.extend(data.get("included", []))

        # Check for next page
        url = data.get("links", {}).get("next")

    # -------------------------------------------------------------
    # success ? great
    if (len(all_members) > 0 and len(all_events) > 0):
        
        # compute json data
        event_map = {e["id"]: e["attributes"] for e in all_events}
        supporters = []

        for m in all_members:
            name = m["attributes"]["full_name"]

            event_list = m["relationships"]["pledge_history"]["data"]
            total_cents = 0
            payments = []

            for e in event_list:
                event_id = e["id"]
                if event_id not in event_map:
                    continue

                ev = event_map[event_id]

                # Keep only truly paid events
                if ev.get("payment_status") == "Paid":
                    payments.append(ev)

            # Sum total paid
            for ev in payments:
                amount = ev["amount_cents"]
                currency = ev["currency_code"]
                total_cents += amount

            if total_cents > 0:
                supporters.append({
                    "name": name,
                    "total_cents": total_cents,
                    "total_usd": total_cents / 100.0
                })

        supporters_sorted = sorted(supporters, key=lambda x: x["total_cents"], reverse=True)
        for s in supporters_sorted:
            print(f"{s['name']:<25}  ${s['total_usd']:.2f}")

        # -------------------------------------------------------------
        # compute top supporters
        str_to_replace = "TOP_SUPPORTERS_LIST_GOES_HERE"
        list_replacement = []
        for sup in supporters_sorted[:10]:
            name = sup["name"]
            sub_str = f"* **{name}**"
            list_replacement.append(sub_str)

        str_replacement = "\n".join(list_replacement)
        content = content.replace(str_to_replace, str_replacement)

        # -------------------------------------------------------------
        # compute supporters
        str_to_replace = "SPECIAL_THANKS_LIST_GOES_HERE"
        list_replacement = []
        for sup in supporters_sorted[:10]:
            list_replacement.append(sup["name"])

        str_replacement = ", ".join(list_replacement)
        content = content.replace(str_to_replace, str_replacement)

    return content


# =========================================================
# set external links
def external_links(content):

    # init
    str_to_replace = "(link_patreon)"
    str_replacement = f"(" + config.md_variables["PATREON_WEBSITE_LINK"] + ")"

    return content.replace(str_to_replace, str_replacement)


# =========================================================
# set glossary terms
def glossary(filepath, content):

    # find all matches
    matches = re.findall(config.glossary_regex, content)

    # safe exit
    if (len(matches) == 0):
        return content

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
    for line in content.splitlines():
        
        # skip summary itself
        if (line == "## Summary"):
            continue
        
        # initialisation
        title=""
        offset=0
        
        # test title line
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
            summary += ' ' * offset + f"- [{title}](#{link})\n"

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
    matches = re.findall(config.action_regex, content)

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
        file_count = 0
        for filepath in Path(SRC_ROOT).rglob("*.md"):
                    
            # -----------------------------------------------------------------
            # md file !
            file_count += 1
            content = ""
            with open(filepath, 'r', encoding="utf8") as f:
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
            if (filepath.name == "hall_of_fame.md"): content = hall_of_fame(content)

            # -----------------------------------------------------------------                    
            # Save the updated content
            with open(filepath, 'w', encoding="utf8") as f:
                f.write(content)

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
