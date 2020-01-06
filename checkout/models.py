from django.db import models
from django.conf import settings

from core.models import IndexedTimeStampedModel

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

class OrderManager(models.Manager):
    def create_order(self, user, cart_items):
        order = self.create(user=user)
        for cart_item in cart_items:
            order_item = OrderItem.objects.create(
                order=order, quantity=cart_item.quantity, product=cart_item.product,
                price=cart_item.price
            )
        return order

class Order(IndexedTimeStampedModel):
    STATUS_CHOICES = (
        (0, 'Aguardando Pagamento'),
        (1, 'Concluída'),
        (2, 'Cancelada'),
    )

    PAYMENT_OPTION_CHOICES = (
        ('deposit', 'Depósito'),
        ('pagseguro', 'PagSeguro'),
        ('paypal', 'Paypal'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', on_delete=models.CASCADE)
    status = models.IntegerField('Situação', choices=STATUS_CHOICES, default=0, blank=True)
    payment_option = models.CharField('Opção de pagamento', choices=PAYMENT_OPTION_CHOICES, max_length=20, default='deposit')

    objects = OrderManager()

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return f'Pedido #{self.pk}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='Pedido', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('catalog.Product', verbose_name='Produto', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=8)

    class Meta:
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens do pedido'

    def __str__(self):
        return f'[{self.order}] {self.product}'

def post_save_cat_item(instance, **kwargs):
    if instance.quantity < 1:
        instance.delete()

models.signals.post_save.connect(
    post_save_cat_item, sender=CartItem, dispatch_uid='post_save_cart_item'
)
