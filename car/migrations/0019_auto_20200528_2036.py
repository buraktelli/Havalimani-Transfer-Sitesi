# Generated by Django 3.0.4 on 2020-05-28 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0018_reservation_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='date',
            field=models.DateField(blank=True, default='2020-05-28'),
        ),
    ]