# Generated by Django 3.0.4 on 2020-05-28 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0024_reservation_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='phone',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
