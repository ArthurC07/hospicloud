# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Persona'
        db.create_table('persona_persona', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tipo_identificacion', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('identificacion', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20, blank=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('apellido', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('sexo', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('nacimiento', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('estado_civil', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('profesion', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('telefono', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('ci', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('celular', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('domicilio', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('tel_trabajo', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('centro_trabajo', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('direccion_trabajo', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('antiguedad', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('cargo', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('fotografia', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, blank=True)),
            ('nacionalidad', self.gf('persona.fields.OrderedCountryField')(max_length=2, blank=True)),
        ))
        db.send_create_signal('persona', ['Persona'])

        # Adding model 'Fisico'
        db.create_table('persona_fisico', (
            ('persona', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['persona.Persona'], unique=True, primary_key=True)),
            ('peso', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2)),
            ('altura', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2)),
            ('color_de_ojos', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('color_de_cabello', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('factor_rh', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('tipo_de_sangre', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
        ))
        db.send_create_signal('persona', ['Fisico'])

        # Adding model 'EstiloVida'
        db.create_table('persona_estilovida', (
            ('persona', self.gf('django.db.models.fields.related.OneToOneField')(related_name='estilo_vida', unique=True, primary_key=True, to=orm['persona.Persona'])),
            ('consume_tabaco', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('inicio_consumo_tabaco', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('tipo_de_tabaco', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('consumo_diario_tabaco', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('vino', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cerveza', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('licor', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cafe', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cantidad_cafe', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('dieta', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('cantidad', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('numero_comidas', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('tipo_de_comidas', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('consume_drogas', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('drogas', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('otros', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('persona', ['EstiloVida'])

        # Adding model 'Antecedente'
        db.create_table('persona_antecedente', (
            ('persona', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['persona.Persona'], unique=True, primary_key=True)),
            ('cardiopatia', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hipertension', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('diabetes', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hepatitis', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('rinitis', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tuberculosis', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('artritis', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('asma', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('colitis', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('gastritis', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sinusitis', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hipertrigliceridemia', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('colelitiasis', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('migrana', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('alergias', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('congenital', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('general', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('nutricional', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('otros', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('persona', ['Antecedente'])

        # Adding model 'AntecedenteFamiliar'
        db.create_table('persona_antecedentefamiliar', (
            ('persona', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['persona.Persona'], unique=True, primary_key=True)),
            ('carcinogenico', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cardiovascular', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('endocrinologico', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('respiratorio', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('otros', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('persona', ['AntecedenteFamiliar'])

        # Adding model 'AntecedenteObstetrico'
        db.create_table('persona_antecedenteobstetrico', (
            ('persona', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['persona.Persona'], unique=True, primary_key=True)),
            ('menarca', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('ultimo_periodo', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('displasia', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('g', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('p', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('a', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('c', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('otros', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('persona', ['AntecedenteObstetrico'])

        # Adding model 'AntecedenteQuirurgico'
        db.create_table('persona_antecedentequirurgico', (
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persona.Persona'], primary_key=True)),
            ('procedimiento', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('fecha', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('persona', ['AntecedenteQuirurgico'])


    def backwards(self, orm):
        
        # Deleting model 'Persona'
        db.delete_table('persona_persona')

        # Deleting model 'Fisico'
        db.delete_table('persona_fisico')

        # Deleting model 'EstiloVida'
        db.delete_table('persona_estilovida')

        # Deleting model 'Antecedente'
        db.delete_table('persona_antecedente')

        # Deleting model 'AntecedenteFamiliar'
        db.delete_table('persona_antecedentefamiliar')

        # Deleting model 'AntecedenteObstetrico'
        db.delete_table('persona_antecedenteobstetrico')

        # Deleting model 'AntecedenteQuirurgico'
        db.delete_table('persona_antecedentequirurgico')


    models = {
        'persona.antecedente': {
            'Meta': {'object_name': 'Antecedente'},
            'alergias': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'artritis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'asma': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cardiopatia': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'colelitiasis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'colitis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'congenital': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'diabetes': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gastritis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'general': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'hepatitis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hipertension': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hipertrigliceridemia': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'migrana': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nutricional': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'otros': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['persona.Persona']", 'unique': 'True', 'primary_key': 'True'}),
            'rinitis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sinusitis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tuberculosis': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'persona.antecedentefamiliar': {
            'Meta': {'object_name': 'AntecedenteFamiliar'},
            'carcinogenico': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cardiovascular': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'endocrinologico': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'otros': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['persona.Persona']", 'unique': 'True', 'primary_key': 'True'}),
            'respiratorio': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'persona.antecedenteobstetrico': {
            'Meta': {'object_name': 'AntecedenteObstetrico'},
            'a': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'c': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'displasia': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'g': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'menarca': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'otros': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'p': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['persona.Persona']", 'unique': 'True', 'primary_key': 'True'}),
            'ultimo_periodo': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'persona.antecedentequirurgico': {
            'Meta': {'object_name': 'AntecedenteQuirurgico'},
            'fecha': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persona.Persona']", 'primary_key': 'True'}),
            'procedimiento': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'persona.estilovida': {
            'Meta': {'object_name': 'EstiloVida'},
            'cafe': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cantidad': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'cantidad_cafe': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'cerveza': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'consume_drogas': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'consume_tabaco': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'consumo_diario_tabaco': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'dieta': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'drogas': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'inicio_consumo_tabaco': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'licor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'numero_comidas': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'otros': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'estilo_vida'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['persona.Persona']"}),
            'tipo_de_comidas': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'tipo_de_tabaco': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'vino': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'persona.fisico': {
            'Meta': {'object_name': 'Fisico'},
            'altura': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'color_de_cabello': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'color_de_ojos': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'factor_rh': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['persona.Persona']", 'unique': 'True', 'primary_key': 'True'}),
            'peso': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'tipo_de_sangre': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'})
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
        }
    }

    complete_apps = ['persona']
