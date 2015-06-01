import urllib2
import datetime
from bs4 import BeautifulSoup
import utils.common.StringManipulators.format_strings as s_format


def scrape_circular(partial_url):
    # "Getting category names and links"
    category_list_page = get_webpage_data(full_url(partial_url))
    # "Iterating over categories:"
    item_list = []
    for category_page_link in category_list_page.find_all("a", {"data-clientanalyticsaction": "Circular Categories"}):
        link_to_category = category_page_link.get("href")
        category_name = category_page_link.get("data-clientanalyticslabel")
        category_name = s_format.to_plain_string(category_name[:category_name.rfind(" - ")])
        if category_name != "Store Services":
            item_list = item_list + iterate_over_category_pages(full_url(link_to_category), category_name)
    return item_list


def circular_info(partial_url):
    page = get_webpage_data(full_url(partial_url))
    dates = circular_valid_dates(page)
    store_info = store_location_and_number(page)
    return dict(valid_dates=dates, info=store_info)


def convert_date(string):
    return datetime.datetime.strptime(string, "%m/%d/%y").strftime("%Y-%m-%d")


def circular_valid_dates(page):
    for a in page.find_all("a", {"class": "megadrop-circular-name"}):
        tag = a.get("data-clientanalyticslabel")
        if tag[:tag.find(" - ")] == "Weekly Ad":
            for s in a.find_all("span"):
                ss = s.contents[0]
                if ss.find(" - ") != -1:
                    start = ss[:ss.find(" - ")]
                    end = ss[-ss.rfind(" - "):]
                    return {"start": convert_date(start), "end": convert_date(end)}


def full_url(link):
    return "http://plan.shoprite.com" + link


def store_location_and_number(page):
    temp = []
    store_information = {}
    for a in page.find_all("div", {"id": "RegionStore"}):
        store_information['name'] = ''.join(a.find("h1").contents)
        # Find a better way to get store address, locale and phone number
        for h2 in a.find("h2").contents:
            h2 = ''.join(h2).split()
            if h2:
                temp.append(" ".join(h2))
    store_information['address'] = temp[0]
    store_information['locale'] = temp[1]
    store_information['phone_number'] = temp[2]
    return store_information


def get_webpage_data(link):
    req = urllib2.Request(link)
    req.add_header('User-agent', 'Mozilla/5.0')
    return BeautifulSoup(urllib2.urlopen(req).read())


def get_item_data(item_data, category_name):
    item = {}
    if item_data.find("h2").find("a", {"class": "show-more"}):
        item["name"] = s_format.to_plain_string(item_data.find("h2").find("a", {"class": "show-more"}).get("title"))
    else:
        item["name"] = s_format.to_plain_string(item_data.find("h2").contents)
    if item_data.find("p", {"class": "price"}).find("a", {"class": "show-more"}):
        item["price"] = s_format.to_plain_string(item_data.find("p", {"class": "price"})
                                                 .find("a", {"class": "show-more"}).get("title"))
    else:
        item["price"] = s_format.to_plain_string(item_data.find("p").contents)
    item["category"] = category_name
    return item


def iterate_over_category_pages(link_to_category, category_name):
    item_list = []
    while True:
        page = get_webpage_data(link_to_category)
        for div in page.find_all("div", {"class": "grid-item"}):
            item_list.append(get_item_data(div, category_name))
        # Check for additional pages
        next_page = page.find_all("a", {"title": "Next Page"})
        if not next_page or full_url(next_page[0].get("href")) == link_to_category:
            return item_list
        else:
            link_to_category = full_url(next_page[0].get("href"))