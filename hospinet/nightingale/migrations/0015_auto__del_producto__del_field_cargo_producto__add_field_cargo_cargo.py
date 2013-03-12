# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Producto'
        db.delete_table('nightingale_producto')

        # Deleting field 'Cargo.producto'
        db.delete_column('nightingale_cargo', 'producto_id')

        # Adding field 'Cargo.cargo'
        db.add_column('nightingale_cargo', 'cargo',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='cargos', null=True, to=orm['inventory.ItemTemplate']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Producto'
        db.create_table('nightingale_producto', (
            ('precio', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('impuesto', self.gf('django.db.models.fields.DecimalField')(max_digits=4, decimal_places=2)),
            ('descripcion', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('nightingale', ['Producto'])

        # Adding field 'Cargo.producto'
        db.add_column('nightingale_cargo', 'producto',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='cargos', null=True, to=orm['nightingale.Producto'], blank=True),
                      keep_default=False)

        # Deleting field 'Cargo.cargo'
        db.delete_column('nightingale_cargo', 'cargo_id')


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
        'inventory.itemtemplate': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'ItemTemplate'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'emergencia': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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
        'nightingale.cargo': {
            'Meta': {'object_name': 'Cargo'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cargos'", 'to': "orm['spital.Admision']"}),
            'cargo': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cargos'", 'null': 'True', 'to': "orm['inventory.ItemTemplate']"}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'fin': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inicio': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cargos'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'nightingale.devolucion': {
            'Meta': {'object_name': 'Devolucion'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'devoluciones'", 'to': "orm['spital.Admision']"}),
            'descripcion': ('django.db.models.fields.TextField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'devoluciones'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'nightingale.dosis': {
            'Meta': {'object_name': 'Dosis'},
            'administrador': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'dosis_administradas'", 'null': 'True', 'to': "orm['auth.User']"}),
            'estado': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medicamento': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dosis'", 'to': "orm['nightingale.Medicamento']"}),
            'recomendacion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
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
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ingestas'", 'null': 'True', 'to': "orm['auth.User']"}),
            'via': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
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
            'estado': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inicio': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'intervalo': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'medicamentos'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'nightingale.notaenfermeria': {
            'Meta': {'object_name': 'NotaEnfermeria'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notas_enfermeria'", 'to': "orm['spital.Admision']"}),
            'cerrada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nota': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'notas_enfermeria'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'nightingale.ordenmedica': {
            'Meta': {'object_name': 'OrdenMedica'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ordenes_medicas'", 'to': "orm['spital.Admision']"}),
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
            'observacion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
            'deposito': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'diagnostico': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'doctor': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'estado': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'fecha_alta': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'fecha_pago': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'fiadores': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'fianzas'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['persona.Persona']"}),
            'habitacion': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'admisiones'", 'null': 'True', 'to': "orm['spital.Habitacion']"}),
            'hospitalizacion': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingreso': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'momento': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'neonato': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'observaciones': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'paciente': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'admisiones'", 'to': "orm['persona.Persona']"}),
            'pago': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'poliza': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'referencias': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'referencias'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['persona.Persona']"}),
            'tiempo': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'tipo_de_habitacion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'tipo_de_ingreso': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        'spital.habitacion': {
            'Meta': {'object_name': 'Habitacion'},
            'estado': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero': ('django.db.models.fields.IntegerField', [], {}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'})
        }
    }

    complete_apps = ['nightingale']