from django.shortcuts import render
from django.http import HttpResponse
import datetime
from Reader.models import Store
import Scraper as Scraper
# Create your views here.

def current_date_time(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s</body></html>" % now
    return HttpResponse(html)

def get_stores(request):
    s = Store.objects.get(pk=1)
    html = s.name
    return HttpResponse(html)