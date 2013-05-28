# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ItemTemplate.medicamento'
        db.add_column(u'inventory_itemtemplate', 'medicamento',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Item.cantidad'
        db.add_column(u'inventory_item', 'cantidad',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ItemTemplate.medicamento'
        db.delete_column(u'inventory_itemtemplate', 'medicamento')

        # Deleting field 'Item.cantidad'
        db.delete_column(u'inventory_item', 'cantidad')


    models = {
        u'inventory.inventario': {
            'Meta': {'object_name': 'Inventario'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'localidad': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'inventarios'", 'null': 'True', 'to': u"orm['inventory.Localidad']"})
        },
        u'inventory.item': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Item'},
            'cantidad': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inventario': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': u"orm['inventory.Inventario']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'plantilla': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': u"orm['inventory.ItemTemplate']"})
        },
        u'inventory.itemtemplate': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'ItemTemplate'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'emergencia': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marca': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'medicamento': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modelo': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'notas': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'numero_de_parte': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'suppliers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'plantillas'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['inventory.Proveedor']"})
        },
        u'inventory.localidad': {
            'Meta': {'object_name': 'Localidad'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'inventory.proveedor': {
            'Meta': {'object_name': 'Proveedor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'inventory.requisicion': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Requisicion'},
            'aprobada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cantidad': ('django.db.models.fields.IntegerField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'entregada': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inventario': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requisiciones'", 'to': u"orm['inventory.Inventario']"}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requisiciones'", 'to': u"orm['inventory.ItemTemplate']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        u'inventory.transferencia': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Transferencia'},
            'aplicada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cantidad': ('django.db.models.fields.IntegerField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'destino': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entradas'", 'to': u"orm['inventory.Inventario']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transferencias'", 'to': u"orm['inventory.ItemTemplate']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'origen': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'salidas'", 'to': u"orm['inventory.Inventario']"})
        }
    }

    complete_apps = ['inventory']