import urllib2
from bs4 import BeautifulSoup
import re
from datetime import datetime
from models import Circular, Item


class Scraper:
    def __init__(self, link):
        self.link = link

    @staticmethod
    def read_page(link):
        return BeautifulSoup(urllib2.urlopen(link))

    def scrape_category_data(self):
        category_page = self.read_page(self.link)
        c = Circular()
        c.store = "Shop Rite Newton"
        c.start = datetime.now()
        c.end = datetime.now()
        for link in self.find_tag(category_page, "a"):
            #Rework to a less hard coded method maybe use a try to catch execptions
            if len(link.contents) > 1:
                contents = BeautifulSoup(link.contents[1]).prettify()
                category_link = re.search(r'href="(.+Categories.+)"', str(link)).group(1)
                category_name = re.search(r'alt="(.+)" class', contents).group(1)
                Scraper.read_category(category_link, category_name)

    @staticmethod
    def find_tag(page, tag):
        return page.find_all(tag)

    @staticmethod
    def create_item(list_item, cat_name):
        new_item = Item()
        new_item.name = list_item.find_all("h3", {"class": "circular-item-title"})[0].contents[0]
        new_item.category = cat_name
        new_item.price = list_item.find_all("h4", {"class": "circular-item-price"})[0].contents[0]
        new_item.save()

    @staticmethod
    def read_category(category_link, category_name):
        page = Scraper.read_page(category_link)
        for li in Scraper.find_tag(page, "li"):
            Scraper.create_item(li, category_name)
        next_page = page.find_all("a", {"data-role": "button"})[0].get("href")

