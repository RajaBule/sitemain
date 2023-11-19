# Generated by Django 4.2.4 on 2023-10-18 15:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('DNC', '0033_inventory'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvetoryViewPerms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.BooleanField(default=True)),
                ('stype', models.BooleanField(default=False)),
                ('project', models.BooleanField(default=False)),
                ('location', models.BooleanField(default=True)),
                ('proccessing', models.BooleanField(default=True)),
                ('cropyear', models.BooleanField(default=True)),
                ('varieties', models.BooleanField(default=True)),
                ('regdate', models.BooleanField(default=True)),
                ('grade', models.BooleanField(default=True)),
                ('rating', models.BooleanField(default=False)),
                ('cert', models.BooleanField(default=False)),
                ('notes', models.BooleanField(default=False)),
                ('refid', models.BooleanField(default=False)),
                ('salenum', models.BooleanField(default=False)),
                ('iconum', models.BooleanField(default=False)),
                ('contnum', models.BooleanField(default=False)),
                ('tracknum', models.BooleanField(default=False)),
                ('country', models.BooleanField(default=True)),
                ('farm', models.BooleanField(default=False)),
                ('importer', models.BooleanField(default=False)),
                ('exporter', models.BooleanField(default=False)),
                ('wetmill', models.BooleanField(default=False)),
                ('drymill', models.BooleanField(default=False)),
                ('cooperative', models.BooleanField(default=False)),
                ('assosiation', models.BooleanField(default=False)),
                ('customer', models.BooleanField(default=False)),
                ('othertrac', models.BooleanField(default=False)),
                ('sampleweight', models.BooleanField(default=False)),
                ('sampleweightunit', models.BooleanField(default=False)),
                ('expweight', models.BooleanField(default=False)),
                ('expweightunit', models.BooleanField(default=False)),
                ('expprice', models.BooleanField(default=False)),
                ('exptotalprice', models.BooleanField(default=False)),
                ('exparrival', models.BooleanField(default=False)),
                ('moisture', models.BooleanField(default=True)),
                ('wa', models.BooleanField(default=True)),
                ('density', models.BooleanField(default=True)),
                ('physicaldefects', models.BooleanField(default=True)),
                ('screensize', models.BooleanField(default=True)),
                ('classification', models.BooleanField(default=False)),
                ('estgreenweight', models.BooleanField(default=False)),
                ('sensorialdescriptors', models.BooleanField(default=True)),
                ('generalcomments', models.BooleanField(default=False)),
                ('sensorial', models.BooleanField(default=True)),
                ('can_share', models.BooleanField(default=False)),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DNC.inventory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InventoryShare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('can_alter', models.BooleanField(default=False)),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DNC.inventory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]