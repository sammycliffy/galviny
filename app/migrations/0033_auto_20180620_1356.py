# Generated by Django 2.0 on 2018-06-20 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_withdraw_previous_withdraw'),
    ]

    operations = [
        migrations.RenameField(
            model_name='withdraw',
            old_name='date_paid',
            new_name='date',
        ),
        migrations.RemoveField(
            model_name='withdraw',
            name='previous_withdraw',
        ),
        migrations.AddField(
            model_name='cryptocurrency',
            name='previous_withdraw',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]
