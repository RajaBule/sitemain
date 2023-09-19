# Generated by Django 4.2.4 on 2023-09-17 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DNC', '0018_alter_cuppingsci_acidity_intensity_range_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuppingsci',
            name='freshcrop_notes',
            field=models.TextField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='cuppingsci',
            name='off_1_range',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='cuppingsci',
            name='off_2_range',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='cuppingsci',
            name='off_3_range',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='cuppingsci',
            name='off_4_range',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='cuppingsci',
            name='off_5_range',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='cuppingsci',
            name='sample_id',
            field=models.CharField(max_length=10000),
        ),
        migrations.AlterField(
            model_name='cuppingsci',
            name='uniform_1_range',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='cuppingsci',
            name='uniform_2_range',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='cuppingsci',
            name='uniform_3_range',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='cuppingsci',
            name='uniform_4_range',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='cuppingsci',
            name='uniform_5_range',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]