# Generated by Django 4.2.4 on 2023-09-22 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DNC', '0029_alter_viewperms_country_alter_viewperms_cropyear_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viewperms',
            name='id',
            field=models.CharField(max_length=300, primary_key=True, serialize=False),
        ),
    ]
