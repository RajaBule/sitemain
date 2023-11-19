# Generated by Django 4.2.4 on 2023-09-21 04:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('DNC', '0025_remove_samples_shared_with'),
    ]

    operations = [
        migrations.AddField(
            model_name='samples',
            name='shared_with',
            field=models.ManyToManyField(blank=True, related_name='shared_samples', through='DNC.SampleShare', to=settings.AUTH_USER_MODEL),
        ),
    ]
