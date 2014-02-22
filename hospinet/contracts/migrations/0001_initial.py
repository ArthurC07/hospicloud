# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Vendedor'
        db.create_table(u'contracts_vendedor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(related_name='vendedores', to=orm['auth.User'])),
            ('habilitado', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'contracts', ['Vendedor'])

        # Adding model 'Plan'
        db.create_table(u'contracts_plan', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('precio', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=2)),
            ('eventos_maximos', self.gf('django.db.models.fields.IntegerField')()),
            ('edad_maxima', self.gf('django.db.models.fields.IntegerField')()),
            ('adicionales', self.gf('django.db.models.fields.IntegerField')()),
            ('medicamentos', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=2)),
        ))
        db.send_create_signal(u'contracts', ['Plan'])

        # Adding model 'Contrato'
        db.create_table(u'contracts_contrato', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(related_name='contratos', to=orm['persona.Persona'])),
            ('numero', self.gf('django.db.models.fields.IntegerField')()),
            ('vendedor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='contratos', to=orm['contracts.Vendedor'])),
            ('plan', self.gf('django.db.models.fields.related.ForeignKey')(related_name='contratos', to=orm['contracts.Plan'])),
            ('inicio', self.gf('django.db.models.fields.DateField')()),
            ('vencimiento', self.gf('django.db.models.fields.DateField')()),
            ('ultimo_pago', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 2, 20, 0, 0))),
        ))
        db.send_create_signal(u'contracts', ['Contrato'])

        # Adding M2M table for field administradores on 'Contrato'
        m2m_table_name = db.shorten_name(u'contracts_contrato_administradores')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contrato', models.ForeignKey(orm[u'contracts.contrato'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['contrato_id', 'user_id'])

        # Adding model 'Beneficiario'
        db.create_table(u'contracts_beneficiario', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(related_name='beneficiarios', to=orm['persona.Persona'])),
            ('contrato', self.gf('django.db.models.fields.related.ForeignKey')(related_name='beneficiarios', to=orm['contracts.Contrato'])),
        ))
        db.send_create_signal(u'contracts', ['Beneficiario'])

        # Adding model 'Pago'
        db.create_table(u'contracts_pago', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('contrato', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pagos', to=orm['contracts.Contrato'])),
            ('fecha', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 2, 20, 0, 0))),
            ('precio', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=2)),
        ))
        db.send_create_signal(u'contracts', ['Pago'])

        # Adding model 'TipoEvento'
        db.create_table(u'contracts_tipoevento', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'contracts', ['TipoEvento'])

        # Adding model 'Evento'
        db.create_table(u'contracts_evento', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('contrato', self.gf('django.db.models.fields.related.ForeignKey')(related_name='eventos', to=orm['contracts.Contrato'])),
            ('tipo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='eventos', to=orm['contracts.TipoEvento'])),
            ('fecha', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 2, 20, 0, 0))),
        ))
        db.send_create_signal(u'contracts', ['Evento'])


    def backwards(self, orm):
        # Deleting model 'Vendedor'
        db.delete_table(u'contracts_vendedor')

        # Deleting model 'Plan'
        db.delete_table(u'contracts_plan')

        # Deleting model 'Contrato'
        db.delete_table(u'contracts_contrato')

        # Removing M2M table for field administradores on 'Contrato'
        db.delete_table(db.shorten_name(u'contracts_contrato_administradores'))

        # Deleting model 'Beneficiario'
        db.delete_table(u'contracts_beneficiario')

        # Deleting model 'Pago'
        db.delete_table(u'contracts_pago')

        # Deleting model 'TipoEvento'
        db.delete_table(u'contracts_tipoevento')

        # Deleting model 'Evento'
        db.delete_table(u'contracts_evento')


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
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'beneficiarios'", 'to': u"orm['persona.Persona']"})
        },
        u'contracts.contrato': {
            'Meta': {'object_name': 'Contrato'},
            'administradores': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'contratos'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inicio': ('django.db.models.fields.DateField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'numero': ('django.db.models.fields.IntegerField', [], {}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contratos'", 'to': u"orm['persona.Persona']"}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contratos'", 'to': u"orm['contracts.Plan']"}),
            'ultimo_pago': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 2, 20, 0, 0)'}),
            'vencimiento': ('django.db.models.fields.DateField', [], {}),
            'vendedor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contratos'", 'to': u"orm['contracts.Vendedor']"})
        },
        u'contracts.evento': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Evento'},
            'contrato': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'eventos'", 'to': u"orm['contracts.Contrato']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 2, 20, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'eventos'", 'to': u"orm['contracts.TipoEvento']"})
        },
        u'contracts.pago': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Pago'},
            'contrato': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pagos'", 'to': u"orm['contracts.Contrato']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 2, 20, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'precio': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'})
        },
        u'contracts.plan': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Plan'},
            'adicionales': ('django.db.models.fields.IntegerField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'edad_maxima': ('django.db.models.fields.IntegerField', [], {}),
            'eventos_maximos': ('django.db.models.fields.IntegerField', [], {}),
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
        u'contracts.vendedor': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Vendedor'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'habilitado': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'vendedores'", 'to': u"orm['auth.User']"})
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

    complete_apps = ['contracts']