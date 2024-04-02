# Generated by Django 5.0.3 on 2024-03-16 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_integration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='login',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]