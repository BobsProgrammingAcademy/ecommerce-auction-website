from django.test import TestCase
from .models import User


class UserModelUnitTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='john@test.com', username='John', password='pass123')

    def test_user_model(self):
        data = self.user
        self.assertTrue(isinstance(data, User))
        self.assertIsInstance(data, User)
        self.assertEqual(str(data.username), 'John')
