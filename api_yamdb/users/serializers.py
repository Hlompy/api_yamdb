from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)
    banned_names = ('me', 'admin', 'ADMIN', 'administrator', 'moderator')

    def validate_username(self, data):
        if data in self.banned_names:
            raise serializers.ValidationError(
                "Нельзя использовать такое имя."
            )
        
        if User.objects.filter(username=data).exists():
            raise serializers.ValidationError(
                "Пользователь с таким именем уже существует."
            )

        return data
    
    def validate_email(self, data):
        if User.objects.filter(email=data).exists():
            raise serializers.ValidationError(
                "Пользователь с такой почтой уже зарегистрирован."
            )

        return data
    
class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=24)
