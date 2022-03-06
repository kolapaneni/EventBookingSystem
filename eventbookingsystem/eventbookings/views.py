from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import EventSerializer, EventWindowSerializer, BookingsSerializer
from .models import Event, EventWindow, Bookings


class EventView(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
    """
    View to retrieve, create, update and delete events
    """
    permission_classes = (IsAdminUser,)
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(pk=self.kwargs['pk'])


class ListEventsView(generics.ListAPIView):
    """
    View to list all events
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

    def get_queryset(self):
        if self.kwargs.get('pk'):
            return Event.objects.filter(pk=self.kwargs['pk'])
        return Event.objects.all()


class EventWindowView(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
    """
    View to create a new window, update window and delete window for a event
    """
    permission_classes = (IsAdminUser,)
    serializer_class = EventWindowSerializer

    def get_queryset(self):
        return EventWindow.objects.filter(pk=self.kwargs['pk'])


class ListEventWindowsView(generics.ListAPIView):
    """
    View to  list all windows for events,
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = EventWindowSerializer

    def get_queryset(self):
        if self.kwargs.get('pk'):
            EventWindow.objects.filter(pk=self.kwargs['pk'])
        return EventWindow.objects.filter(event__id=self.kwargs['event_id'])


class BookingView(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
    """
    View to retrieve, create, update and delete bookings
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = BookingsSerializer

    def delete(self, request, *args, **kwargs):
        """
            this method cancels a user's booking and
             re-adds the reserved tickets in the cancelled booking to the event window back as available seats
        """
        booking = get_object_or_404(Bookings, pk=self.kwargs['pk'], user__id=self.request.user.id)
        booking.is_cancelled = True
        booking.save()

        # re-adding booked tickets to user availability
        window = booking.window
        window.available_seats += booking.no_tickets
        window.save()

        return Response(status=status.HTTP_200_OK, data={"success": True})

    def get_queryset(self):
        booking = Bookings.objects.filter(pk=self.kwargs['pk'])
        return booking


class ListUserBookingsView(generics.ListAPIView):
    """
    View to  list all user bookings or bookings of one event
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = BookingsSerializer

    def get_queryset(self):
        booking = Bookings.objects.filter(user__id=self.request.user.id)

        if self.kwargs.get('event_id'):
            # to filter booking of an event for a user
            booking = booking.filter(event__id=self.kwargs['event_id'])

        return booking


class ListEventBookingsView(generics.ListAPIView):
    """
    View to list all bookings of an event
    """
    permission_classes = (IsAdminUser,)
    serializer_class = BookingsSerializer

    def get_queryset(self):
        return Bookings.objects.filter(event__id=self.kwargs['event_id'])
