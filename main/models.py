from django.db import models
from django.contrib.auth.models import AbstractUser
from .utilities import get_timestamp_path


# Модель кастомного юзера, так как нужно хранить доп данные о пользователе
class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name="Прошел активацию?")
    send_messages = models.BooleanField(default=True, verbose_name="Слать оповещения о новых комментариях?")

    # Переопределение функции, чтобы при удалении пользователя удалялись все его объявления
    def delete(self, *args, **kwargs):
        for bb in self.bb_set.all():
            bb.delete()
        super().delete(*args, **kwargs)

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


# Модель самих объявлений
class Bb(models.Model):
    rubric = models.ForeignKey(SubRubric, on_delete=models.PROTECT, verbose_name='Рубрика')
    title = models.CharField(max_length=40, verbose_name='Товар')
    content = models.TextField(verbose_name="Описание")
    image = models.ImageField(blank=True, upload_to=get_timestamp_path,verbose_name='Изображение')
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE, verbose_name='Автор объявления')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Выводить в списке')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')

    # Переопределение метода, чтобы удалялись все связанные доп изображения
    #  При вызове метода delete() возникает сигнал post_delete, обрабатываемый приложением django_cleanup,
    #  которое в ответ удалит все файлы, хранящиеся в удаленной записи
    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-created_at']

# Модель дополнительных иллюстраций
class AdditionalImage(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name='Объявление')
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name='Изображение')

    class Meta:
        verbose_name_plural = 'Дополнительные иллюстрации'
        verbose_name = 'Дополнительная иллюстрация'