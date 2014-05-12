# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Pago.ciclo'
        db.add_column(u'contracts_pago', 'ciclo',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Pago.ciclo'
        db.delete_column(u'contracts_pago', 'ciclo')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'contracts.beneficiario': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Beneficiario'},
            'contrato': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'beneficiarios'", 'to': u"orm['contracts.Contrato']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inscripcion': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 12, 0, 0)'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'beneficiarios'", 'to': u"orm['persona.Persona']"})
        },
        u'contracts.cancelacion': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Cancelacion'},
            'contrato': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cancelaciones'", 'to': u"orm['contracts.Contrato']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 5, 12, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'motivo': ('django.db.models.fields.TextField', [], {}),
            'pago': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'})
        },
        u'contracts.contrato': {
            'Meta': {'object_name': 'Contrato'},
            'administradores': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'contratos'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'cancelado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'contratos'", 'null': 'True', 'to': u"orm['persona.Empleador']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inicio': ('django.db.models.fields.DateField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'numero': ('django.db.models.fields.IntegerField', [], {}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contratos'", 'to': u"orm['persona.Persona']"}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contratos'", 'to': u"orm['contracts.Plan']"}),
            'renovacion': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'ultimo_pago': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 12, 0, 0)'}),
            'vencimiento': ('django.db.models.fields.DateField', [], {}),
            'vendedor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contratos'", 'to': u"orm['contracts.Vendedor']"})
        },
        u'contracts.evento': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Evento'},
            'adjunto': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'contrato': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'eventos'", 'to': u"orm['contracts.Contrato']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'descripcion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 12, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'precio': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'eventos'", 'to': u"orm['contracts.TipoEvento']"})
        },
        u'contracts.limiteevento': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'LimiteEvento'},
            'cantidad': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'limites'", 'to': u"orm['contracts.Plan']"}),
            'tipo_evento': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'limites'", 'to': u"orm['contracts.TipoEvento']"})
        },
        u'contracts.meta': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Meta'},
            'contratos': ('django.db.models.fields.IntegerField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 5, 12, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        u'contracts.pago': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Pago'},
            'ciclo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'contrato': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pagos'", 'to': u"orm['contracts.Contrato']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'descripcion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'facturar': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 12, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'precio': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'tipo_de_pago': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pagos'", 'null': 'True', 'to': u"orm['contracts.TipoPago']"})
        },
        u'contracts.plan': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Plan'},
            'adicionales': ('django.db.models.fields.IntegerField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'edad_maxima': ('django.db.models.fields.IntegerField', [], {}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'planes'", 'null': 'True', 'to': u"orm['persona.Empleador']"}),
            'empresarial': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medicamentos': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'precio': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'})
        },
        u'contracts.tipoevento': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'TipoEvento'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'contracts.tipopago': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'TipoPago'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tipos_pago'", 'to': u"orm['inventory.ItemTemplate']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        u'contracts.vendedor': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Vendedor'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'habilitado': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'vendedores'", 'to': u"orm['auth.User']"})
        },
        u'inventory.itemtemplate': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'ItemTemplate'},
            'activo': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'comision': ('django.db.models.fields.DecimalField', [], {'default': "'30.00'", 'max_digits': '4', 'decimal_places': '2'}),
            'comision2': ('django.db.models.fields.DecimalField', [], {'default': "'10.00'", 'max_digits': '4', 'decimal_places': '2'}),
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
        u'persona.empleador': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Empleador'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'direccion': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'persona.persona': {
            'Meta': {'object_name': 'Persona'},
            'apellido': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'celular': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'domicilio': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'duplicado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'estado_civil': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'fotografia': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
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

    complete_apps = ['contracts']