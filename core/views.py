import os
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.views import APIView
from django.contrib.auth import login
from rest_framework import permissions

from bot.models import TgUser
from bot.tg.client import TgClient
from config import settings
from core.serializers import CreateUserSerializer, LoginUserSerializer, UserSerializer, MessageCreateSerializer, \
    MessageListSerializer
from rest_framework.response import Response
from .models import User, Message


class SignupView(CreateAPIView):
    model = User
    serializer_class = CreateUserSerializer

    def perform_create(self, serializer):
        super().perform_create(serializer)
        login(
            self.request,
            user=serializer.user,
            backend="django.contrib.auth.backends.ModelBackend",
        )

class LoginView(GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serialize = self.get_serializer(data=request.data)
        serialize.is_valid(raise_exception=True)
        user = serialize.validated_data["user"]
        login(request, user=user)
        user_serializer = UserSerializer(instance=user)
        return Response(user_serializer.data)


class GenerateTokenView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        self.request.user.set_verification_token()
        self.request.user.save(update_fields=["verification_token"])
        return Response({'token': self.request.user.verification_token})


class CreateMessageView(CreateAPIView):
    model = Message
    serializer_class = MessageCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        super().perform_create(serializer)
        tg_user = TgUser.objects.filter(user=self.request.user).first()
        tg_client = TgClient(settings.BOT_TOKEN)
        tg_client.send_message(tg_user.chat_id, text=f'{self.request.user.username}, я получил от вас сообщение:'
                                                     f'\n{self.request.data["text"]}')


class ListMessageView(ListAPIView):
    serializer_class = MessageListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user).all()
