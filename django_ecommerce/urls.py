from django.contrib import admin
from django.conf.urls import url, include
from core import views
from catalog import views as catalog_views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^contato/$', views.contact, name='contact'),
    url(r'^catalogo/', include(('catalog.urls', 'catalog'), namespace='catalog')),
    url(r'^admin/', admin.site.urls),
]
