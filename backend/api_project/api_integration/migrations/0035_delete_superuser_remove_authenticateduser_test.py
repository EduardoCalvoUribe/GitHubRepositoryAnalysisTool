# Generated by Django 5.0.2 on 2024-06-08 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_integration', '0034_superuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SuperUser',
        ),
        migrations.RemoveField(
            model_name='authenticateduser',
            name='test',
        ),
    ]
