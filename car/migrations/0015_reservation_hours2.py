# Generated by Django 3.0.4 on 2020-05-14 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0014_remove_reservation_start_hour'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='hours2',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
    ]
