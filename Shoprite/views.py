from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.db.models import Q
from Shoprite.models import Store, StaticItem
from search import forms
from django.template import RequestContext, loader
import string
# Create your views here.


def current_date_time(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s</body></html>" % now
    return HttpResponse(html)


def test(request):
    form = forms.NameForm()
    return HttpResponse(form)


def search(request):
    search_results = StaticItem.objects.filter(Q(name__icontains="baby") | Q(category__icontains="baby"))
    template = loader.get_template('search/search_results.html')
    context = RequestContext(request, {
        'search_results': search_results,
    })
    return HttpResponse(template.render(context))

"""
def search(request):
    name = Q(name__icontains="baby")
    category = Q(category__icontains="baby")
    qset = StaticItem.objects.filter(name | category)
    list_string = ""
    for a in qset:
        list_string += "<a href=searches/" + string.replace(a.name, " ", "-") + "/" + str(a.id) + "> "+ a.name + "</a><br>"
    return HttpResponse(list_string)
"""

def get_stores(request):
    s = Store.objects.get(pk=1)
    html = s.address
    return HttpResponse(html)