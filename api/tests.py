from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from django.core import mail
from django.conf import settings

from .models import Event, Register, Subscriber

class ContactAPITests(APITestCase):
    def test_valid_contact_submission(self):
        url = reverse('contact')
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'Test message'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Contact Form Message from John Doe')
        self.assertEqual(mail.outbox[0].to, [settings.CONTACT_EMAIL])

    def test_invalid_contact_submission(self):
        url = reverse('contact')
        data = {
            'name': '',  # Invalid: empty name
            'email': 'invalid-email',  # Invalid email
            'message': ''  # Invalid: empty message
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class EventAPITests(APITestCase):
    def setUp(self):
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            eventdatetime=timezone.now() + timedelta(days=7),
            address='123 Test St',
            price=Decimal('99.99')
        )

    def test_list_events(self):
        url = reverse('event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_event(self):
        url = reverse('event-list')
        data = {
            'title': 'New Event',
            'description': 'New Description',
            'eventdatetime': (timezone.now() + timedelta(days=14)).isoformat(),
            'address': '456 New St',
            'price': '149.99'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 2)

    def test_retrieve_event(self):
        url = reverse('event-detail', args=[self.event.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Event')

    def test_update_event(self):
        url = reverse('event-detail', args=[self.event.id])
        data = {
            'title': 'Updated Event',
            'description': self.event.description,
            'eventdatetime': self.event.eventdatetime.isoformat(),
            'address': self.event.address,
            'price': str(self.event.price)
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Event')

    def test_delete_event(self):
        url = reverse('event-detail', args=[self.event.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Event.objects.count(), 0)

class RegisterAPITests(APITestCase):
    def setUp(self):
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            eventdatetime=timezone.now() + timedelta(days=7),
            address='123 Test St',
            price=Decimal('99.99')
        )
        self.registration = Register.objects.create(
            date_registered=timezone.now(),
            email='test@example.com',
            event=self.event
        )

    def test_list_registrations(self):
        url = reverse('register-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_registration(self):
        url = reverse('register-list')
        data = {
            'date_registered': timezone.now().isoformat(),
            'email': 'new@example.com',
            'event': self.event.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Register.objects.count(), 2)

    def test_filter_registrations_by_event(self):
        url = f"{reverse('register-list')}?event={self.event.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['email'], 'test@example.com')

class SubscriberAPITests(APITestCase):
    def setUp(self):
        self.subscriber = Subscriber.objects.create(
            name='Test User',
            email='test@example.com'
        )

    def test_list_subscribers(self):
        url = reverse('subscriber-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_subscriber(self):
        url = reverse('subscriber-list')
        data = {
            'name': 'New User',
            'email': 'new@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscriber.objects.count(), 2)

    def test_duplicate_email_validation(self):
        url = reverse('subscriber-list')
        data = {
            'name': 'Another User',
            'email': 'test@example.com'  # Same email as in setUp
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_opt_out_subscriber(self):
        url = reverse('subscriber-detail', args=[self.subscriber.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify subscriber is marked as opted out but not deleted
        self.subscriber.refresh_from_db()
        self.assertTrue(self.subscriber.opted_out)
        self.assertEqual(Subscriber.objects.count(), 1)
