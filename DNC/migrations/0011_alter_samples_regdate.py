# Generated by Django 4.2.4 on 2023-08-28 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DNC', '0010_alter_samples_regdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='samples',
            name='regdate',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]