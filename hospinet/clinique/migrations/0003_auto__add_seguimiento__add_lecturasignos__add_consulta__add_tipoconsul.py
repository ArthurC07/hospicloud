# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Seguimiento'
        db.create_table(u'clinique_seguimiento', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('paciente', self.gf('django.db.models.fields.related.ForeignKey')(related_name='seguimientos', to=orm['clinique.Paciente'])),
            ('observaciones', self.gf('django.db.models.fields.TextField')()),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(related_name='seguimientos', to=orm['auth.User'])),
        ))
        db.send_create_signal(u'clinique', ['Seguimiento'])

        # Adding model 'LecturaSignos'
        db.create_table(u'clinique_lecturasignos', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('paciente', self.gf('django.db.models.fields.related.ForeignKey')(related_name='signos_vitales', to=orm['clinique.Paciente'])),
            ('pulso', self.gf('django.db.models.fields.IntegerField')()),
            ('temperatura', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2)),
            ('presion_sistolica', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2)),
            ('presion_diastolica', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2)),
            ('respiracion', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2)),
            ('presion_arterial_media', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'clinique', ['LecturaSignos'])

        # Adding model 'Consulta'
        db.create_table(u'clinique_consulta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('paciente', self.gf('django.db.models.fields.related.ForeignKey')(related_name='consultas', to=orm['clinique.Paciente'])),
            ('tipo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='consultas', to=orm['clinique.TipoConsulta'])),
            ('padecimiento', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'clinique', ['Consulta'])

        # Adding model 'TipoConsulta'
        db.create_table(u'clinique_tipoconsulta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'clinique', ['TipoConsulta'])

        # Adding model 'Cita'
        db.create_table(u'clinique_cita', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(related_name='citas', to=orm['auth.User'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('fecha', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'clinique', ['Cita'])

        # Adding model 'Paciente'
        db.create_table(u'clinique_paciente', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pacientes', to=orm['persona.Persona'])),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pacientes', to=orm['auth.User'])),
        ))
        db.send_create_signal(u'clinique', ['Paciente'])

        # Adding model 'Evaluacion'
        db.create_table(u'clinique_evaluacion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('paciente', self.gf('django.db.models.fields.related.ForeignKey')(related_name='examenes_fisicos', to=orm['clinique.Paciente'])),
            ('orl', self.gf('django.db.models.fields.TextField')()),
            ('cardiopulmonar', self.gf('django.db.models.fields.TextField')()),
            ('gastrointestinal', self.gf('django.db.models.fields.TextField')()),
            ('extremidades', self.gf('django.db.models.fields.TextField')()),
            ('otras', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'clinique', ['Evaluacion'])


    def backwards(self, orm):
        # Deleting model 'Seguimiento'
        db.delete_table(u'clinique_seguimiento')

        # Deleting model 'LecturaSignos'
        db.delete_table(u'clinique_lecturasignos')

        # Deleting model 'Consulta'
        db.delete_table(u'clinique_consulta')

        # Deleting model 'TipoConsulta'
        db.delete_table(u'clinique_tipoconsulta')

        # Deleting model 'Cita'
        db.delete_table(u'clinique_cita')

        # Deleting model 'Paciente'
        db.delete_table(u'clinique_paciente')

        # Deleting model 'Evaluacion'
        db.delete_table(u'clinique_evaluacion')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'clinique.cita': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Cita'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'citas'", 'to': u"orm['auth.User']"})
        },
        u'clinique.consulta': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Consulta'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'paciente': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'consultas'", 'to': u"orm['clinique.Paciente']"}),
            'padecimiento': ('django.db.models.fields.TextField', [], {}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'consultas'", 'to': u"orm['clinique.TipoConsulta']"})
        },
        u'clinique.evaluacion': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Evaluacion'},
            'cardiopulmonar': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'extremidades': ('django.db.models.fields.TextField', [], {}),
            'gastrointestinal': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'orl': ('django.db.models.fields.TextField', [], {}),
            'otras': ('django.db.models.fields.TextField', [], {}),
            'paciente': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'examenes_fisicos'", 'to': u"orm['clinique.Paciente']"})
        },
        u'clinique.lecturasignos': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'LecturaSignos'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'paciente': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'signos_vitales'", 'to': u"orm['clinique.Paciente']"}),
            'presion_arterial_media': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'presion_diastolica': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2'}),
            'presion_sistolica': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2'}),
            'pulso': ('django.db.models.fields.IntegerField', [], {}),
            'respiracion': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2'}),
            'temperatura': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2'})
        },
        u'clinique.paciente': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Paciente'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pacientes'", 'to': u"orm['persona.Persona']"}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pacientes'", 'to': u"orm['auth.User']"})
        },
        u'clinique.seguimiento': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Seguimiento'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'observaciones': ('django.db.models.fields.TextField', [], {}),
            'paciente': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'seguimientos'", 'to': u"orm['clinique.Paciente']"}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'seguimientos'", 'to': u"orm['auth.User']"})
        },
        u'clinique.tipoconsulta': {
            'Meta': {'object_name': 'TipoConsulta'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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

    complete_apps = ['clinique']