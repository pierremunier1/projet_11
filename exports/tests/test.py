from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from products.models import Category, Product, Substitute
from users.models import CustomUser
import json
from exports.helpers import Exporter


class ExportTest(TestCase):

    """Products test class"""

    def setUp(self):
        """initializing tests variables"""

        self.username = 'jtest'
        self.email = 'test@ygmail.com'
        self.password = 'Barchetta24'
        self.customuser = CustomUser.objects.create_user(
            self.username, self.email, self.password)
        self.customuser.save()
        self.client = Client()
        category = Category.objects.create(category_name="Pâte à tartiner")
        nutella = {
            'id': '3017620429484',
            'product_name': 'Nutella',
            'brands': 'Ferrero',
            'category': Category.objects.get(category_name=category),
            'nutriscore_fr': 'e',
            'product_url': 'https://fr.openfoodfacts.org/produit/3017620429485/nutella-ferrero',
            'image_food': 'https://test',
            'image_nutrition': 'https://test',
        }
        self.nutella = Product.objects.create(**nutella)

        nociolatta = {
            'id': '3017620429485',
            'product_name': 'Nociolatta',
            'brands': 'Rigoni',
            'category': Category.objects.get(category_name=category),
            'nutriscore_fr': 'b',
            'product_url': 'https://fr.openfoodfacts.org/produit/3017620429485/nociolatta',
            'image_food': 'https://test',
            'image_nutrition': 'https://test',
        }
        self.nociolatta = Product.objects.create(**nociolatta)

    def test_export_view(self):
        """test export view"""

        login = self.client.login(
            username=self.username, password=self.password)
        response = self.client.get('/exports') 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response['content-disposition'], 'attachment; filename="export.json"')

    def test_build_export(self):
        """test build export"""
        Substitute.objects.create(
            customuser=self.customuser,
            product_original=self.nutella,
            product_substitute=self.nutella
        )
        self.client.login(username=self.username, password=self.password)
        product = Product.objects.get(id=3017620429484)
        substitute = Product.objects.get(id=3017620429484)
        response = self.client.post(f'/{product.id}/{substitute.id}')
        result = [{'product_original': {'product_name': 'Nutella', 'id': 3017620429484}, 'product_substitute': {'product_name': 'Nutella', 'id': 3017620429484}}]
        exporter = Exporter()
        data = exporter.data
        self.assertEqual(response.status_code,302 )
        self.assertEqual(result,data)