from django.test import TestCase
from usersmodel.models import CustomUser

class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='password',
            name='John',
            surname='Doe',
            country='Country',
            city='City',
            address='123 Street',
            phone='123456789'
        )

    def test_user_str(self):
        self.assertEqual(str(self.user), 'test@example.com')
