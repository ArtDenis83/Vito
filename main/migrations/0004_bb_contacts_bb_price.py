# Generated by Django 4.1.1 on 2022-10-16 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_bb_additionalimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='bb',
            name='contacts',
            field=models.TextField(default=123, verbose_name='Контакты'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bb',
            name='price',
            field=models.FloatField(default=0, verbose_name='Цена'),
        ),
    ]