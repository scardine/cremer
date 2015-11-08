# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('status', models.IntegerField(choices=[(1, 'Active'), (0, 'Inactive'), (2, 'Blocked')])),
                ('notify', models.BooleanField(default=True, verbose_name='Notify account manager on activity?')),
                ('account_manager', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(default=0, choices=[(0, 'Support'), (1, 'Billing'), (2, 'Closed')])),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('locator', models.CharField(max_length=30, null=True, blank=True)),
                ('pcc', models.CharField(max_length=30, null=True, blank=True)),
                ('pax_name', models.CharField(max_length=40)),
                ('pax_email', models.EmailField(max_length=254, null=True, blank=True)),
                ('subject', models.CharField(max_length=200)),
                ('charge', models.IntegerField(default=0, choices=[(0, b'Client'), (1, b'Pax'), (2, b'Agency'), (3, b'Other')])),
                ('bill_to', models.CharField(max_length=100, null=True, blank=True)),
                ('tax_number', models.CharField(max_length=30, null=True, blank=True)),
                ('invoice_number', models.CharField(max_length=30, null=True, blank=True)),
                ('client', models.ForeignKey(to='helpdesk.Client')),
                ('responsible', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IncidentLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('incident', models.ForeignKey(to='helpdesk.Incident')),
                ('responsible', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
