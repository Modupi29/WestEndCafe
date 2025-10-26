from django.test import TestCase
from django.urls import reverse
from .models import Event

class EventTests(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            title='Music Fest',
            date='2025-10-30',
            time='19:00',
            is_active=True
        )

    def test_event_list(self):
        response = self.client.get(reverse('event_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Music Fest')

    def test_event_detail(self):
        response = self.client.get(reverse('event_detail', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Live music night')
