from django.db import models
from django.utils.translation import ugettext_lazy as _

# from model_utils.fields import AutoCreatedField, AutoLastModifiedField

class IndexedTimeStampedModel(models.Model):
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        abstract = True
