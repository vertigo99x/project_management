# Generated by Django 4.2.16 on 2024-10-25 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_uuid_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('user', 'user'), ('admin', 'admin')], default='user', max_length=10, null=True),
        ),
    ]
