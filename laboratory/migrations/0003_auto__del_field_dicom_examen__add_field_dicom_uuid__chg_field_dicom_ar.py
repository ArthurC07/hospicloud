# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Dicom.examen'
        db.delete_column('laboratory_dicom', 'examen_id')

        # Adding field 'Dicom.uuid'
        db.add_column('laboratory_dicom', 'uuid',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=36, blank=True),
                      keep_default=False)


        # Changing field 'Dicom.archivo'
        db.alter_column('laboratory_dicom', 'archivo', self.gf('private_files.models.fields.PrivateFileField')(max_length=100))

        # Changing field 'Dicom.imagen'
        db.alter_column('laboratory_dicom', 'imagen', self.gf('private_files.models.fields.PrivateFileField')(max_length=100))

    def backwards(self, orm):
        # Adding field 'Dicom.examen'
        db.add_column('laboratory_dicom', 'examen',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='dicoms', null=True, to=orm['laboratory.Examen'], blank=True),
                      keep_default=False)

        # Deleting field 'Dicom.uuid'
        db.delete_column('laboratory_dicom', 'uuid')


        # Changing field 'Dicom.archivo'
        db.alter_column('laboratory_dicom', 'archivo', self.gf('django.db.models.fields.files.FileField')(max_length=100))

        # Changing field 'Dicom.imagen'
        db.alter_column('laboratory_dicom', 'imagen', self.gf('django.db.models.fields.files.ImageField')(max_length=100))

    models = {
        'laboratory.adjunto': {
            'Meta': {'object_name': 'Adjunto'},
            'archivo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'examen': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'adjuntos'", 'to': "orm['laboratory.Examen']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'laboratory.dicom': {
            'Meta': {'object_name': 'Dicom'},
            'archivo': ('private_files.models.fields.PrivateFileField', [], {'max_length': '100'}),
            'convertido': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('private_files.models.fields.PrivateFileField', [], {'max_length': '100', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        'laboratory.examen': {
            'Meta': {'object_name': 'Examen'},
            'diagnostico': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'examenes'", 'to': "orm['persona.Persona']"}),
            'resultado': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'laboratory.imagen': {
            'Meta': {'object_name': 'Imagen'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'examen': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'imagenes'", 'to': "orm['laboratory.Examen']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'})
        },
        'persona.persona': {
            'Meta': {'object_name': 'Persona'},
            'antiguedad': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'apellido': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'cargo': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'celular': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'centro_trabajo': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'ci': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'direccion_trabajo': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'domicilio': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'estado_civil': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'fotografia': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identificacion': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20', 'blank': 'True'}),
            'nacimiento': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'nacionalidad': ('persona.fields.OrderedCountryField', [], {'max_length': '2', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'profesion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'sexo': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'tel_trabajo': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'tipo_identificacion': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'})
        }
    }

    complete_apps = ['laboratory']