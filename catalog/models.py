from django.db import models
from django.urls import reverse

from core.models import IndexedTimeStampedModel

class Category(IndexedTimeStampedModel):
    name = models.CharField('Nome', max_length=200)
    slug = models.SlugField('Identificador', max_length=200)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:category', kwargs={'slug': self.slug})

class Product(IndexedTimeStampedModel):
    name = models.CharField('Produto', max_length=200)
    slug = models.SlugField('Identificador', max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name='Categoria', null=True)
    description = models.TextField('Descrição', blank=True)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=8)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:product', kwargs={'slug': self.slug})
