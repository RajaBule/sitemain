# Generated by Django 4.2.4 on 2023-09-19 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DNC', '0022_alter_cuppingsci_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuppingsci',
            name='total_cup_score',
            field=models.TextField(blank=True, null=True),
        ),
    ]
