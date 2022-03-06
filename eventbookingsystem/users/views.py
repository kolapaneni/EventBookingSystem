from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from .serializers import UserSerializer


class UserRegisterView(generics.CreateAPIView):
    """
    View to register a user or Admin
    """
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class UserListView(generics.ListAPIView):
    """
    View to List all users
    """
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer


class UserAuthToken(ObtainAuthToken):
    """
    View to create authentication token for a user
    """

    def post(self, request, *args, **kwargs):
        """
        This method creates the token for a user and saves it to DB
        """
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
