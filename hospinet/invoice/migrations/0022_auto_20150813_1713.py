# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0021_auto_20150810_0712'),
    ]

    operations = [
        migrations.CreateModel(
            name='PagoCuenta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('inicial', models.DecimalField(default=0, max_digits=11, decimal_places=2)),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('observaciones', models.TextField()),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.AddField(
            model_name='cuentaporcobrar',
            name='inicial',
            field=models.DecimalField(default=0, max_digits=11, decimal_places=2),
        ),
        migrations.AddField(
            model_name='pagocuenta',
            name='cuenta',
            field=models.ForeignKey(to='invoice.CuentaPorCobrar'),
        ),
    ]
