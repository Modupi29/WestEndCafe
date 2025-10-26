from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Booking

User = get_user_model()

class BookingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.client.login(username='user1', password='pass123')

    def test_booking_detail(self):
        response = self.client.post(reverse('booking_detail', args=[self.booking.id]), {
            'name': 'Test Booking',
            'email': 'test@example.com',
            'phone': '123456789',
            'date': '2025-10-25',
            'time': '14:00',
            'guests': 2,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Booking.objects.count(), 1)

    def test_booking_list(self):
        Booking.objects.create(
            user=self.user,
            name='Sample',
            email='s@example.com',
            phone='000111222',
            date='2025-10-25',
            time='10:00',
            guests=3,
        )
        response = self.client.get(reverse('booking_list'))
        self.assertContains(response, 'Sample')
