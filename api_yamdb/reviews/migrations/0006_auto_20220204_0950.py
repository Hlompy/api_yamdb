# Generated by Django 2.2.16 on 2022-02-04 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20220203_1031'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ('name',), 'verbose_name': 'Жанр', 'verbose_name_plural': 'Жанры'},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ('name',), 'verbose_name': 'Произведение', 'verbose_name_plural': 'Произведения'},
        ),
        migrations.AddField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='title',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='Рейтигн'),
        ),
    ]
