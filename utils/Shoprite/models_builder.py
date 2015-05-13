from Shoprite import models
from utils.Shoprite import format_strings, scraper, shoprite_price_data
from utils.common.StringManipulators import format_strings as fmt


def build_circular(partial_url):
    item_list = scraper.scrape_circular(partial_url)
    circular_info = scraper.circular_info(partial_url)
    store, created = models.Store.objects.get_or_create(name="Shoprite",
                                               address=circular_info["info"]["address"],
                                               locale=circular_info["info"]["locale"],
                                               phone_number=circular_info["info"]["phone_number"])

