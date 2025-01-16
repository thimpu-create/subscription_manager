# Generated by Django 5.1.4 on 2025-01-16 07:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SMTPSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=255)),
                ('port', models.IntegerField()),
                ('password', models.CharField(max_length=255)),
                ('use_ssl', models.BooleanField(default=False)),
                ('use_tls', models.BooleanField(default=True)),
                ('email', models.EmailField(max_length=254)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'SMTP Settings',
                'verbose_name_plural': 'SMTP Settings',
            },
        ),
    ]
