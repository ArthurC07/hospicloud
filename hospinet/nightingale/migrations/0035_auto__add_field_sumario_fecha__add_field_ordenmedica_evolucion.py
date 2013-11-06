# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Sumario.fecha'
        db.add_column(u'nightingale_sumario', 'fecha',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'OrdenMedica.evolucion'
        db.add_column(u'nightingale_ordenmedica', 'evolucion',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Sumario.fecha'
        db.delete_column(u'nightingale_sumario', 'fecha')

        # Deleting field 'OrdenMedica.evolucion'
        db.delete_column(u'nightingale_ordenmedica', 'evolucion')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'inventory.itemtemplate': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'ItemTemplate'},
            'activo': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'comision': ('django.db.models.fields.DecimalField', [], {'default': "'30.00'", 'max_digits': '4', 'decimal_places': '2'}),
            'costo': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impuestos': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'item_type': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'items'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['inventory.ItemType']"}),
            'marca': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'modelo': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'notas': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'precio_de_venta': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'suppliers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'plantillas'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['inventory.Proveedor']"}),
            'unidad_de_medida': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'})
        },
        u'inventory.itemtype': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'ItemType'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'inventory.proveedor': {
            'Meta': {'object_name': 'Proveedor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'inventory.tipoventa': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'TipoVenta'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'disminucion': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incremento': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        u'nightingale.cargo': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Cargo'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cargos'", 'to': u"orm['spital.Admision']"}),
            'cantidad': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '8', 'decimal_places': '2'}),
            'cargo': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cargos'", 'null': 'True', 'to': u"orm['inventory.ItemTemplate']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'facturada': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cargos'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'nightingale.devolucion': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Devolucion'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'devoluciones'", 'to': u"orm['spital.Admision']"}),
            'cargo': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'devoluciones'", 'null': 'True', 'to': u"orm['inventory.ItemTemplate']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'descripcion': ('django.db.models.fields.TextField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'devoluciones'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'nightingale.dosis': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Dosis'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'estado': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medicamento': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dosis'", 'to': u"orm['nightingale.Medicamento']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'recomendacion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'dosis'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'nightingale.evolucion': {
            'Meta': {'object_name': 'Evolucion'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'evoluciones'", 'to': u"orm['spital.Admision']"}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nota': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'evoluciones'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'nightingale.excreta': {
            'Meta': {'object_name': 'Excreta'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'excretas'", 'to': u"orm['spital.Admision']"}),
            'cantidad': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medio': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'otro': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'otros': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'excretas'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'nightingale.frecuencialectura': {
            'Meta': {'object_name': 'FrecuenciaLectura'},
            'admision': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['spital.Admision']", 'unique': 'True'}),
            'glucometria': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'signos_vitales': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        u'nightingale.glicemia': {
            'Meta': {'object_name': 'Glicemia'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'glicemias'", 'to': u"orm['spital.Admision']"}),
            'control': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'glicemias'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'nightingale.glucosuria': {
            'Meta': {'object_name': 'Glucosuria'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'glucosurias'", 'to': u"orm['spital.Admision']"}),
            'control': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'glucosurias'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'nightingale.honorario': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Honorario'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'honorarios'", 'to': u"orm['spital.Admision']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'facturada': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'honorarios'", 'null': 'True', 'to': u"orm['inventory.ItemTemplate']"}),
            'medico': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'monto': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'honorarios'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'nightingale.ingesta': {
            'Meta': {'object_name': 'Ingesta'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ingestas'", 'to': u"orm['spital.Admision']"}),
            'cantidad': ('django.db.models.fields.IntegerField', [], {}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingerido': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'liquido': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ingestas'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'via': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'nightingale.insulina': {
            'Meta': {'object_name': 'Insulina'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'insulina'", 'to': u"orm['spital.Admision']"}),
            'control': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'insulinas'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'nightingale.medicamento': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Medicamento'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'medicamentos'", 'to': u"orm['spital.Admision']"}),
            'cargo': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'medicamentos'", 'null': 'True', 'to': u"orm['inventory.ItemTemplate']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'estado': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inicio': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'intervalo': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'proxima_dosis': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'repeticiones': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'suministrado': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'ultima_dosis': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'unidades': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'medicamentos'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'nightingale.notaenfermeria': {
            'Meta': {'object_name': 'NotaEnfermeria'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notas_enfermeria'", 'to': u"orm['spital.Admision']"}),
            'autor': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'cerrada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nota': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'notas_enfermeria'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'nightingale.ordenmedica': {
            'Meta': {'object_name': 'OrdenMedica'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ordenes_medicas'", 'to': u"orm['spital.Admision']"}),
            'doctor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'evolucion': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orden': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ordenes_medicas'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'nightingale.oxigenoterapia': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'OxigenoTerapia'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'oxigeno_terapias'", 'to': u"orm['spital.Admision']"}),
            'cargo': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'oxigeno_terapias'", 'null': 'True', 'to': u"orm['inventory.ItemTemplate']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'facturada': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'terminada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'unidades_por_minuto': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'nightingale.signovital': {
            'Meta': {'object_name': 'SignoVital'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'signos_vitales'", 'to': u"orm['spital.Admision']"}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'presion_arterial_media': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'presion_diastolica': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2'}),
            'presion_sistolica': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2'}),
            'pulso': ('django.db.models.fields.IntegerField', [], {}),
            'respiracion': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2'}),
            'saturacion_de_oxigeno': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2'}),
            'temperatura': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'signos_vitales'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'nightingale.sumario': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Sumario'},
            'admision': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['spital.Admision']", 'unique': 'True'}),
            'condicion': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'diagnostico': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'procedimiento_efectuado': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'recomendaciones': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sumarios'", 'null': 'True', 'to': u"orm['auth.User']"})
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
        },
        u'spital.admision': {
            'Meta': {'object_name': 'Admision'},
            'admision': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'admitio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'arancel': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'aseguradora': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'autorizacion': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'certificado': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'deposito': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'diagnostico': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'doctor': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'estado': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'facturada': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'fecha_alta': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'fecha_pago': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'fiadores': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'fianzas'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['persona.Persona']"}),
            'habitacion': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'admisiones'", 'null': 'True', 'to': u"orm['spital.Habitacion']"}),
            'hospitalizacion': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingreso': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'momento': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'neonato': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'observaciones': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'paciente': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'admisiones'", 'to': u"orm['persona.Persona']"}),
            'pago': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'poliza': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'referencias': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'referencias'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['persona.Persona']"}),
            'tiempo': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'tipo_de_ingreso': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'tipo_de_venta': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.TipoVenta']", 'null': 'True', 'blank': 'True'}),
            'ultimo_cobro': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        u'spital.habitacion': {
            'Meta': {'object_name': 'Habitacion'},
            'estado': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'habitaciones'", 'null': 'True', 'to': u"orm['inventory.ItemTemplate']"}),
            'numero': ('django.db.models.fields.IntegerField', [], {}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'})
        }
    }

    complete_apps = ['nightingale']