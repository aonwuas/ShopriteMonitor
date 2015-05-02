import urllib2
from bs4 import BeautifulSoup
from datetime import datetime
from models import Circular, Item


class Scraper:
    def __init__(self, url):
        self.link = url  # url for Categories page of store
        self.base_url = "http://plan.shoprite.com"
        
    @staticmethod
    def full_url(link):
        return "http://plan.shoprite.com" + link
    
    @staticmethod
    def read_page(link):
        req = urllib2.Request(Scraper.full_url(link))
        req.add_header('User-agent', 'Mozilla/5.0')
        return BeautifulSoup(urllib2.urlopen(req).read())

    def scrape_category_data(self):
        category_page = self.read_page(Scraper.full_url(self.link))
        c = Circular()
        c.store = "Shop Rite Newton"
        c.start = c.end = datetime.now()
        for link in self.find_tag(category_page, "a", "data-clientanalyticsaction", "Circular Categories"):
            cat_link = link.get("href")
            cat_name = link.get("data-clientanalyticslabel")
            cat_name = cat_name[:cat_name.rfind(" - ")]
            Scraper.read_category(cat_link, cat_name)

    @staticmethod
    def find_tag(page, tag, var=None, val=None):
        if var and val:
            return page.find_all(tag, {var: val})
        else:
            return page.find_all(tag)

    @staticmethod
    def create_item(list_item, cat_name):
        new_item = Item()
        new_item.name = list_item.find_all("h3", {"class": "circular-item-title"})[0].contents[0]
        new_item.category = cat_name
        new_item.price = list_item.find_all("h4", {"class": "circular-item-price"})[0].contents[0]
        new_item.save()

    @staticmethod
    def read_category(link, name):
        page = Scraper.read_page(link)
        for li in Scraper.find_tag(page, "li"):
            Scraper.create_item(li, name)
        next_page = page.find_all("a", {"data-role": "button"})[0].get("href")