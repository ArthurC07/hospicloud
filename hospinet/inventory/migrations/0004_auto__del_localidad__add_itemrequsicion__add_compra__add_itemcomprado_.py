# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Localidad'
        db.delete_table(u'inventory_localidad')

        # Adding model 'ItemRequsicion'
        db.create_table(u'inventory_itemrequsicion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('requisicion', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['inventory.Requisicion'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='requisiciones', to=orm['inventory.ItemTemplate'])),
            ('cantidad', self.gf('django.db.models.fields.IntegerField')()),
            ('entregada', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'inventory', ['ItemRequsicion'])

        # Adding model 'Compra'
        db.create_table(u'inventory_compra', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('inventario', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='compras', null=True, to=orm['inventory.Inventario'])),
            ('ingresada', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('proveedor', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['Compra'])

        # Adding model 'ItemComprado'
        db.create_table(u'inventory_itemcomprado', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('compra', self.gf('django.db.models.fields.related.ForeignKey')(related_name='compras', to=orm['inventory.Compra'])),
            ('ingresado', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'inventory', ['ItemComprado'])

        # Adding model 'ItemType'
        db.create_table(u'inventory_itemtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'inventory', ['ItemType'])

        # Adding model 'ItemAction'
        db.create_table(u'inventory_itemaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('action', self.gf('django.db.models.fields.TextField')()),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='acciones', to=orm['inventory.ItemTemplate'])),
        ))
        db.send_create_signal(u'inventory', ['ItemAction'])

        # Adding model 'Transferido'
        db.create_table(u'inventory_transferido', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('transferencia', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transferidos', to=orm['inventory.Transferencia'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transferidos', to=orm['inventory.ItemTemplate'])),
            ('cantidad', self.gf('django.db.models.fields.IntegerField')()),
            ('aplicada', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'inventory', ['Transferido'])

        # Deleting field 'Transferencia.item'
        db.delete_column(u'inventory_transferencia', 'item_id')

        # Deleting field 'Transferencia.cantidad'
        db.delete_column(u'inventory_transferencia', 'cantidad')

        # Adding field 'Transferencia.requisicion'
        db.add_column(u'inventory_transferencia', 'requisicion',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='transferencias', null=True, to=orm['inventory.Requisicion']),
                      keep_default=False)

        # Adding field 'Transferencia.usuario'
        db.add_column(u'inventory_transferencia', 'usuario',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='transferencias', null=True, to=orm['auth.User']),
                      keep_default=False)


        # Changing field 'Transferencia.aplicada'
        db.alter_column(u'inventory_transferencia', 'aplicada', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'Transferencia.destino'
        db.alter_column(u'inventory_transferencia', 'destino_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['inventory.Inventario']))

        # Changing field 'Transferencia.origen'
        db.alter_column(u'inventory_transferencia', 'origen_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['inventory.Inventario']))
        # Deleting field 'ItemTemplate.numero_de_parte'
        db.delete_column(u'inventory_itemtemplate', 'numero_de_parte')

        # Deleting field 'ItemTemplate.medicamento'
        db.delete_column(u'inventory_itemtemplate', 'medicamento')

        # Deleting field 'ItemTemplate.emergencia'
        db.delete_column(u'inventory_itemtemplate', 'emergencia')

        # Adding field 'ItemTemplate.precio_de_venta'
        db.add_column(u'inventory_itemtemplate', 'precio_de_venta',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=2),
                      keep_default=False)

        # Adding field 'ItemTemplate.costo'
        db.add_column(u'inventory_itemtemplate', 'costo',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=2),
                      keep_default=False)

        # Adding field 'ItemTemplate.unidad_de_medida'
        db.add_column(u'inventory_itemtemplate', 'unidad_de_medida',
                      self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True),
                      keep_default=False)

        # Adding field 'ItemTemplate.impuestos'
        db.add_column(u'inventory_itemtemplate', 'impuestos',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=2),
                      keep_default=False)

        # Adding field 'ItemTemplate.activo'
        db.add_column(u'inventory_itemtemplate', 'activo',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Deleting field 'Inventario.localidad'
        db.delete_column(u'inventory_inventario', 'localidad_id')

        # Adding field 'Inventario.lugar'
        db.add_column(u'inventory_inventario', 'lugar',
                      self.gf('django.db.models.fields.CharField')(default='Bodega', max_length=255),
                      keep_default=False)

        # Adding field 'Inventario.puede_comprar'
        db.add_column(u'inventory_inventario', 'puede_comprar',
                      self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Requisicion.item'
        db.delete_column(u'inventory_requisicion', 'item_id')

        # Adding field 'Requisicion.usuario'
        db.add_column(u'inventory_requisicion', 'usuario',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='requisiciones', null=True, to=orm['auth.User']),
                      keep_default=False)


        # Changing field 'Requisicion.inventario'
        db.alter_column(u'inventory_requisicion', 'inventario_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['inventory.Inventario']))

    def backwards(self, orm):
        # Adding model 'Localidad'
        db.create_table(u'inventory_localidad', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'inventory', ['Localidad'])

        # Deleting model 'ItemRequsicion'
        db.delete_table(u'inventory_itemrequsicion')

        # Deleting model 'Compra'
        db.delete_table(u'inventory_compra')

        # Deleting model 'ItemComprado'
        db.delete_table(u'inventory_itemcomprado')

        # Deleting model 'ItemType'
        db.delete_table(u'inventory_itemtype')

        # Deleting model 'ItemAction'
        db.delete_table(u'inventory_itemaction')

        # Deleting model 'Transferido'
        db.delete_table(u'inventory_transferido')

        # Adding field 'Transferencia.item'
        db.add_column(u'inventory_transferencia', 'item',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='transferencias', to=orm['inventory.ItemTemplate']),
                      keep_default=False)

        # Adding field 'Transferencia.cantidad'
        db.add_column(u'inventory_transferencia', 'cantidad',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'Transferencia.requisicion'
        db.delete_column(u'inventory_transferencia', 'requisicion_id')

        # Deleting field 'Transferencia.usuario'
        db.delete_column(u'inventory_transferencia', 'usuario_id')


        # Changing field 'Transferencia.aplicada'
        db.alter_column(u'inventory_transferencia', 'aplicada', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Transferencia.destino'
        db.alter_column(u'inventory_transferencia', 'destino_id', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['inventory.Inventario']))

        # Changing field 'Transferencia.origen'
        db.alter_column(u'inventory_transferencia', 'origen_id', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['inventory.Inventario']))
        # Adding field 'ItemTemplate.numero_de_parte'
        db.add_column(u'inventory_itemtemplate', 'numero_de_parte',
                      self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True),
                      keep_default=False)

        # Adding field 'ItemTemplate.medicamento'
        db.add_column(u'inventory_itemtemplate', 'medicamento',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'ItemTemplate.emergencia'
        db.add_column(u'inventory_itemtemplate', 'emergencia',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Deleting field 'ItemTemplate.precio_de_venta'
        db.delete_column(u'inventory_itemtemplate', 'precio_de_venta')

        # Deleting field 'ItemTemplate.costo'
        db.delete_column(u'inventory_itemtemplate', 'costo')

        # Deleting field 'ItemTemplate.unidad_de_medida'
        db.delete_column(u'inventory_itemtemplate', 'unidad_de_medida')

        # Deleting field 'ItemTemplate.impuestos'
        db.delete_column(u'inventory_itemtemplate', 'impuestos')

        # Deleting field 'ItemTemplate.activo'
        db.delete_column(u'inventory_itemtemplate', 'activo')

        # Adding field 'Inventario.localidad'
        db.add_column(u'inventory_inventario', 'localidad',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='inventarios', null=True, to=orm['inventory.Localidad'], blank=True),
                      keep_default=False)

        # Deleting field 'Inventario.lugar'
        db.delete_column(u'inventory_inventario', 'lugar')

        # Deleting field 'Inventario.puede_comprar'
        db.delete_column(u'inventory_inventario', 'puede_comprar')

        # Adding field 'Requisicion.item'
        db.add_column(u'inventory_requisicion', 'item',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='requisiciones', to=orm['inventory.ItemTemplate']),
                      keep_default=False)

        # Deleting field 'Requisicion.usuario'
        db.delete_column(u'inventory_requisicion', 'usuario_id')


        # Changing field 'Requisicion.inventario'
        db.alter_column(u'inventory_requisicion', 'inventario_id', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['inventory.Inventario']))

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
        u'inventory.compra': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Compra'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingresada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'inventario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'compras'", 'null': 'True', 'to': u"orm['inventory.Inventario']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'proveedor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'inventory.inventario': {
            'Meta': {'object_name': 'Inventario'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lugar': ('django.db.models.fields.CharField', [], {'default': "'Bodega'", 'max_length': '255'}),
            'puede_comprar': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'})
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
        u'inventory.itemaction': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'ItemAction'},
            'action': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'acciones'", 'to': u"orm['inventory.ItemTemplate']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'inventory.itemcomprado': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'ItemComprado'},
            'compra': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'compras'", 'to': u"orm['inventory.Compra']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingresado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        u'inventory.itemrequsicion': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'ItemRequsicion'},
            'cantidad': ('django.db.models.fields.IntegerField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'entregada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requisiciones'", 'to': u"orm['inventory.ItemTemplate']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'requisicion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': u"orm['inventory.Requisicion']"})
        },
        u'inventory.itemtemplate': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'ItemTemplate'},
            'activo': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'costo': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impuestos': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
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
        u'inventory.requisicion': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Requisicion'},
            'aprobada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cantidad': ('django.db.models.fields.IntegerField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'entregada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inventario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'requisiciones'", 'null': 'True', 'to': u"orm['inventory.Inventario']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'requisiciones'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'inventory.transferencia': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Transferencia'},
            'aplicada': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'destino': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'entradas'", 'null': 'True', 'to': u"orm['inventory.Inventario']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'origen': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'salidas'", 'null': 'True', 'to': u"orm['inventory.Inventario']"}),
            'requisicion': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'transferencias'", 'null': 'True', 'to': u"orm['inventory.Requisicion']"}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'transferencias'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'inventory.transferido': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Transferido'},
            'aplicada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cantidad': ('django.db.models.fields.IntegerField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transferidos'", 'to': u"orm['inventory.ItemTemplate']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'transferencia': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transferidos'", 'to': u"orm['inventory.Transferencia']"})
        }
    }

    complete_apps = ['inventory']