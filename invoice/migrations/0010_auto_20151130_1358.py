# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0005_auto_20151123_1041'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('invoice', '0009_cotizacion_terminada'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuentaporcobrar',
            name='enviadas',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='cuentaporcobrar',
            name='usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='pago',
            name='aseguradora',
            field=models.ForeignKey(blank=True, to='contracts.Aseguradora', null=True),
        ),
        migrations.AddField(
            model_name='pagocuenta',
            name='archivo',
            field=models.FileField(null=True, upload_to=b'', blank=True),
        ),
    ]
