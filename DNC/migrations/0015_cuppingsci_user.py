# Generated by Django 4.2.4 on 2023-09-02 05:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('DNC', '0014_alter_cuppingsci_acidity_notes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuppingsci',
            name='user',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]