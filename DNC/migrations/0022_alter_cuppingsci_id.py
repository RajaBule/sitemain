# Generated by Django 4.2.4 on 2023-09-19 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DNC', '0021_alter_cuppingsci_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuppingsci',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]