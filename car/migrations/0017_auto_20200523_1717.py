# Generated by Django 3.0.4 on 2020-05-23 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0016_auto_20200523_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='kisi_sayisi',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]