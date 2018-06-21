# Generated by Django 2.0 on 2018-06-11 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20180611_1123'),
    ]

    operations = [
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
    ]