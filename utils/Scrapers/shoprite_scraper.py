import urllib2
from bs4 import BeautifulSoup


def scrape_category_data(url):
        # "Getting category names and links"
        category_list_page = get_webpage_data(full_url(url))
        # "Iterating over categories:"
        for category_page_link in category_list_page.find_all("a", {"data-clientanalyticsaction": "Circular Categories"}):
            link_to_category = category_page_link.get("href")
            category_name = category_page_link.get("data-clientanalyticslabel")
            category_name = category_name[:category_name.rfind(" - ")]
            if category_name != "Store Services":
                #  "   " + category_name
                iterate_over_category_pages(full_url(link_to_category), category_name)


def circular_valid_dates(page):
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
        item["name"] = item_data.find("h2").find("a", {"class": "show-more"}).get("title")
    else:
        item["name"] = item_data.find("h2").contents
    if item_data.find("p", {"class": "price"}).find("a", {"class": "show-more"}):
        item["price"] = item_data.find("p", {"class": "price"}).find("a", {"class": "show-more"}).get("title")
    else:
        item["price"] = item_data.find("p").contents
    item["category"] = category_name
    return item


def iterate_over_category_pages(link_to_category, category_name):
    page = get_webpage_data(link_to_category)
    # Check for additional pages
    for next_page_link in page.find_all("a", {"title": "Next Page"}):
        next_page = full_url(next_page_link.get("href"))
        #  Check if next page loops back to this page (end of pages)
        if next_page == link_to_category:
            return True
        else:
            return iterate_over_category_pages(next_page, category_name)