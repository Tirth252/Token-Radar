# Generated by Django 3.2.6 on 2021-08-17 13:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('symbol', models.CharField(max_length=20, unique=True)),
                ('network', models.CharField(choices=[('BSC', 'Binance Smart Chain'), ('ETH', 'Ethereum'), ('MATIC', 'Polygon'), ('TRX', 'Tron')], default='BSC', max_length=6)),
                ('contractAddress', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(default=' ')),
                ('launchDate', models.DateField()),
                ('telegram', models.URLField()),
                ('twitter', models.URLField()),
                ('discord', models.URLField()),
                ('is_promoted', models.BooleanField(default=False)),
                ('priceUSD', models.DecimalField(blank=True, decimal_places=100, max_digits=100)),
                ('priceBNB', models.DecimalField(blank=True, decimal_places=100, max_digits=100)),
                ('votes', models.IntegerField(default=0)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos')),
                ('custotchart', models.URLField()),
                ('registeredBy', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('votedBy', models.ManyToManyField(blank=True, related_name='whovoted', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
