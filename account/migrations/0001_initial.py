# Generated by Django 3.2.7 on 2021-10-23 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('activation_code', models.CharField(blank=True, max_length=20)),
                ('spam_subscribe', models.BooleanField(blank=True, default=False, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
