# Generated by Django 3.0.3 on 2020-04-07 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrateur', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offres',
            name='titre',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
