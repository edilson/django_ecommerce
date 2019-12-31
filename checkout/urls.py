from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^adicionar/(?P<slug>[\w_-]+)/$', views.CreateCartItemView.as_view(), name='create_cartitem'),
    url(r'^carrinho/$', views.CartItemView.as_view(), name='cart_item'),
]
