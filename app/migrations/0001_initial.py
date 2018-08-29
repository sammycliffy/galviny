# Generated by Django 2.0 on 2018-08-21 09:56

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
            name='Cryptocurrency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, null=True)),
                ('choice', models.PositiveIntegerField(null=True)),
                ('lent', models.CharField(blank=True, max_length=255)),
                ('confirmed', models.BooleanField(default=False)),
                ('profit', models.PositiveIntegerField(default=0, null=True)),
                ('deposit_date', models.DateTimeField(auto_now=True)),
                ('lend_date', models.DateTimeField(blank=True, null=True)),
                ('amount_lent', models.PositiveIntegerField(default=0, null=True)),
                ('previous_withdraw', models.PositiveIntegerField(default=0, null=True)),
                ('logistics', models.PositiveIntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Expired_Referrer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referee', models.CharField(max_length=255, null=True)),
                ('referred', models.CharField(max_length=255, null=True)),
                ('amount', models.PositiveIntegerField(null=True)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Forex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, null=True)),
                ('choice', models.PositiveIntegerField(null=True)),
                ('lent', models.CharField(blank=True, max_length=255)),
                ('confirmed', models.BooleanField(default=False)),
                ('profit', models.PositiveIntegerField(default=0, null=True)),
                ('deposit_date', models.DateTimeField(auto_now=True)),
                ('lend_date', models.DateTimeField(blank=True, null=True)),
                ('amount_lent', models.PositiveIntegerField(default=0, null=True)),
                ('previous_withdraw', models.PositiveIntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, null=True)),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Oil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, null=True)),
                ('choice', models.PositiveIntegerField(null=True)),
                ('lent', models.CharField(blank=True, max_length=255)),
                ('confirmed', models.BooleanField(default=False)),
                ('profit', models.PositiveIntegerField(default=0, null=True)),
                ('deposit_date', models.DateTimeField(auto_now=True)),
                ('lend_date', models.DateTimeField(blank=True, null=True)),
                ('amount_lent', models.PositiveIntegerField(default=0, null=True)),
                ('previous_withdraw', models.PositiveIntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payable_referred',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, null=True)),
                ('amount', models.PositiveIntegerField(null=True)),
                ('previous_username', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=255, null=True)),
                ('lastname', models.CharField(max_length=255, null=True)),
                ('address', models.CharField(max_length=255, null=True)),
                ('age', models.CharField(max_length=255, null=True)),
                ('phone', models.CharField(max_length=255, null=True)),
                ('sex', models.CharField(max_length=255, null=True)),
                ('bank', models.CharField(max_length=255, null=True)),
                ('account_name', models.CharField(max_length=255, null=True)),
                ('occupation', models.CharField(max_length=255, null=True)),
                ('account_number', models.CharField(max_length=255, null=True)),
                ('email_confirmed', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Referrer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referee', models.CharField(max_length=255, null=True)),
                ('referred', models.CharField(max_length=255, null=True)),
                ('amount', models.PositiveIntegerField(null=True)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Testimony',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, null=True)),
                ('testimony', models.CharField(max_length=255, null=True)),
                ('date', models.DateField(auto_now=True)),
                ('confirmed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=255, null=True)),
                ('email', models.EmailField(max_length=255, null=True)),
                ('plan', models.CharField(max_length=255, null=True)),
                ('amount', models.CharField(max_length=255, null=True)),
                ('date', models.DateField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Withdraw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, null=True)),
                ('plan', models.CharField(max_length=255, null=True)),
                ('withdraw_amount', models.PositiveIntegerField(null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('previous_withdraw', models.PositiveIntegerField(default=0, null=True)),
                ('logistics', models.PositiveIntegerField(default=0, null=True)),
            ],
        ),
    ]
