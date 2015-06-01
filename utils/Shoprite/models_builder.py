from utils.Shoprite import format_strings, scraper, shoprite_price_data
from Shoprite.models import Store, Circular, Item, SaleItem, Units, XForYItem, FlatPriceItem, \
    FractionalReductionItem, PercentReductionItem, RangedPriceItem


def build_circular(partial_url):
    print "Getting circular item data"
    item_list = scraper.scrape_circular(partial_url)
    circular_info = scraper.circular_info(partial_url)
    dates = scraper.circular_valid_dates(scraper.get_webpage_data(scraper.full_url(partial_url)))
    store, created = Store.objects.get_or_create(name="Shoprite",
                                                 address=circular_info["info"]["address"],
                                                 locale=circular_info["info"]["locale"],
                                                 phone_number=circular_info["info"]["phone_number"])
    circular = Circular.objects.create(store=store, start=dates["start"], end=dates["end"])
    for item in item_list:
        m_item, created = Item.objects.get_or_create(name=item["name"])
        sale_item = SaleItem.objects.create(static_item=m_item, circular=circular)
        price_string = format_strings.remove_extra_text(
            format_strings.remove_extra_periods(format_strings.cents_to_dollars(item["price"])))

        # Check if item has a unit measure
        returns = shoprite_price_data.price_units(price_string)
        if returns["bool"]:
            Units.objects.create(sale_item=sale_item, unit=returns["units"])

        #  Check if price plus card is required
        returns = shoprite_price_data.get_plus_card(returns["price"])
        SaleItem.objects.filter(pk=sale_item.pk).update(card_requirement=returns["bool"])

        #  Check if sale is an x items for $y
        returns = shoprite_price_data.x_for_y(returns["price"])
        if returns["bool"]:
            XForYItem.objects.create(sale_item=sale_item, count=returns["count"], price=returns["price"],
                                     effective_price=returns["eff_price"])
            break

        #  Check if sale is a fractional reduction
        returns = shoprite_price_data.fractional_reduction(returns["price"])
        if returns["bool"]:
            FractionalReductionItem.objects.create(sale_item=sale_item, fractional_reduction=returns["price"])
            break

        #  Check if sale is a percent reducation
        returns = shoprite_price_data.percent_reduction(returns["price"])
        if returns["bool"]:
            PercentReductionItem.objects.create(sale_item=sale_item, percent_reduction=returns["price"])
            break

        #  Check if sale is a ranged price
        returns = shoprite_price_data.price_range(returns["price"])
        if returns["bool"]:
            RangedPriceItem.objects.create(sale_item=sale_item, minimum_price=returns["price"][0],
                                           maximum_price=returns["price"][1])
            break
        """
        #Check if sale is a flat price reduction
        returns = pdt.flat_reduction(returns["price"])
        if returns["bool"]:
            shop.RangedPriceItem.objects.create(sale_item=sale_item, price_reduction=returns["price"])
        """
        #  Check if sale is a flat price
        print returns["price"]
        returns = shoprite_price_data.flat_price(returns["price"])
        if returns["bool"]:
            FlatPriceItem.objects.create(sale_item=sale_item, price=returns["price"])

