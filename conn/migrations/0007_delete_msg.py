# Generated by Django 5.1.4 on 2024-12-16 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conn', '0006_chatroom_host_chatroom_participants_count_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='msg',
        ),
    ]