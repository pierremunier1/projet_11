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

    def test_export(self):
        """test export view"""

        login = self.client.login(
            username=self.username, password=self.password)
        response = self.client.get(('/exports'), {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.__getitem__('content-type'), 'application/json')

    def test_build_export(self):
        
        exporter = Exporter()
        result = [{'product_original': {'product_name': "100% pur jus d'Oranges BIO pressées", 'id': 3045320104738}, 'product_substitute': {'product_name': 'Pur jus citron vert', 'id': 3478820088879}}]
        response = exporter.data
        self.assertEqual(response, result)