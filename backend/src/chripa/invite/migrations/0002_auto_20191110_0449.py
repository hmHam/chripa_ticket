# Generated by Django 2.2.7 on 2019-11-10 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participationlog',
            name='visited_time',
            field=models.DateTimeField(null=True, verbose_name='来店時刻'),
        ),
    ]