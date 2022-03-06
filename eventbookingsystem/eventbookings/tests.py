from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Event, EventWindow, Bookings


class Events(TestCase):

    def setUp(self):

        self.admin_user = User.objects.create_user(
            username='admin', email='admin@gmail.com', password='top_secret', is_staff=True)
        self.user = User.objects.create_user(
            username='mahesh', email='mahesh@gmail.com', password='top_secret', is_staff=False)

        admin_token = Token.objects.create(user=self.admin_user)
        self.admin_client = APIClient()
        self.admin_client.credentials(HTTP_AUTHORIZATION='Token ' + admin_token.key)

        user_token = Token.objects.create(user=self.user)
        self.user_client = APIClient()
        self.user_client.credentials(HTTP_AUTHORIZATION='Token ' + user_token.key)

        self.event = Event.objects.create(id=100, name='event1', description='this is a event', user=self.admin_user)
        self.event_window = EventWindow.objects.create(id=100, event=self.event,
                                                       start_time='10:00', end_time='10:30',
                                                       available_seats=100, total_seats=100)

        self.admin_booking = Bookings.objects.create(id=100, no_tickets=10, is_cancelled=False,
                                                     user=self.admin_user, event=self.event, window=self.event_window)

        self.user_booking = Bookings.objects.create(id=101, no_tickets=10, is_cancelled=False,
                                                    user=self.user, event=self.event, window=self.event_window)
        self.event_window.available_seats = 90
        self.event_window.save()
        
    def create_event(self, client):
        data = {
            "name": "test_event",
            "description": "this is a test event",
            "event_windows": [
                {
                    "start_time": "10:00",
                    "end_time": "12:30",
                    "total_seats": 100
                }
            ]
        }
        response = client.post('/event/create', data=data, format="json")
        return response

    def update_event(self, event_id, client):
        data = {
            "name": "test_event",
            "description": "this is a new test event",
            "event_windows": [
                {
                    "start_time": "10:00",
                    "end_time": "12:30",
                    "total_seats": 100
                }
            ]
        }
        response = client.put(f'/event/update/{event_id}', data=data, format="json")
        return response

    def create_event_window(self, event_id, client):
        data = {
            "event_id": event_id,
            "start_time": "10:30",
            "end_time": "10:35",
            "total_seats": 100
        }
        response = client.post('/event/windows/create', data=data, format="json")
        return response

    def update_event_window(self, event_id, window_id, client):
        data = {
            "event_id": event_id,
            "start_time": "10:30",
            "end_time": "10:35",
            "available_seats": 90,
            "total_seats": 100
        }
        response = client.put(f'/event/windows/update/{window_id}', data=data, format="json")
        return response

    def create_booking(self, event_id, window_id, client):
        data = {
            "event_id": event_id,
            "window_id": window_id,
            "no_tickets": 10
        }
        response = client.post('/event/booking/create', data=data, format="json")
        return response

    def test_admin_list_events(self):
        response = self.admin_client.get('/event/list')
        self.assertEqual(response.status_code, 200)

    def test_user_list_events(self):
        response = self.user_client.get('/event/list')
        self.assertEqual(response.status_code, 200)

    def test_admin_get_event(self):
        response = self.admin_client.get(f'/event/get/{self.event.id}')
        self.assertEqual(response.status_code, 200)

    def test_user_get_event(self):
        response = self.user_client.get(f'/event/get/{self.event.id}')
        self.assertEqual(response.status_code, 200)
        
    def test_admin_create_event(self):
        response = self.create_event(self.admin_client)
        self.assertEqual(response.status_code, 201)

    def test_user_create_event(self):
        response = self.create_event(self.user_client)
        self.assertEqual(response.status_code, 403)

    def test_admin_update_event(self):
        response = self.update_event(self.event.id, self.admin_client)
        self.assertEqual(response.status_code, 200)

    def test_user_update_event(self):
        response = self.update_event(self.event.id, self.user_client)
        self.assertEqual(response.status_code, 403)

    def test_admin_create_event_window(self):
        response = self.create_event_window(self.event.id, self.admin_client)
        self.assertEqual(response.status_code, 201)

    def test_user_create_event_window(self):
        response = self.create_event_window(self.event.id, self.user_client)
        self.assertEqual(response.status_code, 403)

    def test_admin_update_event_window(self):
        response = self.update_event_window(self.event.id, self.event_window.id, self.admin_client)
        self.assertEqual(response.status_code, 200)

    def test_user_update_event_window(self):
        response = self.update_event_window(self.event.id, self.event_window.id, self.user_client)
        self.assertEqual(response.status_code, 403)

    def test_admin_list_event_windows(self):
        response = self.admin_client.get(f'/event/windows/list/{self.event.id}')
        self.assertEqual(response.status_code, 200)

    def test_user_list_event_windows(self):
        response = self.user_client.get(f'/event/windows/list/{self.event.id}')
        self.assertEqual(response.status_code, 200)

    def test_admin_get_event_window(self):
        response = self.admin_client.get(f'/event/get/{self.event_window.id}')
        self.assertEqual(response.status_code, 200)

    def test_user_get_event_window(self):
        response = self.user_client.get(f'/event/get/{self.event_window.id}')
        self.assertEqual(response.status_code, 200)

    def test_admin_create_booking(self):
        response = self.create_booking(
            event_id=self.event.id, window_id=self.event_window.id, client=self.admin_client
        )
        self.assertEqual(response.status_code, 201)

    def test_user_create_booking(self):
        response = self.create_booking(
            event_id=self.event.id, window_id=self.event_window.id, client=self.user_client
        )
        self.assertEqual(response.status_code, 201)

    def test_admin_get_all_event_bookings(self):
        response = self.admin_client.get(f'/event/booking/list/event/{self.event.id}')
        self.assertEqual(response.status_code, 200)

    def test_user_get_all_event_bookings(self):
        response = self.user_client.get(f'/event/booking/list/event/{self.event.id}')
        self.assertEqual(response.status_code, 403)

    def test_admin_get_all_user_bookings(self):
        response = self.admin_client.get(f'/event/booking/list/user')
        self.assertEqual(response.status_code, 200)

    def test_user_get_all_user_bookings(self):
        response = self.user_client.get(f'/event/booking/list/user')
        self.assertEqual(response.status_code, 200)

    def test_admin_get_booking_by_id(self):
        response = self.admin_client.get(f'/event/booking/get/{self.admin_booking.id}')
        self.assertEqual(response.status_code, 200)

    def test_user_get_booking_by_id(self):
        response = self.user_client.get(f'/event/booking/get/{self.user_booking.id}')
        self.assertEqual(response.status_code, 200)

    def test_admin_cancel_booking(self):
        response = self.admin_client.delete(f'/event/booking/delete/{self.admin_booking.id}')
        self.assertEqual(response.status_code, 200)

    def test_user_cancel_booking(self):
        response = self.user_client.delete(f'/event/booking/delete/{self.user_booking.id}')
        self.assertEqual(response.status_code, 200)
