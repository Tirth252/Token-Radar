# Generated by Django 3.2.6 on 2021-08-20 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_remove_coins_votes'),
    ]

    operations = [
        migrations.AddField(
            model_name='coins',
            name='votes',
            field=models.IntegerField(default=0),
        ),
    ]
