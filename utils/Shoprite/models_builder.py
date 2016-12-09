from utils.Shoprite import format_strings, scraper, shoprite_price_data
from Shoprite.models import Store, Circular, StaticItem, SaleItem, Units, XForYSale, FlatPriceSale, \
    FractionalReductionSale, PercentReductionSale, RangedPriceSale, ConditionalSale, FlatReductionSale


def build_circular(partial_url):
    print "Getting circular item data"
    item_list = scraper.scrape_circular(partial_url)
    circular_info = scraper.circular_info(partial_url)
    dates = scraper.circular_valid_dates(scraper.get_webpage_data(scraper.full_url(partial_url)))
    store, created = Store.objects.get_or_create(name="Shoprite",
                                                 address=circular_info["info"]["address"],
                                                 locale=circular_info["info"]["locale"],
                                                 phone_number=circular_info["info"]["phone_number"])
    circular, created = Circular.objects.get_or_create(store=store, start=dates["start"], end=dates["end"])
    if not created:
        print "Circular for this store during these dates already exists"
    else:
        for item in item_list:
            static_item, created = StaticItem.objects.get_or_create(name=item["name"], category=item["category"])
            sale_item = SaleItem.objects.create(static_item=static_item, circular=circular)
            price_string = format_strings.remove_extra_text(
                format_strings.remove_extra_periods(format_strings.cents_to_dollars(item["price"])))

            # Check if item has a unit measure
            returns = shoprite_price_data.price_units(price_string)
            if returns["bool"]:
                Units.objects.create(sale_item=sale_item, unit=returns["units"])

            #  Check if price plus card is required
            returns = shoprite_price_data.get_plus_card(returns["price"])
            SaleItem.objects.filter(pk=sale_item.pk).update(card_requirement=returns["bool"])

            #  Check if sale is conditional
            returns = shoprite_price_data.conditional(returns["price"])
            if returns["bool"]:
                ConditionalSale.objects.create(sale_item=sale_item, buy=returns["buy"], get=returns["get"])
                continue

            #  Check if sale is an x items for $y
            returns = shoprite_price_data.x_for_y(returns["price"])
            if returns["bool"]:
                XForYSale.objects.create(
                    sale_item=sale_item,
                    count=returns["count"], price=returns["price"], effective_price=returns["eff_price"])
                continue

            #  Check if sale is a fractional reduction
            returns = shoprite_price_data.fractional_reduction(returns["price"])
            if returns["bool"]:
                FractionalReductionSale.objects.create(
                    sale_item=sale_item,
                    fractional_reduction=returns["fractional_reduction"], percent_reduction=returns["price"])
                continue

            #  Check if sale is a percent reducation
            returns = shoprite_price_data.percent_reduction(returns["price"])
            if returns["bool"]:
                PercentReductionSale.objects.create(sale_item=sale_item, percent_reduction=returns["price"])
                continue

            #  Check if sale is a ranged price
            returns = shoprite_price_data.price_range(returns["price"])
            if returns["bool"]:
                RangedPriceSale.objects.create(sale_item=sale_item, minimum_price=returns["price"][0],
                                               maximum_price=returns["price"][1])
                continue

            #  Check if sale is a flat price reduction
            returns = shoprite_price_data.flat_reduction(returns["price"])
            if returns["bool"]:
                print "\n====================================================================="
                print "Static Item: " + static_item.name + "\tCreated:" + str(created)
                print "Original price string: " + item["price"]
                print "-Flat Reduction Item-"
                print "$" + returns["price"] + " off"
                FlatReductionSale.objects.create(sale_item=sale_item, price_reduction=returns["price"])

            #  Check if sale is a flat price
            returns = shoprite_price_data.flat_price(returns["price"])
            if returns["bool"]:
                FlatPriceSale.objects.create(sale_item=sale_item, price="{0:.2f}".format(float(returns["price"])))
                continue
            "\n====================================================================="
            print "Static Item: " + static_item.name + "\tCreated:" + str(created)
            print "Original price string: " + item["price"]
            print "~~~Item did not fit into any categories~~~"
