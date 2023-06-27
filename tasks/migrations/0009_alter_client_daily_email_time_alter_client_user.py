# Generated by Django 4.0.1 on 2023-06-27 07:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0008_alter_client_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='daily_email_time',
            field=models.TimeField(blank=True, default='00:00:00', null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]