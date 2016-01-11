# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Carlos Flores <cafg10@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.
import environ
env = environ.Env(DEBUG=(bool, False), )
environ.Env.read_env()


class ModuleConfig(object):
    def __init__(self):
        self.caja = env.bool('INVOICE_ENABLED', default=True)
        self.consulta = env.bool('CONSULTA_ENABLED', default=True)
        self.contratos = env.bool('CONTRATOS_ENABLED', default=True)
        self.emergencia = env.bool('EMERGENCIA_ENABLED', default=True)
        self.hospitalizacion = env.bool('HOSPITALIZACION_ENABLED', default=True)
        self.imagenes = env.bool('IMAGENES_ENABLED', default=True)
        self.laboratorio = env.bool('LAB_ENABLED', default=True)
        self.inventario = env.bool('INVENTARIO_ENABLED', default=True)
        self.presupuesto = env.bool('BUDGET_ENABLED', default=True)
        self.rrhh = env.bool('RRHH_ENABLED', default=True)


def chat(request):
    return {
        'online_help': 'placeholder',
        'chat': 'placeholder',
        'bug_report': 'https://gitreports.com/issue/SpectralAngel/hospicloud',
    }


def configuration(request):
    return {
        'modules': ModuleConfig()
    }
