# Generated by Django 2.0 on 2018-06-17 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_auto_20180617_0627'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cryptocurrency',
            old_name='date',
            new_name='deposit_date',
        ),
        migrations.AddField(
            model_name='cryptocurrency',
            name='lend_date',
            field=models.DateTimeField(null=True),
        ),
    ]
