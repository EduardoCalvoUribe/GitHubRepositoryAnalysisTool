# Generated by Django 5.0.3 on 2024-03-25 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_integration', '0003_repos_rename_user_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='repos',
            name='users',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
