# Generated by Django 2.0 on 2018-06-16 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_auto_20180615_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptocurrency',
            name='choice',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
