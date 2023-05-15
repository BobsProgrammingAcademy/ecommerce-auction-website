from django.test import TestCase
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
