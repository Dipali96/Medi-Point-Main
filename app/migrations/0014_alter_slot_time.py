# Generated by Django 3.2 on 2022-05-12 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_alter_slot_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='time',
            field=models.CharField(blank=True, max_length=60),
        ),
    ]