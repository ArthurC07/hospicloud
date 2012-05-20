# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Consultorio'
        db.create_table('clinique_consultorio', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('secretaria', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='secretariados', null=True, to=orm['users.Profile'])),
            ('doctor', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='consultorios', null=True, to=orm['users.Profile'])),
        ))
        db.send_create_signal('clinique', ['Consultorio'])

        # Adding model 'Paciente'
        db.create_table('clinique_paciente', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(related_name='consultorios', to=orm['persona.Persona'])),
            ('consultorio', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pacientes', to=orm['clinique.Consultorio'])),
        ))
        db.send_create_signal('clinique', ['Paciente'])

        # Adding model 'Transaccion'
        db.create_table('clinique_transaccion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('paciente', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transacciones', to=orm['clinique.Paciente'])),
            ('concepto', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('tipo', self.gf('django.db.models.fields.IntegerField')()),
            ('monto', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('fecha_y_hora', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('clinique', ['Transaccion'])

        # Adding model 'Cita'
        db.create_table('clinique_cita', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('consultorio', self.gf('django.db.models.fields.related.ForeignKey')(related_name='citas', to=orm['clinique.Consultorio'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('fecha_y_hora', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 5, 20, 0, 0))),
        ))
        db.send_create_signal('clinique', ['Cita'])

        # Adding model 'Esperador'
        db.create_table('clinique_esperador', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('consultorio', self.gf('django.db.models.fields.related.ForeignKey')(related_name='esperadores', to=orm['clinique.Consultorio'])),
            ('paciente', self.gf('django.db.models.fields.related.ForeignKey')(related_name='esperas', to=orm['clinique.Paciente'])),
            ('atendido', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('clinique', ['Esperador'])


    def backwards(self, orm):
        # Deleting model 'Consultorio'
        db.delete_table('clinique_consultorio')

        # Deleting model 'Paciente'
        db.delete_table('clinique_paciente')

        # Deleting model 'Transaccion'
        db.delete_table('clinique_transaccion')

        # Deleting model 'Cita'
        db.delete_table('clinique_cita')

        # Deleting model 'Esperador'
        db.delete_table('clinique_esperador')


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
        'clinique.cita': {
            'Meta': {'object_name': 'Cita'},
            'consultorio': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'citas'", 'to': "orm['clinique.Consultorio']"}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 20, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'clinique.consultorio': {
            'Meta': {'object_name': 'Consultorio'},
            'doctor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'consultorios'", 'null': 'True', 'to': "orm['users.Profile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'secretaria': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'secretariados'", 'null': 'True', 'to': "orm['users.Profile']"})
        },
        'clinique.esperador': {
            'Meta': {'object_name': 'Esperador'},
            'atendido': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'consultorio': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'esperadores'", 'to': "orm['clinique.Consultorio']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paciente': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'esperas'", 'to': "orm['clinique.Paciente']"})
        },
        'clinique.paciente': {
            'Meta': {'object_name': 'Paciente'},
            'consultorio': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pacientes'", 'to': "orm['clinique.Consultorio']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'consultorios'", 'to': "orm['persona.Persona']"})
        },
        'clinique.transaccion': {
            'Meta': {'object_name': 'Transaccion'},
            'concepto': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monto': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'paciente': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transacciones'", 'to': "orm['clinique.Paciente']"}),
            'tipo': ('django.db.models.fields.IntegerField', [], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
        },
        'users.profile': {
            'Meta': {'object_name': 'Profile'},
            'doctor': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'suscripcion': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['clinique']