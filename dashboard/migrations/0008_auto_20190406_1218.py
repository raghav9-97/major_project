# Generated by Django 2.1.7 on 2019-04-06 12:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_auto_20190405_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usage',
            name='started_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 6, 12, 18, 5, 789961, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='usage',
            name='stopped_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 6, 12, 18, 5, 789994, tzinfo=utc)),
        ),
    ]
