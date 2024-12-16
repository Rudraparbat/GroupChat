# Generated by Django 5.1.4 on 2024-12-16 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conn', '0004_msg_host'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatroom',
            old_name='password',
            new_name='room_id',
        ),
        migrations.AddField(
            model_name='chatroom',
            name='room_type',
            field=models.CharField(choices=[('public', 'Public'), ('private', 'Private')], default='public', max_length=10),
        ),
    ]