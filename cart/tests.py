from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from menu.models import MenuItem
from .models import CartItem

User = get_user_model()

class CartTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.client.login(username='user1', password='pass123')
        self.item = MenuItem.objects.create(name='Pizza', price=50.00, description='Cheesy goodness')

    def test_add_to_cart(self):
        response = self.client.post(reverse('cart_add', args=[self.item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CartItem.objects.count(), 1)
