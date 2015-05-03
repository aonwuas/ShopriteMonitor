import urllib2
from bs4 import BeautifulSoup  # , UnicodeDammit
from models import Circular, Item, Store
import stringformatter as fmt


class Scraper:
    def __init__(self, url):
        self.link = url  # url for Categories page of store

    def scrape_category_data(self):
        print "Getting category names and links"
        category_page = read_page(full_url(self.link))
        s = create_store(get_store_info(category_page))
        c = create_circular(s, get_circular_dates(category_page))
        print "Iterating over categories:"
        for link in find_tag(category_page, "a", "data-clientanalyticsaction", "Circular Categories"):
            cat_link = link.get("href")
            cat_name = link.get("data-clientanalyticslabel")
            cat_name = cat_name[:cat_name.rfind(" - ")]
            if cat_name != "Store Services":
                print "   " + cat_name
                read_category(full_url(cat_link), cat_name, c)
        print "Finished scraping circular"


def get_circular_dates(page):
    for a in page.find_all("a", {"class": "megadrop-circular-name"}):
        tag = a.get("data-clientanalyticslabel")
        if tag[:tag.find(" - ")] == "Weekly Ad":
            for s in a.find_all("span"):
                ss = s.contents[0]
                if ss.find(" - ") != -1:
                    start = ss[:ss.find(" - ")]
                    end = ss[-ss.rfind(" - "):]
                    return {"start": start, "end": end}


def full_url(link):
    return "http://plan.shoprite.com" + link


def get_store_info(page):
    temp = []
    info = {}
    for a in page.find_all("div", {"id": "RegionStore"}):
        info['name'] = ''.join(a.find("h1").contents)
        # Find a better way to get store address, locale and phone number
        for h2 in a.find("h2").contents:
            h2 = ''.join(h2).split()
            if h2:
                temp.append(" ".join(h2))
    info['address'] = temp[0]
    info['locale'] = temp[1]
    info['phone_number'] = temp[2]
    return info


def read_page(link):
    req = urllib2.Request(link)
    req.add_header('User-agent', 'Mozilla/5.0')
    return BeautifulSoup(urllib2.urlopen(req).read())


def create_store(store_info):
    s = Store()
    s.name = store_info['name']
    s.locale = store_info['locale']
    s.address = store_info['address']
    s.phone_number = store_info['phone_number']
    s.save()
    print "Created new store object: with id %d" % s.pk
    return s


def create_circular(s, dates):
    c = Circular()
    c.store = s
    c.start = fmt.convert_date(dates["start"])
    c.end = fmt.convert_date(dates["end"])
    c.save()
    print "Created new circular object: with id %d" % c.pk
    return c


def find_tag(page, tag, var=None, val=None):
    if var and val:
        return page.find_all(tag, {var: val})
    else:
        return page.find_all(tag)


def read_category(link, name, c):
    page = read_page(link)
    # Grab div for inventory items and pass to Item creator
    for div in find_tag(page, "div", "class", "grid-item"):
        i = create_item(div, name, c)
    # Check for additional pages
    for a in find_tag(page, "a", "title", "Next Page"):
        n_page = full_url(a.get("href"))
        if n_page == link:
            return True
        else:
            return read_category(n_page, name, c)


def create_item(div, name, circular_id):
    i = Item()
    if div.find("h2").find("a", {"class": "show-more"}):
        i.name = fmt.convert(div.find("h2").find("a", {"class": "show-more"}).get("title"))
    else:
        i.name = fmt.convert(div.find("h2").contents)
    if div.find("p", {"class": "price"}).find("a", {"class": "show-more"}):
        i.price = fmt.convert(div.find("p", {"class": "price"}).find("a", {"class": "show-more"}).get("title"))
    else:
        i.price = fmt.convert(div.find("p").contents)
    i.category = name
    i.circular = circular_id
    i.save()
    return i