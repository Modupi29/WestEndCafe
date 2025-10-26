from django.test import TestCase
from django.urls import reverse
from .models import MenuItem

class MenuTests(TestCase):
    def setUp(self):
        MenuItem.objects.create(name='Burger', description='Tasty beef burger', price=50)

    def test_menu_list(self):
        response = self.client.get(reverse('menu_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Burger')
