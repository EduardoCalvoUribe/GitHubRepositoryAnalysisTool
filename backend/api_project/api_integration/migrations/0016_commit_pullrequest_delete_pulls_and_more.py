# Generated by Django 5.0.3 on 2024-04-02 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_integration', '0015_remove_repos_login'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('title', models.CharField(max_length=100)),
                ('body', models.CharField(max_length=500)),
                ('user_test', models.CharField(max_length=100)),
                ('comments', models.JSONField(blank=True, default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='PullRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('title', models.CharField(max_length=100)),
                ('body', models.CharField(max_length=100)),
                ('user', models.CharField(max_length=100)),
                ('comments', models.JSONField(blank=True, default=dict)),
            ],
        ),
        migrations.DeleteModel(
            name='Pulls',
        ),
        migrations.RemoveField(
            model_name='users',
            name='avatar_url',
        ),
        migrations.RemoveField(
            model_name='users',
            name='html_url',
        ),
    ]
