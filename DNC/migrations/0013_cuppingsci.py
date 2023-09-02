# Generated by Django 4.2.4 on 2023-09-02 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DNC', '0012_samples_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='CuppingSCI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample_id', models.CharField(max_length=100)),
                ('roast_level_range', models.FloatField()),
                ('ferment_level_range', models.FloatField()),
                ('fragrance_range', models.FloatField()),
                ('fragrance_intensity_range', models.FloatField()),
                ('fragrance_notes', models.TextField()),
                ('flavor_range', models.FloatField()),
                ('flavor_intensity_range', models.FloatField()),
                ('Flavor_notes', models.TextField()),
                ('acidity_range', models.FloatField()),
                ('acidity_intensity_range', models.FloatField()),
                ('Acidity_notes', models.TextField()),
                ('body_range', models.FloatField()),
                ('body_thickness_range', models.FloatField()),
                ('body_notes', models.TextField()),
                ('sweetness_range', models.FloatField()),
                ('sweetness_intensity_range', models.FloatField()),
                ('sweetness_notes', models.TextField()),
                ('aftertaste_range', models.FloatField()),
                ('aftertaste_duration_range', models.FloatField()),
                ('aftertaste_notes', models.TextField()),
                ('fresh_range', models.FloatField()),
                ('fresh_woody_range', models.FloatField()),
                ('freshcrop_notes', models.TextField()),
                ('off_1_range', models.IntegerField()),
                ('off_2_range', models.IntegerField()),
                ('off_3_range', models.IntegerField()),
                ('off_4_range', models.IntegerField()),
                ('off_5_range', models.IntegerField()),
                ('off_notes', models.TextField()),
                ('uniform_1_range', models.IntegerField()),
                ('uniform_2_range', models.IntegerField()),
                ('uniform_3_range', models.IntegerField()),
                ('uniform_4_range', models.IntegerField()),
                ('uniform_5_range', models.IntegerField()),
                ('uniformity_notes', models.TextField()),
                ('sens_descriptors', models.TextField()),
            ],
        ),
    ]