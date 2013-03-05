# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Localidad'
        db.create_table('inventory_localidad', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('inventory', ['Localidad'])

        # Adding model 'Inventario'
        db.create_table('inventory_inventario', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('localidad', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='inventarios', null=True, to=orm['inventory.Localidad'])),
        ))
        db.send_create_signal('inventory', ['Inventario'])

        # Adding model 'ItemTemplate'
        db.create_table('inventory_itemtemplate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('marca', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('modelo', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('numero_de_parte', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('notas', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('inventory', ['ItemTemplate'])

        # Adding M2M table for field suppliers on 'ItemTemplate'
        db.create_table('inventory_itemtemplate_suppliers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('itemtemplate', models.ForeignKey(orm['inventory.itemtemplate'], null=False)),
            ('proveedor', models.ForeignKey(orm['inventory.proveedor'], null=False))
        ))
        db.create_unique('inventory_itemtemplate_suppliers', ['itemtemplate_id', 'proveedor_id'])

        # Adding model 'Proveedor'
        db.create_table('inventory_proveedor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('inventory', ['Proveedor'])

        # Adding model 'Item'
        db.create_table('inventory_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('plantilla', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['inventory.ItemTemplate'])),
            ('inventario', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['inventory.Inventario'])),
        ))
        db.send_create_signal('inventory', ['Item'])

        # Adding model 'Transferencia'
        db.create_table('inventory_transferencia', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('origen', self.gf('django.db.models.fields.related.ForeignKey')(related_name='salidas', to=orm['inventory.Inventario'])),
            ('destino', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entradas', to=orm['inventory.Inventario'])),
            ('aplicada', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transferencias', to=orm['inventory.ItemTemplate'])),
            ('cantidad', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('inventory', ['Transferencia'])

        # Adding model 'Requisicion'
        db.create_table('inventory_requisicion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('inventario', self.gf('django.db.models.fields.related.ForeignKey')(related_name='requisiciones', to=orm['inventory.Inventario'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='requisiciones', to=orm['inventory.ItemTemplate'])),
            ('cantidad', self.gf('django.db.models.fields.IntegerField')()),
            ('aprobada', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('entregada', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('inventory', ['Requisicion'])


    def backwards(self, orm):
        # Deleting model 'Localidad'
        db.delete_table('inventory_localidad')

        # Deleting model 'Inventario'
        db.delete_table('inventory_inventario')

        # Deleting model 'ItemTemplate'
        db.delete_table('inventory_itemtemplate')

        # Removing M2M table for field suppliers on 'ItemTemplate'
        db.delete_table('inventory_itemtemplate_suppliers')

        # Deleting model 'Proveedor'
        db.delete_table('inventory_proveedor')

        # Deleting model 'Item'
        db.delete_table('inventory_item')

        # Deleting model 'Transferencia'
        db.delete_table('inventory_transferencia')

        # Deleting model 'Requisicion'
        db.delete_table('inventory_requisicion')


    models = {
        'inventory.inventario': {
            'Meta': {'object_name': 'Inventario'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'localidad': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'inventarios'", 'null': 'True', 'to': "orm['inventory.Localidad']"})
        },
        'inventory.item': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Item'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inventario': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['inventory.Inventario']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'plantilla': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['inventory.ItemTemplate']"})
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
        'inventory.localidad': {
            'Meta': {'object_name': 'Localidad'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'inventory.proveedor': {
            'Meta': {'object_name': 'Proveedor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'inventory.requisicion': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Requisicion'},
            'aprobada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cantidad': ('django.db.models.fields.IntegerField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'entregada': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inventario': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requisiciones'", 'to': "orm['inventory.Inventario']"}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requisiciones'", 'to': "orm['inventory.ItemTemplate']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'inventory.transferencia': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Transferencia'},
            'aplicada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cantidad': ('django.db.models.fields.IntegerField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'destino': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entradas'", 'to': "orm['inventory.Inventario']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transferencias'", 'to': "orm['inventory.ItemTemplate']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'origen': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'salidas'", 'to': "orm['inventory.Inventario']"})
        }
    }

    complete_apps = ['inventory']