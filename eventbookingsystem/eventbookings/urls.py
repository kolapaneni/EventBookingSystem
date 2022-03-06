from django.urls import path
from .views import (EventView, ListEventsView,
                    ListEventWindowsView, EventWindowView, BookingView, ListEventBookingsView, ListUserBookingsView)

urlpatterns = [
    path('create', EventView.as_view()),
    path('update/<int:pk>', EventView.as_view()),
    path('list', ListEventsView.as_view()),
    path('get/<int:pk>', ListEventsView.as_view()),

    path('windows/get/<int:pk>', EventWindowView.as_view()),
    path('windows/create', EventWindowView.as_view()),
    path('windows/update/<int:pk>', EventWindowView.as_view()),
    path('windows/list/<int:event_id>', ListEventWindowsView.as_view()),

    path('booking/get/<int:pk>', BookingView.as_view()),
    path('booking/create', BookingView.as_view()),
    # path('booking/update/<int:pk>', BookingView.as_view()),
    path('booking/delete/<int:pk>', BookingView.as_view()),
    path('booking/list/user', ListUserBookingsView.as_view()),
    path('booking/list/user/<int:event_id>', ListUserBookingsView.as_view()),
    path('booking/list/event/<int:event_id>', ListEventBookingsView.as_view()),
]
