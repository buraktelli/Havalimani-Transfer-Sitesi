# Generated by Django 3.0.4 on 2020-05-13 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0010_auto_20200510_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='check_in',
            field=models.DateField(blank=True, default='13-05-2020'),
        ),
    ]
