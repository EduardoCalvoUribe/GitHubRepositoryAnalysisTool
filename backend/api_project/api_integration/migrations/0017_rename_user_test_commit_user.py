# Generated by Django 5.0.3 on 2024-04-02 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_integration', '0016_commit_pullrequest_delete_pulls_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commit',
            old_name='user_test',
            new_name='user',
        ),
    ]
