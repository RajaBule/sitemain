# Generated by Django 4.2.4 on 2023-10-18 15:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('DNC', '0034_invetoryviewperms_inventoryshare'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='shared_with',
            field=models.ManyToManyField(blank=True, related_name='shared_inventory', through='DNC.InventoryShare', to=settings.AUTH_USER_MODEL),
        ),
    ]