from django.contrib import admin
from django.conf.urls import url
from core import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^contato/$', views.contato, name='contato'),
    url(r'^produto/$', views.produto, name='produto'),
    url(r'^produtos/$', views.lista_produto, name='lista_produtos'),
    url(r'^admin/', admin.site.urls),
]
