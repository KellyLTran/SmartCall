# Generated by Django 5.0.2 on 2025-02-04 19:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Duel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_number', models.IntegerField()),
                ('phone_1', models.CharField(max_length=255)),
                ('phone_2', models.CharField(blank=True, max_length=255, null=True)),
                ('winner', models.CharField(blank=True, max_length=255, null=True)),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smart_call_app.tournament')),
            ],
        ),
    ]
