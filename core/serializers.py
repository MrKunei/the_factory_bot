from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError

from .models import User, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "login",
            "username",
        )


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "login",
            "username",
            "password",
            "password_repeat",
        )

    def validate(self, attrs):
        password = attrs.get('password')
        password_repeat = attrs.pop('password_repeat', None)

        if password != password_repeat:
            raise ValidationError("password and password_repeat is not equal")
        return attrs

    def create(self, validated_data):
        self.user = User.objects.create_user(**validated_data)
        return self.user


class LoginUserSerializer(serializers.ModelSerializer):
    login = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'login',
            'password',
        )

    def validate(self, attrs):
        login = attrs.get('login')
        password = attrs.get('password')

        user = authenticate(login=login, password=password)
        if not user:
            raise ValidationError("login or password is incorrect")
        attrs["user"] = user
        return attrs


class MessageCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Message
        read_only_fields = ('id', 'created_at')
        fields = '__all__'

    def create(self, validated_data):
        message = Message.objects.create(**validated_data)
        return message


class MessageListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('created_at', 'text')