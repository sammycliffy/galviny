# Generated by Django 2.0 on 2018-06-14 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='profit',
            field=models.CharField(max_length=255, null=True),
        ),
    ]