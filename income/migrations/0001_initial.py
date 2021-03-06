# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-16 19:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('invoice', '0001_initial'),
        ('budget', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('persona', '0002_auto_20160116_1236'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('nombre', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Cheque',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('fecha_de_entrega', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_de_emision', models.DateTimeField(default=django.utils.timezone.now)),
                ('numero_de_cheque', models.CharField(max_length=255)),
                ('monto', models.DecimalField(decimal_places=2, default=0, max_digits=11)),
                ('monto_retenido', models.DecimalField(decimal_places=2, default=0, max_digits=11)),
                ('imagen_de_cheque', models.FileField(null=True, upload_to='income/cheque/%Y/%m/%d')),
                ('banco_de_emision', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='income.Banco')),
                ('emisor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='persona.Persona')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Deposito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('fecha_de_deposito', models.DateTimeField(default=django.utils.timezone.now)),
                ('monto', models.DecimalField(decimal_places=2, default=0, max_digits=11)),
                ('aplicado', models.BooleanField(default=False)),
                ('comprobante', models.FileField(upload_to='income/deposito/%Y/%m/%d')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='DetallePago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('monto', models.DecimalField(decimal_places=2, default=0, max_digits=11)),
                ('cheque', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='income.Cheque')),
                ('pago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.Pago')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='CierrePOS',
            fields=[
                ('deposito_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='income.Deposito')),
                ('batch', models.CharField(max_length=255)),
                ('banco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='income.Banco')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=('income.deposito',),
        ),
        migrations.AddField(
            model_name='deposito',
            name='cuenta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget.Fuente'),
        ),
        migrations.AddField(
            model_name='deposito',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
