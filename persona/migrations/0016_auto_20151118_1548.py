# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0015_auto_20150920_1729'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='antecedente',
            options={'ordering': ('-modified', '-created'), 'get_latest_by': 'modified'},
        ),
        migrations.AlterModelOptions(
            name='antecedentefamiliar',
            options={'ordering': ('-modified', '-created'), 'get_latest_by': 'modified'},
        ),
        migrations.AlterModelOptions(
            name='antecedenteobstetrico',
            options={'ordering': ('-modified', '-created'), 'get_latest_by': 'modified'},
        ),
        migrations.AlterModelOptions(
            name='antecedentequirurgico',
            options={'ordering': ('-modified', '-created'), 'get_latest_by': 'modified'},
        ),
        migrations.AlterModelOptions(
            name='estilovida',
            options={'ordering': ('-modified', '-created'), 'get_latest_by': 'modified'},
        ),
        migrations.AlterModelOptions(
            name='fisico',
            options={'ordering': ('-modified', '-created'), 'get_latest_by': 'modified'},
        ),
        migrations.AddField(
            model_name='antecedente',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(default=datetime.datetime(2015, 11, 18, 21, 47, 10, 574000, tzinfo=utc), verbose_name='created', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='antecedente',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(default=datetime.datetime(2015, 11, 18, 21, 47, 21, 152000, tzinfo=utc), verbose_name='modified', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='antecedentefamiliar',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(default=datetime.datetime(2015, 11, 18, 21, 47, 27, 534000, tzinfo=utc), verbose_name='created', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='antecedentefamiliar',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(default=datetime.datetime(2015, 11, 18, 21, 47, 35, 13000, tzinfo=utc), verbose_name='modified', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='antecedenteobstetrico',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(default=datetime.datetime(2015, 11, 18, 21, 47, 42, 182000, tzinfo=utc), verbose_name='created', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='antecedenteobstetrico',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(default=datetime.datetime(2015, 11, 18, 21, 47, 52, 280000, tzinfo=utc), verbose_name='modified', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='antecedentequirurgico',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(default=datetime.datetime(2015, 11, 18, 21, 47, 54, 745000, tzinfo=utc), verbose_name='created', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='antecedentequirurgico',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(default=datetime.datetime(2015, 11, 18, 21, 47, 57, 915000, tzinfo=utc), verbose_name='modified', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='estilovida',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(default=datetime.datetime(2015, 11, 18, 21, 48, 0, 522000, tzinfo=utc), verbose_name='created', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='estilovida',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(default=datetime.datetime(2015, 11, 18, 21, 48, 3, 92000, tzinfo=utc), verbose_name='modified', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fisico',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(default=datetime.datetime(2015, 11, 18, 21, 48, 7, 484000, tzinfo=utc), verbose_name='created', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fisico',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(default=datetime.datetime(2015, 11, 18, 21, 48, 10, 511000, tzinfo=utc), verbose_name='modified', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='persona',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(default=datetime.datetime(2015, 11, 18, 21, 48, 13, 88000, tzinfo=utc), verbose_name='created', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='persona',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(default=datetime.datetime(2015, 11, 18, 21, 48, 16, 484000, tzinfo=utc), verbose_name='modified', auto_now=True),
            preserve_default=False,
        ),
    ]
