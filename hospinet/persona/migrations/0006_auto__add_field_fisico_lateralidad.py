# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Fisico.lateralidad'
        db.add_column(u'persona_fisico', 'lateralidad',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=1, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Fisico.lateralidad'
        db.delete_column(u'persona_fisico', 'lateralidad')


    models = {
        u'persona.antecedente': {
            'Meta': {'object_name': 'Antecedente'},
            'alergias': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'artritis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'asma': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cardiopatia': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'colelitiasis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'colitis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'congenital': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'diabetes': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gastritis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'general': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'hepatitis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hipertension': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hipertrigliceridemia': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'migrana': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nutricional': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'otros': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['persona.Persona']", 'unique': 'True', 'primary_key': 'True'}),
            'rinitis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sinusitis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tuberculosis': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'persona.antecedentefamiliar': {
            'Meta': {'object_name': 'AntecedenteFamiliar'},
            'carcinogenico': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cardiovascular': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'endocrinologico': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'otros': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['persona.Persona']", 'unique': 'True', 'primary_key': 'True'}),
            'respiratorio': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'persona.antecedenteobstetrico': {
            'Meta': {'object_name': 'AntecedenteObstetrico'},
            'a': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'c': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'displasia': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'g': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'menarca': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'otros': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'p': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['persona.Persona']", 'unique': 'True', 'primary_key': 'True'}),
            'ultimo_periodo': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'persona.antecedentequirurgico': {
            'Meta': {'object_name': 'AntecedenteQuirurgico'},
            'fecha': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'antecedentes_quirurgicos'", 'primary_key': 'True', 'to': u"orm['persona.Persona']"}),
            'procedimiento': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'persona.estilovida': {
            'Meta': {'object_name': 'EstiloVida'},
            'cafe': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cantidad': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'cantidad_cafe': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'cerveza': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'consume_drogas': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'consume_tabaco': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'consumo_diario_tabaco': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'dieta': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'drogas': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'inicio_consumo_tabaco': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'licor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'numero_comidas': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'otros': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'estilo_vida'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['persona.Persona']"}),
            'tipo_de_comidas': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'tipo_de_tabaco': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'vino': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'persona.fisico': {
            'Meta': {'object_name': 'Fisico'},
            'altura': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'color_de_cabello': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'color_de_ojos': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'factor_rh': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'lateralidad': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['persona.Persona']", 'unique': 'True', 'primary_key': 'True'}),
            'peso': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'tipo_de_sangre': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'})
        },
        u'persona.persona': {
            'Meta': {'object_name': 'Persona'},
            'apellido': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'celular': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'domicilio': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'estado_civil': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'fotografia': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identificacion': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'nacimiento': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'nacionalidad': ('persona.fields.OrderedCountryField', [], {'max_length': '2', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'profesion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'sexo': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'tipo_identificacion': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'})
        }
    }

    complete_apps = ['persona']