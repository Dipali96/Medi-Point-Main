# Generated by Django 3.2 on 2022-05-10 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_speciality'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.speciality'),
        ),
        migrations.DeleteModel(
            name='FieldTypes',
        ),
    ]
