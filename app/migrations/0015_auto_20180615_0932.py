# Generated by Django 2.0 on 2018-06-15 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_remove_plan_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cryptocurrency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, null=True)),
                ('plan', models.CharField(max_length=255, null=True)),
                ('confirmed', models.BooleanField(default=False)),
                ('profit', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Plan',
        ),
    ]
