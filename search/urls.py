from django.conf.urls import url
import search.views

urlpatterns = [
    url(r'test/', search.views.search),
    url(r'item/(?P<item_id>\d+)', search.views.test),
]
