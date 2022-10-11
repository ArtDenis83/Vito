from django.db import models
from django.contrib.auth.models import AbstractUser

# Модель кастомного юзера, так как нужно хранить доп данные о пользователе
class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name="Прошел активацию?")
    send_messages = models.BooleanField(default=True, verbose_name="Слать оповещения о новых комментариях?")

    class Meta(AbstractUser.Meta):
        pass

# Базовая модель, хранящая рубрики и подрубрики
class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, unique=True, verbose_name="Название")
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name="Порядок")
    super_rubric = models.ForeignKey('SuperRubric', on_delete=models.PROTECT,
                                     null=True, blank=True, verbose_name="Надрубрика")

# Диспетчер записей выбирает только надрубрики (пустое поле super_rubric)
class SuperRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)

# Псевдо-модель надрубрик
class SuperRubric(Rubric):
    objects = SuperRubricManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Надрубрика'
        verbose_name_plural = 'Надрубрики'

# Диспетчер записей выбирает только подрубрики (поле super_rubric заполнено)
class SubRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)

# Псевдо-модель подрубрик
class SubRubric(Rubric):
    objects = SubRubricManager()

    def __str__(self):
        # %-форматирование как эксперимент
        return "%s - %s" % (self.super_rubric.name, self.name)

    class Meta:
        proxy = True
        ordering = ('super_rubric__order', 'super_rubric__name', 'order', 'name')
        verbose_name = 'Подрубрика'
        verbose_name_plural = 'Подрубрики'