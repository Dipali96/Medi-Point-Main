# Generated by Django 3.2 on 2022-05-12 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20220513_0135 copy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slot',
            name='auto_increment_id',
        ),
        migrations.AddField(
            model_name='slot',
            name='id',
            field=models.AutoField(default=1000, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
