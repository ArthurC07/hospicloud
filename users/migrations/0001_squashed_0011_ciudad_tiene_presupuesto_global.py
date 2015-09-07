# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import userena.models
import django.utils.timezone
from django.conf import settings
import easy_thumbnails.fields
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bsc', '0001_squashed_0013_holiday_login'),
        ('auth', '0001_initial'),
        ('inventory', '0001_squashed_0019_auto_20150729_1025'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('persona', '0001_squashed_0013_persona_mostrar_en_cardex'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('action', models.TextField()),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('mugshot', easy_thumbnails.fields.ThumbnailerImageField(help_text='A personal image displayed in your profile.', upload_to=userena.models.upload_to_mugshot, verbose_name='mugshot', blank=True)),
                ('privacy', models.CharField(default=b'registered', help_text='Designates who can view your profile.', max_length=15, verbose_name='privacy', choices=[(b'open', 'Open'), (b'registered', 'Registered'), (b'closed', 'Closed')])),
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('honorario', models.ForeignKey(related_name='usuarios', blank=True, to='inventory.ItemTemplate', null=True)),
                ('inventario', models.ForeignKey(related_name='usuarios', blank=True, to='inventory.Inventario', null=True)),
                ('persona', models.OneToOneField(related_name='profile', null=True, blank=True, to='persona.Persona')),
                ('user', models.OneToOneField(related_name='profile', null=True, blank=True, to=settings.AUTH_USER_MODEL)),
                ('prefijo_recibo', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
                'permissions': (('view_profile', 'Can view profile'),),
            },
        ),
        migrations.AddField(
            model_name='useraction',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('nombre', models.CharField(max_length=100)),
                ('correlativo_de_recibo', models.IntegerField(default=0)),
                ('prefijo_recibo', models.CharField(max_length=100, blank=True)),
                ('inicio_rango', models.CharField(max_length=100, blank=True)),
                ('limite_de_emision', models.DateTimeField(default=django.utils.timezone.now)),
                ('direccion', models.CharField(max_length=255, blank=True)),
                ('telefono', models.CharField(max_length=100, blank=True)),
                ('fin_rango', models.CharField(max_length=100, blank=True)),
                ('tiene_presupuesto_global', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.AddField(
            model_name='userprofile',
            name='ciudad',
            field=models.ForeignKey(related_name='usuarios', blank=True, to='users.Ciudad', null=True),
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='prefijo_recibo',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='bsc',
            field=models.ForeignKey(related_name='usuarios', blank=True, to='bsc.ScoreCard', null=True),
        ),
    ]
