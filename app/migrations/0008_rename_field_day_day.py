# Generated by Django 3.2 on 2022-05-11 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_slot_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='day',
            old_name='field',
            new_name='day',
        ),
    ]
