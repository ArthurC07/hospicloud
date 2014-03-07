# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'AntecedenteFamiliar.respiratorio'
        db.delete_column(u'persona_antecedentefamiliar', 'respiratorio')

        # Deleting field 'AntecedenteFamiliar.carcinogenico'
        db.delete_column(u'persona_antecedentefamiliar', 'carcinogenico')

        # Deleting field 'AntecedenteFamiliar.endocrinologico'
        db.delete_column(u'persona_antecedentefamiliar', 'endocrinologico')

        # Deleting field 'AntecedenteFamiliar.cardiovascular'
        db.delete_column(u'persona_antecedentefamiliar', 'cardiovascular')

        # Adding field 'AntecedenteFamiliar.sindrome_coronario_agudo'
        db.add_column(u'persona_antecedentefamiliar', 'sindrome_coronario_agudo',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'AntecedenteFamiliar.hipertension'
        db.add_column(u'persona_antecedentefamiliar', 'hipertension',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'AntecedenteFamiliar.tabaquismo'
        db.add_column(u'persona_antecedentefamiliar', 'tabaquismo',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'AntecedenteFamiliar.epoc'
        db.add_column(u'persona_antecedentefamiliar', 'epoc',
                      self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True),
                      keep_default=False)

        # Adding field 'AntecedenteFamiliar.diabetes'
        db.add_column(u'persona_antecedentefamiliar', 'diabetes',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'AntecedenteFamiliar.tuberculosis'
        db.add_column(u'persona_antecedentefamiliar', 'tuberculosis',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'AntecedenteFamiliar.asma'
        db.add_column(u'persona_antecedentefamiliar', 'asma',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'AntecedenteFamiliar.colitis'
        db.add_column(u'persona_antecedentefamiliar', 'colitis',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'AntecedenteFamiliar.sinusitis'
        db.add_column(u'persona_antecedentefamiliar', 'sinusitis',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'AntecedenteFamiliar.colelitiasis'
        db.add_column(u'persona_antecedentefamiliar', 'colelitiasis',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'AntecedenteFamiliar.migrana'
        db.add_column(u'persona_antecedentefamiliar', 'migrana',
                      self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True),
                      keep_default=False)

        # Adding field 'AntecedenteFamiliar.obesidad'
        db.add_column(u'persona_antecedentefamiliar', 'obesidad',
                      self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True),
                      keep_default=False)

        # Adding field 'AntecedenteFamiliar.dislipidemias'
        db.add_column(u'persona_antecedentefamiliar', 'dislipidemias',
                      self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True),
                      keep_default=False)

        # Adding field 'AntecedenteFamiliar.alcoholismo'
        db.add_column(u'persona_antecedentefamiliar', 'alcoholismo',
                      self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True),
                      keep_default=False)

        # Adding field 'AntecedenteFamiliar.cancer'
        db.add_column(u'persona_antecedentefamiliar', 'cancer',
                      self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True),
                      keep_default=False)

        # Adding field 'AntecedenteFamiliar.alergias'
        db.add_column(u'persona_antecedentefamiliar', 'alergias',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'AntecedenteFamiliar.congenital'
        db.add_column(u'persona_antecedentefamiliar', 'congenital',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'AntecedenteFamiliar.general'
        db.add_column(u'persona_antecedentefamiliar', 'general',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'AntecedenteFamiliar.nutricional'
        db.add_column(u'persona_antecedentefamiliar', 'nutricional',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'AntecedenteFamiliar.respiratorio'
        db.add_column(u'persona_antecedentefamiliar', 'respiratorio',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'AntecedenteFamiliar.carcinogenico'
        db.add_column(u'persona_antecedentefamiliar', 'carcinogenico',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'AntecedenteFamiliar.endocrinologico'
        db.add_column(u'persona_antecedentefamiliar', 'endocrinologico',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'AntecedenteFamiliar.cardiovascular'
        db.add_column(u'persona_antecedentefamiliar', 'cardiovascular',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'AntecedenteFamiliar.sindrome_coronario_agudo'
        db.delete_column(u'persona_antecedentefamiliar', 'sindrome_coronario_agudo')

        # Deleting field 'AntecedenteFamiliar.hipertension'
        db.delete_column(u'persona_antecedentefamiliar', 'hipertension')

        # Deleting field 'AntecedenteFamiliar.tabaquismo'
        db.delete_column(u'persona_antecedentefamiliar', 'tabaquismo')

        # Deleting field 'AntecedenteFamiliar.epoc'
        db.delete_column(u'persona_antecedentefamiliar', 'epoc')

        # Deleting field 'AntecedenteFamiliar.diabetes'
        db.delete_column(u'persona_antecedentefamiliar', 'diabetes')

        # Deleting field 'AntecedenteFamiliar.tuberculosis'
        db.delete_column(u'persona_antecedentefamiliar', 'tuberculosis')

        # Deleting field 'AntecedenteFamiliar.asma'
        db.delete_column(u'persona_antecedentefamiliar', 'asma')

        # Deleting field 'AntecedenteFamiliar.colitis'
        db.delete_column(u'persona_antecedentefamiliar', 'colitis')

        # Deleting field 'AntecedenteFamiliar.sinusitis'
        db.delete_column(u'persona_antecedentefamiliar', 'sinusitis')

        # Deleting field 'AntecedenteFamiliar.colelitiasis'
        db.delete_column(u'persona_antecedentefamiliar', 'colelitiasis')

        # Deleting field 'AntecedenteFamiliar.migrana'
        db.delete_column(u'persona_antecedentefamiliar', 'migrana')

        # Deleting field 'AntecedenteFamiliar.obesidad'
        db.delete_column(u'persona_antecedentefamiliar', 'obesidad')

        # Deleting field 'AntecedenteFamiliar.dislipidemias'
        db.delete_column(u'persona_antecedentefamiliar', 'dislipidemias')

        # Deleting field 'AntecedenteFamiliar.alcoholismo'
        db.delete_column(u'persona_antecedentefamiliar', 'alcoholismo')

        # Deleting field 'AntecedenteFamiliar.cancer'
        db.delete_column(u'persona_antecedentefamiliar', 'cancer')

        # Deleting field 'AntecedenteFamiliar.alergias'
        db.delete_column(u'persona_antecedentefamiliar', 'alergias')

        # Deleting field 'AntecedenteFamiliar.congenital'
        db.delete_column(u'persona_antecedentefamiliar', 'congenital')

        # Deleting field 'AntecedenteFamiliar.general'
        db.delete_column(u'persona_antecedentefamiliar', 'general')

        # Deleting field 'AntecedenteFamiliar.nutricional'
        db.delete_column(u'persona_antecedentefamiliar', 'nutricional')


    models = {
        u'persona.antecedente': {
            'Meta': {'object_name': 'Antecedente'},
            'alcoholismo': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'alergias': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'artritis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'asma': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cancer': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'cardiopatia': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'colelitiasis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'colesterol': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'colitis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'congenital': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'diabetes': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gastritis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'general': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'hepatitis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hipertension': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hipertrigliceridemia': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'migrana': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'nutricional': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'obesidad': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'otros': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['persona.Persona']", 'unique': 'True', 'primary_key': 'True'}),
            'rinitis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sinusitis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'trigliceridos': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'tuberculosis': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'persona.antecedentefamiliar': {
            'Meta': {'object_name': 'AntecedenteFamiliar'},
            'alcoholismo': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'alergias': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'asma': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cancer': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'colelitiasis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'colitis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'congenital': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'diabetes': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dislipidemias': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'epoc': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'general': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'hipertension': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'migrana': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'nutricional': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'obesidad': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'otros': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'antecedente_familiar'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['persona.Persona']"}),
            'sindrome_coronario_agudo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sinusitis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tabaquismo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tuberculosis': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'persona.antecedenteobstetrico': {
            'Meta': {'object_name': 'AntecedenteObstetrico'},
            'anticoncepcion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'cesareas': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'displasia': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gestas': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'menarca': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'otros': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'partos': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'antecedente_quirurgico'", 'primary_key': 'True', 'to': u"orm['persona.Persona']"}),
            'ultimo_periodo': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'persona.antecedentequirurgico': {
            'Meta': {'object_name': 'AntecedenteQuirurgico'},
            'fecha': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'hospitalizacion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
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
            'fotografia': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
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