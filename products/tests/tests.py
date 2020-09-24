from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from products.models import Category, Product, Substitute
from users.models import CustomUser


class ProductTest(TestCase):

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

    def test_research(self):
        """test research of product, if correct expected 200 status code"""

        response = self.client.get(reverse('results'), {'query': 'Nutella'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'results.html')

    def test_research_invalid(self):
        """test invalid search expected 302 code"""

        response = self.client.get(reverse('results'), {'query': '?bkxkbx?'})
        self.assertEqual(response.status_code, 302)

    def test_get_detail_of_product(self):
        """test to access detail page of product"""

        product = Product.objects.get(id=3017620429484)

        context = {
            'product_id': product.id,
        }

        response = self.client.get(f'/{product.id}')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'detail.html')

    def test_substitute_save(self):
        """test action to save substitute"""

        product = Product.objects.get(id=3017620429484)
        response = self.client.post(f'/{product.id}/{product.id}')
        self.assertEquals(response.status_code, 302)

    def test_favorite_invalid_credential(self):
        """test access to favorite page with invalid credential"""

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("favorite"), follow=True)
        self.assertEquals(response.status_code, 200)

    def test_favorite_valid_credential(self):
        """test access to favorite page with valid credential"""

        self.client.login(username=self.username, password=self.password)
        response = self.client.post(('/users/login/?next=/favorite'), {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 302)

    def test_favorite_remove_product(self):
        """test access to favorite page with valid credential"""
        Substitute.objects.create(
            customuser=self.customuser,
            product_original=self.nutella,
            product_substitute=self.nutella
        )
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(f'/remove_products/{self.nutella.id}/{self.nutella.id}')
        self.assertEqual(response.status_code, 302)

    def test_mentions_legales(self):
        """test access to mentions legales section"""

        response = self.client.get(reverse('mentions_legales'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mentions_legales.html')

    def test_access_my_account_without_redirection(self):
        """without redirection"""

        response = self.client.get('/my_account')
        self.assertEqual(response.status_code, 302)

    def test_access_my_account_with_redirection(self):
        """with redirection"""

        response = self.client.get('/users/login/?next=/my_account')
        self.assertEqual(response.status_code, 200)

    def test_access_my_account_login(self):
        """with redirection"""

        login = self.client.login(
            username=self.username, password=self.password)
        response = self.client.post(('/users/login/?next=/my_account'), {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(login)


    def test_autocomplete(self):
        """test research of product by autocomplete"""

        response = self.client.get('/search_autocomplete/?term=nute')
        self.assertEqual(response.status_code,200)
        self.assertJSONEqual(response.content,['Nutella'])

    def test_reset_password(self):
        """test function to reset password"""

        response = self.client.get('/users/password_reset/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset.html')
    
    def test_reset_password_1(self):
        """test function to reset password"""

        self.client.login(email=self.email)
        response = self.client.post(('/users/password_reset/'), {
            'email': self.email
        })
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'registration/password_reset_email.html')
    
    def test_reset_password_2(self):
        """test function to reset password"""

        response = self.client.get('/users/password_reset/done/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_reset_done.html')

    
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

