from django.test import TestCase
from Scraper import Scraper
# Create your tests here.

s = Scraper("/Circular/ShopRite-of-Newton/8C15732/Categories")
s.scrape_category_data()