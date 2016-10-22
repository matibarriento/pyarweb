# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import community.models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0011_auto_20160326_0230'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='ts_moderate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='user_moderate',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='is_active',
            field=models.BooleanField(default=community.models.is_active_default),
        ),
    ]
