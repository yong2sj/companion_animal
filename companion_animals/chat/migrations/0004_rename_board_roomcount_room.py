# Generated by Django 4.0.6 on 2022-08-04 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_room_count_users'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roomcount',
            old_name='board',
            new_name='room',
        ),
    ]
