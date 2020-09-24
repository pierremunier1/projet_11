
from django.test import TestCase, Client
from django.urls import reverse
from products.models import Category, Product, Substitute
from users.models import CustomUser
from django.core import mail

# Create your tests here.

class UserTest(TestCase):


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


    def test_reset_password_3(self):
        """test function to reset password"""
        
        response = self.client.get("/users/reset/MTQ/set-password/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_reset_confirm.html')

    def test_reset_password_4(self):
        """test function to confirm change password"""

        response = self.client.post(("/users/password_reset/"),{'email':self.email})
        self.assertEqual(response.status_code, 302)
        # At this point the system will "send" us an email:
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Password reset on testserver')
        # Now we can use the token:
        token = response.context[0]['token']
        uid = response.context[0]['uid']
        response = self.client.get(reverse('password_reset_confirm', kwargs={'token':token,'uidb64':uid}))
        self.assertEqual(response.status_code, 302)
        # Now we post to the same url with our new password:
        response = self.client.post(reverse('password_reset_confirm', 
        kwargs={'uidb64':uid,'token':token}),{'new_password1':'password32!','new_password2':'password32!'})
       