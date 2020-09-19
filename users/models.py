from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """class user favorite"""

    lastname = models.CharField(max_length=150)
    firstname = models.CharField(max_length=150)
    email = models.EmailField(_('email address'), unique=True)
    saved = models.ManyToManyField(
        'products.Product',
        through='products.Substitute',
        through_fields=('customuser', 'product_original','product_substitute'),
        )
