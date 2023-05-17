from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Category


class UserModelUnitTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='john@test.com', username='John', password='pass123')

    def test_user_model(self):
        data = self.user
        self.assertTrue(isinstance(data, User))
        self.assertIsInstance(data, User)
        self.assertEqual(str(data.username), 'John')


class CategoryUnitTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(category_name='Books')

    def test_food_category_model(self):
        data = self.category
        self.assertIsInstance(data, Category)
        self.assertEqual(str(data.category_name), 'Books')


class IndexRequestTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class RegisterRequestTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)


class LoginRequestTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)


class ActiveAuctionsRequestTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_active_auctions_view(self):
        response = self.client.get(reverse('active_auctions_view'))
        self.assertEqual(response.status_code, 200)
