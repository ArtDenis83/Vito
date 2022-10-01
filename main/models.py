from django.db import models
from django.contrib.auth.models import AbstractUser

# Создает кастомного юзера, так как нужно хранить доп данные о пользователе
class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name="Прошел активацию?")
    send_messages = models.BooleanField(default=True, verbose_name="Слать оповещения о новых комментариях?")

    class Meta(AbstractUser.Meta):
        pass



