# Generated by Django 4.2.4 on 2023-09-22 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DNC', '0030_alter_viewperms_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='viewperms',
            old_name='sample_id',
            new_name='sample',
        ),
    ]
