from lists import views as list_views
from lists import urls as list_urls
from accounts import urls as accounts_urls
from django.conf.urls import url, include

urlpatterns = [
    url(r'^$', list_views.home_page, name="home"),
    url(r'^lists/', include(list_urls)),
    url(r'^accounts/', include(accounts_urls)),
    #url(r'^admin/', admin.site.urls),
]
