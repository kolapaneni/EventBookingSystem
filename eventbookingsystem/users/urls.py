from django.urls import path
from .views import UserAuthToken, UserRegisterView, UserListView

urlpatterns = [
    path('get-token', UserAuthToken.as_view()),
    path('register', UserRegisterView.as_view()),
    path('list', UserListView.as_view())
]
