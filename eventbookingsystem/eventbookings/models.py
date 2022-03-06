from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Event(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


class EventWindow(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='event_windows'
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    available_seats = models.IntegerField()
    total_seats = models.IntegerField()


class Bookings(models.Model):
    window = models.ForeignKey(
        EventWindow,
        on_delete=models.CASCADE
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    no_tickets = models.IntegerField()
    is_cancelled = models.BooleanField(default=False)
