from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """class user favorite"""

    lastname = models.CharField(max_length=150)
    firstname = models.CharField(max_length=150)
    saved = models.ManyToManyField(
        'products.Product',
        through='products.Substitute',
        through_fields=('customuser', 'product_original','product_substitute'),
        )
