# Generated by Django 5.0.2 on 2024-05-31 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_integration', '0025_rename_repos_repository_rename_users_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='comments',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name='user',
            name='commits',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name='user',
            name='pull_requests',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name='user',
            name='repositories',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
