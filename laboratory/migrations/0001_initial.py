# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Examen'
        db.create_table('laboratory_examen', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(related_name='examenes', to=orm['persona.Persona'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('resultado', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('diagnostico', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('fecha', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('laboratory', ['Examen'])

        # Adding model 'Imagen'
        db.create_table('laboratory_imagen', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('examen', self.gf('django.db.models.fields.related.ForeignKey')(related_name='imagenes', to=orm['laboratory.Examen'])),
            ('imagen', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('laboratory', ['Imagen'])

        # Adding model 'Adjunto'
        db.create_table('laboratory_adjunto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('examen', self.gf('django.db.models.fields.related.ForeignKey')(related_name='adjuntos', to=orm['laboratory.Examen'])),
            ('archivo', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('laboratory', ['Adjunto'])

        # Adding model 'Dicom'
        db.create_table('laboratory_dicom', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('archivo', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('convertido', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('imagen', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('laboratory', ['Dicom'])


    def backwards(self, orm):
        
        # Deleting model 'Examen'
        db.delete_table('laboratory_examen')

        # Deleting model 'Imagen'
        db.delete_table('laboratory_imagen')

        # Deleting model 'Adjunto'
        db.delete_table('laboratory_adjunto')

        # Deleting model 'Dicom'
        db.delete_table('laboratory_dicom')


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
            'archivo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'convertido': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
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
