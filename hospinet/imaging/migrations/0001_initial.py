# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Remision'
        db.create_table('imaging_remision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='Remisiones', null=True, to=orm['auth.User'])),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(related_name='remisiones', to=orm['persona.Persona'])),
            ('fecha', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('examen', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('efectuado', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
        ))
        db.send_create_signal('imaging', ['Remision'])

        # Adding model 'Examen'
        db.create_table('imaging_examen', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(related_name='examenes', to=orm['persona.Persona'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('resultado', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('diagnostico', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('fecha', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
        ))
        db.send_create_signal('imaging', ['Examen'])

        # Adding model 'Imagen'
        db.create_table('imaging_imagen', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('examen', self.gf('django.db.models.fields.related.ForeignKey')(related_name='imagenes', to=orm['imaging.Examen'])),
            ('imagen', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('imaging', ['Imagen'])

        # Adding model 'Adjunto'
        db.create_table('imaging_adjunto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('examen', self.gf('django.db.models.fields.related.ForeignKey')(related_name='adjuntos', to=orm['imaging.Examen'])),
            ('archivo', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('imaging', ['Adjunto'])

        # Adding model 'Dicom'
        db.create_table('imaging_dicom', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('examen', self.gf('django.db.models.fields.related.ForeignKey')(related_name='dicoms', to=orm['imaging.Examen'])),
            ('archivo', self.gf('private_files.models.fields.PrivateFileField')(max_length=100)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('convertido', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('imagen', self.gf('private_files.models.fields.PrivateFileField')(max_length=100, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
        ))
        db.send_create_signal('imaging', ['Dicom'])


    def backwards(self, orm):
        # Deleting model 'Remision'
        db.delete_table('imaging_remision')

        # Deleting model 'Examen'
        db.delete_table('imaging_examen')

        # Deleting model 'Imagen'
        db.delete_table('imaging_imagen')

        # Deleting model 'Adjunto'
        db.delete_table('imaging_adjunto')

        # Deleting model 'Dicom'
        db.delete_table('imaging_dicom')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'imaging.adjunto': {
            'Meta': {'object_name': 'Adjunto'},
            'archivo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'examen': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'adjuntos'", 'to': "orm['imaging.Examen']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'imaging.dicom': {
            'Meta': {'object_name': 'Dicom'},
            'archivo': ('private_files.models.fields.PrivateFileField', [], {'max_length': '100'}),
            'convertido': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'examen': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dicoms'", 'to': "orm['imaging.Examen']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('private_files.models.fields.PrivateFileField', [], {'max_length': '100', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        'imaging.examen': {
            'Meta': {'object_name': 'Examen'},
            'diagnostico': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'examenes'", 'to': "orm['persona.Persona']"}),
            'resultado': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        'imaging.imagen': {
            'Meta': {'object_name': 'Imagen'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'examen': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'imagenes'", 'to': "orm['imaging.Examen']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'})
        },
        'imaging.remision': {
            'Meta': {'object_name': 'Remision'},
            'efectuado': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'examen': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'fecha': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'remisiones'", 'to': "orm['persona.Persona']"}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'Remisiones'", 'null': 'True', 'to': "orm['auth.User']"})
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
            'identificacion': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
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

    complete_apps = ['imaging']