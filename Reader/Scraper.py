import urllib2
from bs4 import BeautifulSoup  # , UnicodeDammit
from datetime import datetime
from models import Circular, Item, Store
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

    @staticmethod
    def get_store_info(page):
        temp = []
        info = {}
        for a in page.find_all("div", {"id": "RegionStore"}):
            info['name'] = a.find("h1").contents
            # Find a better way to get store address, locale and phone number
            for h2 in a.find("h2").contents:
                h2 = ''.join(h2).split()
                if h2:
                    temp.append(" ".join(h2))
        info['address'] = temp[0]
        info['locale'] = temp[1]
        info['phone_number'] = temp[2]
        return info

    @staticmethod
    def create_store(store_info):
        s = Store()
        s.name = store_info['name']
        s.locale = store_info['locale']
        s.address = store_info['address']
        s.phone_number = store_info['phone_number']
        s.save()
        return s

    @staticmethod
    def create_circular(s, circular_info):
        c = Circular()
        c.store = s
        c.start = c.end = datetime.now()
        c.save()
        return c

    def scrape_category_data(self):
        category_page = self.read_page(Scraper.full_url(self.link))
        s = Scraper.create_store(Scraper.get_store_info(category_page))
        c = Scraper.create_circular(s, "")
        print "Store id: " + str(s.pk)
        print "Circular id: " + str(c.pk)
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
        return i

    @staticmethod
    def read_category(link, name):
        page = Scraper.read_page(link)
        # Grab div for inventory items and pass to Item creator
        for div in Scraper.find_tag(page, "div", "class", "grid-item"):
            i = Scraper.create_item(div, name)
            print "Item id: " + str(i.pk)
        # Check for additional pages
        for a in Scraper.find_tag(page, "a", "title", "Next Page"):
            n_page = Scraper.full_url(a.get("href"))
            if n_page == link:
                return True
            else:
                return Scraper.read_category(n_page, name)