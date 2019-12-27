from django.db import models

class CartItemManager(models.Manager):
    def add_item(self, cart_id, product):
        if self.filter(cart_id=cart_id, product=product).exists():
            created = False
            cart_item = self.get(cart_id=cart_id, product=product)
            cart_item.quantity = cart_item.quantity + 1
            cart_item.save()
        else:
            created = True
            cart_item = CartItem.objects.create(cart_id=cart_id, product=product, price=product.price)
        return cart_item, created

class CartItem(models.Model):
    cart_id = models.CharField('Chave do carrinho', max_length=40, db_index=True)
    product = models.ForeignKey('catalog.Product', verbose_name='Produto', on_delete=models.CASCADE)
    quantity = models.IntegerField('Quantidade', default=1)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=8)

    objects = CartItemManager()

    class Meta:
        verbose_name = 'Item do Carrinho'
        verbose_name_plural = 'Itens do Carrinho'
        unique_together = (('cart_id', 'product'),)

    def __str__(self):
        return f'{self.product} [{self.quantity}]'
