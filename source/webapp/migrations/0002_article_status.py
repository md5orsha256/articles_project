# Generated by Django 4.0 on 2021-12-22 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='status',
            field=models.CharField(choices=[('new', 'Новая'), ('moderated', 'Модерирована'), ('rejected', 'Откланена')], default='new', max_length=15, verbose_name='Статус'),
        ),
    ]
