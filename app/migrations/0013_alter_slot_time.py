# Generated by Django 3.2 on 2022-05-12 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_rename_s_id_slot_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='time',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
