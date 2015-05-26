from Shoprite import models
from utils.Shoprite import format_strings as fmt, scraper, shoprite_price_data as pdt


def build_circular(partial_url):
    item_list = scraper.scrape_circular(partial_url)
    circular_info = scraper.circular_info(partial_url)
    dates = scraper.circular_valid_dates(scraper.get_webpage_data(scraper.full_url(partial_url)))
    store, created = models.Store.objects.get_or_create(name="Shoprite",
                                                        address=circular_info["info"]["address"],
                                                        locale=circular_info["info"]["locale"],
                                                        phone_number=circular_info["info"]["phone_number"])
    circular = models.Circular.objects.create(store=store.pk, start=dates["start"], end=dates["end"])
    for item in item_list:
        m_item = models.Item.objects.get_or_create(name=item["name"])
        sale_item = models.SaleItem.objects.create(item=m_item.pk, circular=circular.pk)
        price_string = fmt.remove_extra_text(fmt.remove_extra_periods(fmt.cents_to_dollars(item["price"])))

        # Check if item has a unit measure
        returns = pdt.price_units(price_string)
        if returns["bool"]:
            models.Units.objects.create(item=sale_item.pk, unit=returns["units"])

        #  Check if price plus card is required
        returns = pdt.get_plus_card(returns["price"])
        models.SaleItem.objects.filter(pk=sale_item.pk).update(card_requirement=returns["bool"])

        #  Check if sale is an x items for $y
        returns = pdt.x_for_y(returns["price"])
        if returns["bool"]:
            models.XForYItem.objects.create(sale_item=sale_item.pk, count=returns["count"])

        #  Check if sale is a fractional reduction
        returns = pdt.fractional_reduction(returns["price"])
        if returns["bool"]:
            models.FractionalReductionItem.objects.create(sale_item=sale_item.pk, fractional_reduction=returns["price"])

        #  Check if sale is a percent reducation
        returns = pdt.percent_reduction(returns["price"])
        if returns["bool"]:
            models.PercentReductionItem.objects.create(sale_item=sale_item.pk, percent_reduction=returns["price"])

        #  Check if sale is a ranged price
        returns = pdt.price_range(returns["price"])
        if returns["bool"]:
            models.RangedPriceItem.objects.create(sale_item=sale_item.pk, minimum_price=returns["price"][0],
                                                  maximum_price=returns["price"][1])
        """
        #Check if sale is a flat price reduction
        returns = pdt.flat_reduction(returns["price"])
        if returns["bool"]:
            models.RangedPriceItem.objects.create(sale_item=sale_item.pk, price_reduction=returns["price"])
        """
        #Check if sale is a flat price
        returns = pdt.flat_price(returns["price"])
        if returns["bool"]:
            models.FlatPriceItem.objects.create(sale_item=sale_item.pk, price=returns["price"])

        print returns["price"]
