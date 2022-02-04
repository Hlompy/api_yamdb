from api.permissions import IsAdminPermission
from api_yamdb.settings import EMAIL_ADMIN
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import SignupSerializer, TokenSerializer, UserSerializer


class UserJSWTokenViewSet(viewsets.ViewSetMixin, generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    def create(self, request, *args, **kwargs):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
        confirmation_code = serializer.data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            jwt_token = RefreshToken.for_user(user)
            return Response(
                {'token': str(jwt_token.access_token)},
                status=status.HTTP_200_OK
            )
        return Response(
            status=status.HTTP_400_BAD_REQUEST
        )

class UserSignupViewSet(viewsets.ViewSetMixin, generics.CreateAPIView):
    """Регистрация пользователя."""
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = self.request.data.get('username')
        email = self.request.data.get('email')
        user = serializer.save(username=username, email=email)
        confirmation_code = default_token_generator.make_token(user)
        send_mail("Token", confirmation_code, EMAIL_ADMIN, (email,),)
        return Response(
            {'email': email, 'username': username},
            status=status.HTTP_200_OK
        )

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminPermission,)
    filter_backends = (filters.SearchFilter,)
    
    lookup_field = 'username'
