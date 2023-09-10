# Generated by Django 4.2.4 on 2023-09-05 13:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('DNC', '0016_cuppingsci_aroma_intensity_range_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='samples',
            name='shared_with',
            field=models.ManyToManyField(blank=True, related_name='shared_samples', to=settings.AUTH_USER_MODEL),
        ),
    ]
