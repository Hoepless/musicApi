# Generated by Django 3.2.7 on 2021-10-29 03:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20211029_0131'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='userfollowing',
            name='unique_followers',
        ),
    ]
