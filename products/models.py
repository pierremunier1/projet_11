from django.db import models
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django import forms

from .management.commands import config


class Category(models.Model):
    """category models"""
    category_name = models.CharField(max_length=150, unique=True)

    class Meta:
        ordering = ['category_name']

    def __str__(self):
        return self.category_name


class ProductManager(models.Manager):
    """manager find product substitutes"""

    def search_sub(self, product_name):
        """check if substitutes exists in database"""

        product = Product.objects.filter(
            Q(product_name__icontains=product_name) |
            Q(brands__icontains=product_name
              ))[:1].get()

        substitutes = Product.objects.filter(
            category=product.category,
            nutriscore_fr__lt=product.nutriscore_fr
        ).order_by("nutriscore_fr")[:9]

        return product, substitutes

    def get_detail(self, product_id):
        """get detail of product"""

        try:
            product = Product.objects.get(id=product_id)

        except Product.DoesNotExist:
            product = None

        finally:
            return product

    def add_substitute(self, product_original_id, product_substitute_id, user):
        """save substitute in favoris"""

        Substitute.objects.update_or_create(
            product_substitute_id=product_substitute_id,
            product_original_id=product_original_id,
            customuser=user
        )


class Product(models.Model):
    """product model"""
    id = models.BigIntegerField(primary_key=True)
    product_name = models.CharField(max_length=150)
    nutriscore_fr = models.CharField(max_length=2)
    nutriscore_100g = models.CharField(max_length=150)
    brands = models.CharField(max_length=150)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE
    )
    product_url = models.CharField(max_length=150)
    image_nutrition = models.CharField(max_length=250)
    image_food = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)
    objects = ProductManager()

    class Meta:
        ordering = ['product_name']

    def __str__(self):
        return self.product_name


class Substitute(models.Model):
    """substitute model"""

    customuser = models.ForeignKey(
        'users.CustomUser', on_delete=models.CASCADE)
    product_original = models.ForeignKey(Product,
                                         on_delete=models.CASCADE, related_name='product_original')
    product_substitute = models.ForeignKey(Product,
                                           on_delete=models.CASCADE, related_name='product_substitute')
    objects = ProductManager()

    def __str__(self):

        return str(self.product_substitute)
