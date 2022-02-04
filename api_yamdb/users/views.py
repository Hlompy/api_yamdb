from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import IsAdminPermission
from api_yamdb.settings import EMAIL_ADMIN
from users.models import User
from users.serializers import SignupSerializer, TokenSerializer, UserSerializer


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


class UserJSWTokenViewSet(viewsets.ViewSetMixin, generics.CreateAPIView):
    """Получение JSW-токена."""
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
                {'Token': str(jwt_token.access_token)},
                status=status.HTTP_200_OK
            )
        return Response(
            status=status.HTTP_400_BAD_REQUEST
        )


class UsersViewSet(viewsets.ModelViewSet):
    """Работа с пользователями."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminPermission,)
    filter_backends = (filters.SearchFilter,)

    lookup_field = 'username'

    @action(
        detail=False,
        methods=['GET', 'PUT', 'PATCH'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
