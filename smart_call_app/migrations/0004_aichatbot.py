# Generated by Django 5.0.2 on 2025-03-19 14:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smart_call_app', '0003_tournament_winner'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AIChatbot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.TextField()),
                ('response', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smart_call_app.tournament')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
