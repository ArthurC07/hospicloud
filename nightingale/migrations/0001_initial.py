# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SignoVital'
        db.create_table('nightingale_signovital', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('admision', self.gf('django.db.models.fields.related.ForeignKey')(related_name='signos_vitales', to=orm['spital.Admision'])),
            ('fecha_y_hora', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('pulso', self.gf('django.db.models.fields.IntegerField')()),
            ('temperatura', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2)),
            ('presion', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2)),
            ('respiracion', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2)),
            ('observacion', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2)),
            ('saturacion_de_oxigeno', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2)),
            ('presion_arterial_media', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('nightingale', ['SignoVital'])

        # Adding model 'Evolucion'
        db.create_table('nightingale_evolucion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('admision', self.gf('django.db.models.fields.related.ForeignKey')(related_name='evolucion', to=orm['spital.Admision'])),
            ('fecha_y_hora', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('nota', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('nightingale', ['Evolucion'])

        # Adding model 'Cargo'
        db.create_table('nightingale_cargo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('admision', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cargos', to=orm['spital.Admision'])),
            ('fecha_y_hora', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('cargo', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('inicio', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('fin', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('nightingale', ['Cargo'])

        # Adding model 'OrdenMedica'
        db.create_table('nightingale_ordenmedica', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('admision', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ordenes_medicas', to=orm['spital.Admision'])),
            ('orden', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('doctor', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('fecha_y_hora', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('nightingale', ['OrdenMedica'])

        # Adding model 'Ingesta'
        db.create_table('nightingale_ingesta', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('admision', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ingestas', to=orm['spital.Admision'])),
            ('fecha_y_hora', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('ingerido', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('cantidad', self.gf('django.db.models.fields.IntegerField')()),
            ('liquido', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal('nightingale', ['Ingesta'])

        # Adding model 'Excreta'
        db.create_table('nightingale_excreta', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('admision', self.gf('django.db.models.fields.related.ForeignKey')(related_name='excretas', to=orm['spital.Admision'])),
            ('fecha_y_hora', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('medio', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('cantidad', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('otro', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('otros', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('nightingale', ['Excreta'])

        # Adding model 'NotaEnfermeria'
        db.create_table('nightingale_notaenfermeria', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('admision', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notas_enfermeria', to=orm['spital.Admision'])),
            ('fecha_y_hora', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('nota', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('nightingale', ['NotaEnfermeria'])

        # Adding model 'Glucometria'
        db.create_table('nightingale_glucometria', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('admision', self.gf('django.db.models.fields.related.ForeignKey')(related_name='glucometrias', to=orm['spital.Admision'])),
            ('fecha_y_hora', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('control', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('observacion', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('nightingale', ['Glucometria'])

        # Adding model 'Sumario'
        db.create_table('nightingale_sumario', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('admision', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['spital.Admision'], unique=True)),
            ('diagnostico', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('procedimiento_efectuado', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('condicion', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('recomendaciones', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('nightingale', ['Sumario'])

        # Adding model 'FrecuenciaLectura'
        db.create_table('nightingale_frecuencialectura', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('admision', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['spital.Admision'], unique=True)),
            ('glucometria', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('signos_vitales', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal('nightingale', ['FrecuenciaLectura'])


    def backwards(self, orm):
        
        # Deleting model 'SignoVital'
        db.delete_table('nightingale_signovital')

        # Deleting model 'Evolucion'
        db.delete_table('nightingale_evolucion')

        # Deleting model 'Cargo'
        db.delete_table('nightingale_cargo')

        # Deleting model 'OrdenMedica'
        db.delete_table('nightingale_ordenmedica')

        # Deleting model 'Ingesta'
        db.delete_table('nightingale_ingesta')

        # Deleting model 'Excreta'
        db.delete_table('nightingale_excreta')

        # Deleting model 'NotaEnfermeria'
        db.delete_table('nightingale_notaenfermeria')

        # Deleting model 'Glucometria'
        db.delete_table('nightingale_glucometria')

        # Deleting model 'Sumario'
        db.delete_table('nightingale_sumario')

        # Deleting model 'FrecuenciaLectura'
        db.delete_table('nightingale_frecuencialectura')


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
            'inicio': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'nightingale.evolucion': {
            'Meta': {'object_name': 'Evolucion'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'evolucion'", 'to': "orm['spital.Admision']"}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nota': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
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
            'otros': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'nightingale.frecuencialectura': {
            'Meta': {'object_name': 'FrecuenciaLectura'},
            'admision': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['spital.Admision']", 'unique': 'True'}),
            'glucometria': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'signos_vitales': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        'nightingale.glucometria': {
            'Meta': {'object_name': 'Glucometria'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'glucometrias'", 'to': "orm['spital.Admision']"}),
            'control': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'})
        },
        'nightingale.ingesta': {
            'Meta': {'object_name': 'Ingesta'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ingestas'", 'to': "orm['spital.Admision']"}),
            'cantidad': ('django.db.models.fields.IntegerField', [], {}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingerido': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'liquido': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        'nightingale.notaenfermeria': {
            'Meta': {'object_name': 'NotaEnfermeria'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notas_enfermeria'", 'to': "orm['spital.Admision']"}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nota': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'nightingale.ordenmedica': {
            'Meta': {'object_name': 'OrdenMedica'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ordenes_medicas'", 'to': "orm['spital.Admision']"}),
            'doctor': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orden': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'nightingale.signovital': {
            'Meta': {'object_name': 'SignoVital'},
            'admision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'signos_vitales'", 'to': "orm['spital.Admision']"}),
            'fecha_y_hora': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2'}),
            'presion': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2'}),
            'presion_arterial_media': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'pulso': ('django.db.models.fields.IntegerField', [], {}),
            'respiracion': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2'}),
            'saturacion_de_oxigeno': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2'}),
            'temperatura': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2'})
        },
        'nightingale.sumario': {
            'Meta': {'object_name': 'Sumario'},
            'admision': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['spital.Admision']", 'unique': 'True'}),
            'condicion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'diagnostico': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'procedimiento_efectuado': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'recomendaciones': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
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
            'tiempo': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'tipo_de_habitacion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        }
    }

    complete_apps = ['nightingale']
