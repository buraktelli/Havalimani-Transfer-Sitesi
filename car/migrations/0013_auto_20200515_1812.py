# Generated by Django 3.0.4 on 2020-05-15 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0012_auto_20200515_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='start_hour',
            field=models.IntegerField(blank=True, max_length=10),
        ),
    ]