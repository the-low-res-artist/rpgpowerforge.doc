
import re
import sys
import os
import datetime 
from pathlib import Path

from config import config


# =========================================================
# constant values
BOOK_ROOT = "/home/www-data/rpgpowerforge/book"


# =========================================================
class Url:
    def __init__(self, loc):
        self.loc = loc
        self.lastmod = datetime.datetime.now().strftime("%Y-%m-%d")
        self.changefreq = "weeekly"
        self.priority = "0.5"
    
    def get_sitemap(self):
        return f"""
<url>
    <loc>{self.loc}</loc>
    <lastmod>{self.lastmod}</lastmod>
    <changefreq>{self.changefreq}</changefreq>
    <priority>{self.priority}</priority>
</url>"""

# =========================================================
class Urlset:
    def __init__(self):
        self.urls = []

    def get_sitemap(self):
        sitemap = "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">"
        for url in self.urls:
            sitemap += url.get_sitemap()
        sitemap += "\n</urlset>"
        return sitemap

# =========================================================
class Xml:
    def __init__(self):
        self.urlset = Urlset()

    def crawl(self, website_root):
        # Walk through the directory structure
        for path in Path(website_root).rglob("*.html"):
            # Get the full path of the HTML file
            path = str(path).replace(website_root, "https://rpgpowerforge.com")
            self.urlset.urls.append(Url(path))

    def get_sitemap(self):
        sitemap = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        sitemap += self.urlset.get_sitemap()
        return sitemap

# =========================================================
class Sitemap:
    def __init__(self):
        self.xml = Xml()
    
    def crawl(self, website_root):
        self.xml.crawl(website_root)

    def write(self, sitemap_filepath):
        with open(sitemap_filepath, 'w', encoding="utf8") as f:
            f.write(self.xml.get_sitemap())

# =========================================================
# generate the sitemap file
def generate_sitemap(website_root, sitemap_filepath):
    sitemap = Sitemap()
    sitemap.crawl(website_root)
    sitemap.write(sitemap_filepath)


# =========================================================
# entry point
if __name__ == "__main__":
    generate_sitemap(BOOK_ROOT, f"{BOOK_ROOT}/sitemap.xml")
    sys.exit(0)