# Generated by Django 2.0 on 2018-06-15 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_auto_20180615_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptocurrency',
            name='profit',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
