# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Cobro'
        db.create_table('emergency_cobro', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('emergencia', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cobros', to=orm['emergency.Emergencia'])),
            ('cargo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cobros', to=orm['inventory.ItemTemplate'])),
        ))
        db.send_create_signal('emergency', ['Cobro'])

        # Deleting field 'Emergencia.hallazgos'
        db.delete_column('emergency_emergencia', 'hallazgos')

        # Deleting field 'Emergencia.diagnostico'
        db.delete_column('emergency_emergencia', 'diagnostico')

        # Adding field 'Emergencia.historia_enfermedad_actual'
        db.add_column('emergency_emergencia', 'historia_enfermedad_actual',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Emergencia.pulso'
        db.add_column('emergency_emergencia', 'pulso',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Emergencia.temperatura'
        db.add_column('emergency_emergencia', 'temperatura',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2),
                      keep_default=False)

        # Adding field 'Emergencia.presion_sistolica'
        db.add_column('emergency_emergencia', 'presion_sistolica',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2),
                      keep_default=False)

        # Adding field 'Emergencia.presion_diastolica'
        db.add_column('emergency_emergencia', 'presion_diastolica',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2),
                      keep_default=False)

        # Adding field 'Emergencia.respiracion'
        db.add_column('emergency_emergencia', 'respiracion',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2),
                      keep_default=False)

        # Adding field 'Emergencia.observacion'
        db.add_column('emergency_emergencia', 'observacion',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Emergencia.saturacion_de_oxigeno'
        db.add_column('emergency_emergencia', 'saturacion_de_oxigeno',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2),
                      keep_default=False)

        # Adding field 'Emergencia.presion_arterial_media'
        db.add_column('emergency_emergencia', 'presion_arterial_media',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Cobro'
        db.delete_table('emergency_cobro')

        # Adding field 'Emergencia.hallazgos'
        db.add_column('emergency_emergencia', 'hallazgos',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'Emergencia.diagnostico'
        db.add_column('emergency_emergencia', 'diagnostico',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Deleting field 'Emergencia.historia_enfermedad_actual'
        db.delete_column('emergency_emergencia', 'historia_enfermedad_actual')

        # Deleting field 'Emergencia.pulso'
        db.delete_column('emergency_emergencia', 'pulso')

        # Deleting field 'Emergencia.temperatura'
        db.delete_column('emergency_emergencia', 'temperatura')

        # Deleting field 'Emergencia.presion_sistolica'
        db.delete_column('emergency_emergencia', 'presion_sistolica')

        # Deleting field 'Emergencia.presion_diastolica'
        db.delete_column('emergency_emergencia', 'presion_diastolica')

        # Deleting field 'Emergencia.respiracion'
        db.delete_column('emergency_emergencia', 'respiracion')

        # Deleting field 'Emergencia.observacion'
        db.delete_column('emergency_emergencia', 'observacion')

        # Deleting field 'Emergencia.saturacion_de_oxigeno'
        db.delete_column('emergency_emergencia', 'saturacion_de_oxigeno')

        # Deleting field 'Emergencia.presion_arterial_media'
        db.delete_column('emergency_emergencia', 'presion_arterial_media')


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
        'emergency.cobro': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Cobro'},
            'cargo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cobros'", 'to': "orm['inventory.ItemTemplate']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'emergencia': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cobros'", 'to': "orm['emergency.Emergencia']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'emergency.emergencia': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Emergencia'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'historia_enfermedad_actual': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'observacion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'emergencias'", 'to': "orm['persona.Persona']"}),
            'presion_arterial_media': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'presion_diastolica': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2'}),
            'presion_sistolica': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2'}),
            'pulso': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'respiracion': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2'}),
            'saturacion_de_oxigeno': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2'}),
            'temperatura': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2'}),
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
        'inventory.itemtemplate': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'ItemTemplate'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marca': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'modelo': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'notas': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'numero_de_parte': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'suppliers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'plantillas'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['inventory.Proveedor']"})
        },
        'inventory.proveedor': {
            'Meta': {'object_name': 'Proveedor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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