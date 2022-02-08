# Generated by Django 2.2.16 on 2022-02-08 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20220208_0541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'User role'), ('moderator', 'Moderator role'), ('admin', 'Administrator role')], default='user', max_length=2, verbose_name='Пользовательская роль'),
        ),
    ]
