from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.fields import AutoCreatedField, AutoLastModifiedField

class IndexedTimeStampedModel(models.Model):
    created = AutoCreatedField(_('criado em'), db_index=True)
    modified = AutoLastModifiedField(_('modificado em'), db_index=True)

    class Meta:
        abstract = True
