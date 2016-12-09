from django.conf.urls import include, url
from django.contrib import admin
from Shoprite import views as reader
from search.views import search

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'form/', reader.test),
    url(r'test/', search),
    url(r'time/', reader.current_date_time),
    url(r'store/', reader.get_stores),
    url(r'^search/', include('search.urls'))
]
