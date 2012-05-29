# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Admision'
        db.create_table('spital_admision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('momento', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('paciente', self.gf('django.db.models.fields.related.ForeignKey')(related_name='admisiones', to=orm['persona.Persona'])),
            ('diagnostico', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('doctor', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('tipo_de_habitacion', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('habitacion', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('arancel', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('pago', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('poliza', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('certificado', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('aseguradora', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('deposito', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('observaciones', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('admitio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('admision', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('autorizacion', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('hospitalizacion', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('ingreso', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('fecha_pago', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('fecha_alta', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('codigo', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, blank=True)),
            ('qr', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, blank=True)),
            ('estado', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
        ))
        db.send_create_signal('spital', ['Admision'])

        # Adding M2M table for field fiadores on 'Admision'
        db.create_table('spital_admision_fiadores', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('admision', models.ForeignKey(orm['spital.admision'], null=False)),
            ('persona', models.ForeignKey(orm['persona.persona'], null=False))
        ))
        db.create_unique('spital_admision_fiadores', ['admision_id', 'persona_id'])

        # Adding M2M table for field referencias on 'Admision'
        db.create_table('spital_admision_referencias', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('admision', models.ForeignKey(orm['spital.admision'], null=False)),
            ('persona', models.ForeignKey(orm['persona.persona'], null=False))
        ))
        db.create_unique('spital_admision_referencias', ['admision_id', 'persona_id'])


    def backwards(self, orm):
        
        # Deleting model 'Admision'
        db.delete_table('spital_admision')

        # Removing M2M table for field fiadores on 'Admision'
        db.delete_table('spital_admision_fiadores')

        # Removing M2M table for field referencias on 'Admision'
        db.delete_table('spital_admision_referencias')


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
            'observaciones': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'paciente': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'admisiones'", 'to': "orm['persona.Persona']"}),
            'pago': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'poliza': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'qr': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'referencias': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'referencias'", 'symmetrical': 'False', 'to': "orm['persona.Persona']"}),
            'tipo_de_habitacion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        }
    }

    complete_apps = ['spital']
