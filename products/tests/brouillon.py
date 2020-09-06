 def test_access_my_account_1(self):
        """test action to access login page of my_account"""

        response = self.client.get(reverse('/users/login/?next=/my_account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_signin_invalid(self):
        """Post a valid form from the Sign In page that must return
        the account page (HTTP 302 url redirection).
        """
        response = self.client.post(("/users/login/?next=/my_account"), {
            'username': "self.username",
            'password': "self.password"
        })
    
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_signin_valid(self):
        """Post a valid form from the Sign In page that must return
        the account page (HTTP 302 url redirection).
        """
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 200)