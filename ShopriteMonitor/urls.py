from django.conf.urls import include, url
from django.contrib import admin
from Shoprite import views as reader

urlpatterns = [
    # Examples:
    # url(r'^$', 'ShopriteMonitor.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'time/', reader.current_date_time),
    url(r'store/', reader.get_stores)
]
