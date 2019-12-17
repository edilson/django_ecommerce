from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth.views import LoginView, LogoutView

from core import views
from catalog import views as catalog_views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^contato/$', views.contact, name='contact'),
    url(r'^login/', LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/', LogoutView.as_view(next_page='index'), name='logout'),
    url(r'^cadastrar/', views.SignupView.as_view(), name='signup'),
    url(r'^catalogo/', include(('catalog.urls', 'catalog'), namespace='catalog')),
    url(r'^admin/', admin.site.urls),
]
