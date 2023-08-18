import logging
from django.conf import settings
from django.core.management import BaseCommand
from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from core.models import User

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "run bot"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.BOT_TOKEN)

    def handle_user_without_verification(self, msg: Message, tg_user: TgUser):
        user = User.objects.filter(verification_token = msg.text).first()
        if user:
            tg_user.user = user
            tg_user.save(update_fields=["user"])
            self.tg_client.send_message(
               msg.chat.id, "[ Verification has been completed ]"
            )
        else:
            self.tg_client.send_message(
                msg.chat.id, f"[ Verification token is wrong! Try again. ]"
            )

    def handle_verified_user(self, msg: Message, tg_user: TgUser):
        if "/messages" in msg.text:
            ...
        elif msg.text.startswith("/"):
            self.tg_client.send_message(msg.chat.id, "[unknown command]")

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(
            chat_id=msg.chat.id,
            defaults={"username": msg.from_.username},
        )
        if created:
            self.tg_client.send_message(msg.chat.id, "[ Greeting ]\n [ Send verification Token ]")
        if tg_user.user:
            self.handle_verified_user(msg, tg_user)
        else:
            self.handle_user_without_verification(msg, tg_user)

    def handle(self, *args, **kwargs):
        offset = 0

        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)
