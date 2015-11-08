# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='bill_address',
            field=models.TextField(null=True, blank=True),
        ),
    ]
