# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Esperador'
        db.delete_table(u'clinique_esperador')

        # Deleting model 'HistoriaClinica'
        db.delete_table(u'clinique_historiaclinica')

        # Deleting model 'Optometria'
        db.delete_table(u'clinique_optometria')

        # Deleting model 'Transaccion'
        db.delete_table(u'clinique_transaccion')

        # Deleting model 'Pago'
        db.delete_table(u'clinique_pago')

        # Deleting model 'Consultorio'
        db.delete_table(u'clinique_consultorio')

        # Deleting model 'Receta'
        db.delete_table(u'clinique_receta')

        # Deleting model 'Consulta'
        db.delete_table(u'clinique_consulta')

        # Deleting model 'Cita'
        db.delete_table(u'clinique_cita')

        # Deleting model 'Paciente'
        db.delete_table(u'clinique_paciente')


    def backwards(self, orm):
        # Adding model 'Esperador'
        db.create_table(u'clinique_esperador', (
            ('atendido', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('consultorio', self.gf('django.db.models.fields.related.ForeignKey')(related_name='esperadores', to=orm['clinique.Consultorio'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('paciente', self.gf('django.db.models.fields.related.ForeignKey')(related_name='esperas', to=orm['clinique.Paciente'])),
        ))
        db.send_create_signal('clinique', ['Esperador'])

        # Adding model 'HistoriaClinica'
        db.create_table(u'clinique_historiaclinica', (
            ('paciente', self.gf('django.db.models.fields.related.ForeignKey')(related_name='historias_clinicas', null=True, to=orm['clinique.Paciente'])),
            ('agudeza_visual_ojo_derecho', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('fecha_y_hora', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('nota', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agudeza_visual_ojo_izquierdo', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('clinique', ['HistoriaClinica'])

        # Adding model 'Optometria'
        db.create_table(u'clinique_optometria', (
            ('prisma_ojo_derecho', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=2)),
            ('d_p_ojo_izquierdo', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=2)),
            ('altura_ojo_derecho', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=2)),
            ('esfera_ojo_derecho', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=2)),
            ('cilindro_ojo_derecho', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=2)),
            ('adicion_ojo_izquierdo', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=2)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('esfera_ojo_izquierdo', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=2)),
            ('altura_ojo_izquierdo', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=2)),
            ('adicion_ojo_derecho', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=2)),
            ('notas', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('eje_ojo_izquierdo', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=2)),
            ('cilindro_ojo_izquierdo', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=2)),
            ('eje_ojo_derecho', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=2)),
            ('prisma_ojo_izquierdo', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=2)),
            ('fecha_y_hora', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('d_p_ojo_derecho', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=2)),
            ('paciente', self.gf('django.db.models.fields.related.ForeignKey')(related_name='optometrias', to=orm['clinique.Paciente'])),
        ))
        db.send_create_signal('clinique', ['Optometria'])

        # Adding model 'Transaccion'
        db.create_table(u'clinique_transaccion', (
            ('paciente', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transacciones', to=orm['clinique.Paciente'])),
            ('tipo', self.gf('django.db.models.fields.IntegerField')()),
            ('monto', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('fecha_y_hora', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('concepto', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('clinique', ['Transaccion'])

        # Adding model 'Pago'
        db.create_table(u'clinique_pago', (
            ('paciente', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pagos', to=orm['clinique.Paciente'])),
            ('monto', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=2)),
            ('fecha_y_hora', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('concepto', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('forma_de_pago', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('clinique', ['Pago'])

        # Adding model 'Consultorio'
        db.create_table(u'clinique_consultorio', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('doctor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='consultorios', null=True, to=orm['auth.User'], blank=True)),
            ('secretaria', self.gf('django.db.models.fields.related.ForeignKey')(related_name='secretariados', null=True, to=orm['auth.User'], blank=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('clinique', ['Consultorio'])

        # Adding model 'Receta'
        db.create_table(u'clinique_receta', (
            ('paciente', self.gf('django.db.models.fields.related.ForeignKey')(related_name='recetas', to=orm['clinique.Paciente'])),
            ('notas_adicionales', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('fecha_y_hora', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('medicamentos', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('clinique', ['Receta'])

        # Adding model 'Consulta'
        db.create_table(u'clinique_consulta', (
            ('paciente', self.gf('django.db.models.fields.related.ForeignKey')(related_name='consultas', to=orm['clinique.Paciente'])),
            ('agudeza_visual_ojo_derecho', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('fecha_y_hora', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('razon_de_la_visita', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agudeza_visual_ojo_izquierdo', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('clinique', ['Consulta'])

        # Adding model 'Cita'
        db.create_table(u'clinique_cita', (
            ('consultorio', self.gf('django.db.models.fields.related.ForeignKey')(related_name='citas', to=orm['clinique.Consultorio'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('fecha_y_hora', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('clinique', ['Cita'])

        # Adding model 'Paciente'
        db.create_table(u'clinique_paciente', (
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(related_name='consultorios', to=orm['persona.Persona'])),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('consultorio', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pacientes', to=orm['clinique.Consultorio'])),
            ('primera_visita', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('clinique', ['Paciente'])


    models = {
        
    }

    complete_apps = ['clinique']