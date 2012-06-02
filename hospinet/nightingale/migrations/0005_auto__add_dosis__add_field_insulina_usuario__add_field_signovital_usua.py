# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Dosis'
        db.create_table('nightingale_dosis', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('medicamento', self.gf('django.db.models.fields.related.ForeignKey')(related_name='dosis', to=orm['nightingale.Medicamento'])),
            ('momento', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now)),
            ('suministrada', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='dosis', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('nightingale', ['Dosis'])

        # Adding field 'Insulina.usuario'
        db.add_column('nightingale_insulina', 'usuario',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='insulinas', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'SignoVital.usuario'
        db.add_column('nightingale_signovital', 'usuario',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='signos_vitales', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Evolucion.usuario'
        db.add_column('nightingale_evolucion', 'usuario',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='evoluciones', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Cargo.usuario'
        db.add_column('nightingale_cargo', 'usuario',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='cargos', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'NotaEnfermeria.usuario'
        db.add_column('nightingale_notaenfermeria', 'usuario',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='notas_enfermeria', null=True, to=orm['auth.User']),
                      keep_default=False)


        # Changing field 'NotaEnfermeria.nota'
        db.alter_column('nightingale_notaenfermeria', 'nota', self.gf('django.db.models.fields.TextField')())
        # Adding field 'Ingesta.usuario'
        db.add_column('nightingale_ingesta', 'usuario',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='ingestas', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Sumario.usuario'
        db.add_column('nightingale_sumario', 'usuario',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='sumarios', null=True, to=orm['auth.User']),
                      keep_default=False)


        # Changing field 'Sumario.diagnostico'
        db.alter_column('nightingale_sumario', 'diagnostico', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Sumario.procedimiento_efectuado'
        db.alter_column('nightingale_sumario', 'procedimiento_efectuado', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Sumario.condicion'
        db.alter_column('nightingale_sumario', 'condicion', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Sumario.recomendaciones'
        db.alter_column('nightingale_sumario', 'recomendaciones', self.gf('django.db.models.fields.TextField')())
        # Adding field 'OrdenMedica.usuario'
        db.add_column('nightingale_ordenmedica', 'usuario',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='ordenes_medicas', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Deleting field 'Medicamento.hora'
        db.delete_column('nightingale_medicamento', 'hora')

        # Deleting field 'Medicamento.medicamento'
        db.delete_column('nightingale_medicamento', 'medicamento')

        # Adding field 'Medicamento.nombre'
        db.add_column('nightingale_medicamento', 'nombre',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Medicamento.inicio'
        db.add_column('nightingale_medicamento', 'inicio',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Medicamento.intervalo'
        db.add_column('nightingale_medicamento', 'intervalo',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Medicamento.dias'
        db.add_column('nightingale_medicamento', 'dias',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Medicamento.control'
        db.add_column('nightingale_medicamento', 'control',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Medicamento.usuario'
        db.add_column('nightingale_medicamento', 'usuario',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='medicamentos', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Glucosuria.usuario'
        db.add_column('nightingale_glucosuria', 'usuario',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='glucosurias', null=True, to=orm['auth.User']),
                      keep_default=False)


        # Changing field 'Glucosuria.observacion'
        db.alter_column('nightingale_glucosuria', 'observacion', self.gf('django.db.models.fields.TextField')())
        # Adding field 'Excreta.usuario'
        db.add_column('nightingale_excreta', 'usuario',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='excretas', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Glicemia.usuario'
        db.add_column('nightingale_glicemia', 'usuario',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='glicemias', null=True, to=orm['auth.User']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Dosis'
        db.delete_table('nightingale_dosis')

        # Deleting field 'Insulina.usuario'
        db.delete_column('nightingale_insulina', 'usuario_id')

        # Deleting field 'SignoVital.usuario'
        db.delete_column('nightingale_signovital', 'usuario_id')

        # Deleting field 'Evolucion.usuario'
        db.delete_column('nightingale_evolucion', 'usuario_id')

        # Deleting field 'Cargo.usuario'
        db.delete_column('nightingale_cargo', 'usuario_id')

        # Deleting field 'NotaEnfermeria.usuario'
        db.delete_column('nightingale_notaenfermeria', 'usuario_id')


        # Changing field 'NotaEnfermeria.nota'
        db.alter_column('nightingale_notaenfermeria', 'nota', self.gf('django.db.models.fields.CharField')(max_length=200))
        # Deleting field 'Ingesta.usuario'
        db.delete_column('nightingale_ingesta', 'usuario_id')

        # Deleting field 'Sumario.usuario'
        db.delete_column('nightingale_sumario', 'usuario_id')


        # Changing field 'Sumario.diagnostico'
        db.alter_column('nightingale_sumario', 'diagnostico', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Sumario.procedimiento_efectuado'
        db.alter_column('nightingale_sumario', 'procedimiento_efectuado', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Sumario.condicion'
        db.alter_column('nightingale_sumario', 'condicion', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Sumario.recomendaciones'
        db.alter_column('nightingale_sumario', 'recomendaciones', self.gf('django.db.models.fields.CharField')(max_length=200))
        # Deleting field 'OrdenMedica.usuario'
        db.delete_column('nightingale_ordenmedica', 'usuario_id')

        # Adding field 'Medicamento.hora'
        db.add_column('nightingale_medicamento', 'hora',
                      self.gf('django.db.models.fields.TimeField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Medicamento.medicamento'
        db.add_column('nightingale_medicamento', 'medicamento',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Medicamento.nombre'
        db.delete_column('nightingale_medicamento', 'nombre')

        # Deleting field 'Medicamento.inicio'
        db.delete_column('nightingale_medicamento', 'inicio')

        # Deleting field 'Medicamento.intervalo'
        db.delete_column('nightingale_medicamento', 'intervalo')

        # Deleting field 'Medicamento.dias'
        db.delete_column('nightingale_medicamento', 'dias')

        # Deleting field 'Medicamento.control'
        db.delete_column('nightingale_medicamento', 'control')

        # Deleting field 'Medicamento.usuario'
        db.delete_column('nightingale_medicamento', 'usuario_id')

        # Deleting field 'Glucosuria.usuario'
        db.delete_column('nightingale_glucosuria', 'usuario_id')


        # Changing field 'Glucosuria.observacion'
        db.alter_column('nightingale_glucosuria', 'observacion', self.gf('django.db.models.fields.CharField')(max_length=200))
        # Deleting field 'Excreta.usuario'
        db.delete_column('nightingale_excreta', 'usuario_id')

        # Deleting field 'Glicemia.usuario'
        db.delete_column('nightingale_glicemia', 'usuario_id')


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
        'nightingale.cargo': {
            'Meta': {'object_name': 'Cargo'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cargos'", 'to': "orm['spital.Admision']"}),
            'cargo': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'fin': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inicio': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cargos'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'nightingale.dosis': {
            'Meta': {'object_name': 'Dosis'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medicamento': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dosis'", 'to': "orm['nightingale.Medicamento']"}),
            'momento': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'suministrada': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'dosis'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'nightingale.evolucion': {
            'Meta': {'object_name': 'Evolucion'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'evoluciones'", 'to': "orm['spital.Admision']"}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nota': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'evoluciones'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'nightingale.excreta': {
            'Meta': {'object_name': 'Excreta'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'excretas'", 'to': "orm['spital.Admision']"}),
            'cantidad': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medio': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'otro': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'otros': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'excretas'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'nightingale.frecuencialectura': {
            'Meta': {'object_name': 'FrecuenciaLectura'},
            'admision': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['spital.Admision']", 'unique': 'True'}),
            'glucometria': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'signos_vitales': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        'nightingale.glicemia': {
            'Meta': {'object_name': 'Glicemia'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'glicemias'", 'to': "orm['spital.Admision']"}),
            'control': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'glicemias'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'nightingale.glucosuria': {
            'Meta': {'object_name': 'Glucosuria'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'glucosurias'", 'to': "orm['spital.Admision']"}),
            'control': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'glucosurias'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'nightingale.ingesta': {
            'Meta': {'object_name': 'Ingesta'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ingestas'", 'to': "orm['spital.Admision']"}),
            'cantidad': ('django.db.models.fields.IntegerField', [], {}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingerido': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'liquido': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ingestas'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'nightingale.insulina': {
            'Meta': {'object_name': 'Insulina'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'insulina'", 'to': "orm['spital.Admision']"}),
            'control': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'insulinas'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'nightingale.medicamento': {
            'Meta': {'object_name': 'Medicamento'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'medicamentos'", 'to': "orm['spital.Admision']"}),
            'control': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'dias': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inicio': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'intervalo': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'medicamentos'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'nightingale.notaenfermeria': {
            'Meta': {'object_name': 'NotaEnfermeria'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notas_enfermeria'", 'to': "orm['spital.Admision']"}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nota': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'notas_enfermeria'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'nightingale.ordenmedica': {
            'Meta': {'object_name': 'OrdenMedica'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ordenes_medicas'", 'to': "orm['spital.Admision']"}),
            'doctor': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orden': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ordenes_medicas'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'nightingale.signovital': {
            'Meta': {'object_name': 'SignoVital'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'signos_vitales'", 'to': "orm['spital.Admision']"}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2'}),
            'presion_arterial_media': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'presion_diastolica': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2'}),
            'presion_sistolica': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2'}),
            'pulso': ('django.db.models.fields.IntegerField', [], {}),
            'respiracion': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2'}),
            'saturacion_de_oxigeno': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2'}),
            'temperatura': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'signos_vitales'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'nightingale.sumario': {
            'Meta': {'object_name': 'Sumario'},
            'admision': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['spital.Admision']", 'unique': 'True'}),
            'condicion': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'diagnostico': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'procedimiento_efectuado': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'recomendaciones': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sumarios'", 'null': 'True', 'to': "orm['auth.User']"})
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
        },
        'spital.admision': {
            'Meta': {'object_name': 'Admision'},
            'admision': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'admitio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'arancel': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'aseguradora': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'autorizacion': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'certificado': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'codigo': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'deposito': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'diagnostico': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'doctor': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'estado': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'fecha_alta': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'fecha_pago': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'fiadores': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'fianzas'", 'symmetrical': 'False', 'to': "orm['persona.Persona']"}),
            'habitacion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'hospitalizacion': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingreso': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'momento': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'neonato': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'observaciones': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'paciente': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'admisiones'", 'to': "orm['persona.Persona']"}),
            'pago': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'poliza': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'qr': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'referencias': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'referencias'", 'symmetrical': 'False', 'to': "orm['persona.Persona']"}),
            'tiempo': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'tipo_de_habitacion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'tipo_de_ingreso': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        }
    }

    complete_apps = ['nightingale']