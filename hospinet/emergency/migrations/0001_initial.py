# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Emergencia'
        db.create_table('emergency_emergencia', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(related_name='emergencias', to=orm['persona.Persona'])),
            ('hallazgos', self.gf('django.db.models.fields.TextField')()),
            ('diagnostico', self.gf('django.db.models.fields.TextField')()),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='er_examenes', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('emergency', ['Emergencia'])

        # Adding model 'Tratamiento'
        db.create_table('emergency_tratamiento', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('emergencia', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tratamientos', to=orm['emergency.Emergencia'])),
            ('indicaciones', self.gf('django.db.models.fields.TextField')()),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='er_tratamientos', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('emergency', ['Tratamiento'])

        # Adding model 'Hallazgo'
        db.create_table('emergency_hallazgo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('emergencia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['emergency.Emergencia'])),
            ('hallazgo', self.gf('django.db.models.fields.TextField')()),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='hallazgos', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('emergency', ['Hallazgo'])

        # Adding model 'RemisionInterna'
        db.create_table('emergency_remisioninterna', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('emergencia', self.gf('django.db.models.fields.related.ForeignKey')(related_name='remisiones_internas', to=orm['emergency.Emergencia'])),
            ('doctor', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='er_rinternas', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('emergency', ['RemisionInterna'])

        # Adding model 'RemisionExterna'
        db.create_table('emergency_remisionexterna', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('emergencia', self.gf('django.db.models.fields.related.ForeignKey')(related_name='remisiones_externas', to=orm['emergency.Emergencia'])),
            ('destino', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('diagnostico', self.gf('django.db.models.fields.TextField')()),
            ('notas', self.gf('django.db.models.fields.TextField')()),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='er_rexternas', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('emergency', ['RemisionExterna'])


    def backwards(self, orm):
        # Deleting model 'Emergencia'
        db.delete_table('emergency_emergencia')

        # Deleting model 'Tratamiento'
        db.delete_table('emergency_tratamiento')

        # Deleting model 'Hallazgo'
        db.delete_table('emergency_hallazgo')

        # Deleting model 'RemisionInterna'
        db.delete_table('emergency_remisioninterna')

        # Deleting model 'RemisionExterna'
        db.delete_table('emergency_remisionexterna')


    models = {
        'actstream.action': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'Action'},
            'action_object_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'action_object'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'action_object_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'actor_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actor'", 'to': "orm['contenttypes.ContentType']"}),
            'actor_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'target_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'target'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'target_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'verb': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
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
        'emergency.emergencia': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Emergencia'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'diagnostico': ('django.db.models.fields.TextField', [], {}),
            'hallazgos': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'emergencias'", 'to': "orm['persona.Persona']"}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'er_examenes'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'emergency.hallazgo': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Hallazgo'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'emergencia': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['emergency.Emergencia']"}),
            'hallazgo': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'hallazgos'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'emergency.remisionexterna': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'RemisionExterna'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'destino': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'diagnostico': ('django.db.models.fields.TextField', [], {}),
            'emergencia': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'remisiones_externas'", 'to': "orm['emergency.Emergencia']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'notas': ('django.db.models.fields.TextField', [], {}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'er_rexternas'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'emergency.remisioninterna': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'RemisionInterna'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'doctor': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'emergencia': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'remisiones_internas'", 'to': "orm['emergency.Emergencia']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'er_rinternas'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'emergency.tratamiento': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Tratamiento'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'emergencia': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tratamientos'", 'to': "orm['emergency.Emergencia']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicaciones': ('django.db.models.fields.TextField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'er_tratamientos'", 'null': 'True', 'to': "orm['auth.User']"})
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

    complete_apps = ['emergency']