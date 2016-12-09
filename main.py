#!/usr/bin/env python
import os


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ShopriteMonitor.settings")
    import django
    django.setup()
    from utils.Shoprite.models_builder import build_circular as build
    build("/Circular/ShopRite-of-Newton/8C15732/Categories")