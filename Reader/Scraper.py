import urllib2
from bs4 import BeautifulSoup  # , UnicodeDammit
from datetime import datetime
from models import Circular, Item
import stringformatter as fmt


class Scraper:
    def __init__(self, url):
        self.link = url  # url for Categories page of store
        
    @staticmethod
    def full_url(link):
        return "http://plan.shoprite.com" + link
    
    @staticmethod
    def read_page(link):
        req = urllib2.Request(link)
        req.add_header('User-agent', 'Mozilla/5.0')

        return BeautifulSoup(urllib2.urlopen(req).read())

    def scrape_category_data(self):
        category_page = self.read_page(Scraper.full_url(self.link))
        c = Circular()
        # c.store = "Shop Rite Newton"
        c.start = c.end = datetime.now()
        for link in self.find_tag(category_page, "a", "data-clientanalyticsaction", "Circular Categories"):
            cat_link = link.get("href")
            cat_name = link.get("data-clientanalyticslabel")
            cat_name = cat_name[:cat_name.rfind(" - ")]
            Scraper.read_category(Scraper.full_url(cat_link), cat_name)

    @staticmethod
    def find_tag(page, tag, var=None, val=None):
        if var and val:
            return page.find_all(tag, {var: val})
        else:
            return page.find_all(tag)

    @staticmethod
    def create_item(div, name):
        i = Item()
        i.name = fmt.convert(div.find("h2").contents)
        i.price = fmt.convert(div.find("p").contents)
        i.category = name
        i.save()

    @staticmethod
    def read_category(link, name):
        page = Scraper.read_page(link)
        # Grab div for inventory items and pass to Item creator
        for div in Scraper.find_tag(page, "div", "class", "grid-item"):
            Scraper.create_item(div, name)
        # Check for additional pages
        for a in Scraper.find_tag(page, "a", "title", "Next Page"):
            n_page = Scraper.full_url(a.get("href"))
            if n_page == link:
                return True
            else:
                return Scraper.read_category(n_page, name)