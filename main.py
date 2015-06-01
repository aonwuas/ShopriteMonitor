#!/usr/bin/env python
import os


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ShopriteMonitor.settings")
    from utils.Shoprite.models_builder import build_circular as build
    build("/Circular/ShopRite-of-Newton/8C15732/Categories")
    """
    from utils.Shoprite.shoprite_price_data import fractional_reduction
    string = 'Shit\'s 1/4 price!'
    returned = fractional_reduction(string)
    print returned["price"]
    """