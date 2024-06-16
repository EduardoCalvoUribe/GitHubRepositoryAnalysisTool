# Generated by Django 5.0.2 on 2024-06-08 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_integration', '0033_authenticateduser_test'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuperUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=100)),
                ('test', models.CharField(default='test', max_length=100)),
            ],
        ),
    ]
