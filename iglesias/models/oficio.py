# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Oficio(models.Model):
    _name = 'iglesias.oficio'
    _rec_name = 'nombre'

    congregacion_id = fields.Many2one('iglesias.congregacion', 'Congregación')
    fecha = fields.Date('Fecha')
    estacion_liturgica_id = fields.Many2one('iglesias.estacion_liturgica', 'Estación litúrgica')
    actividad = fields.Selection([('comunion', 'Servicio de Santa comunión'), ('otros', 'Otros servicios')],
                                 'Actividad que se realiza')
    # sacramentos_celebrados_ids = fields.One2many('sacramentos.oficios', 'oficio_id', 'Sacramentos celebrados')
    nombre = fields.Char('Nombre', compute='_calc_nombre', readonly=True, store=True)
    asistencia_total = fields.Integer('Asistencia total')
    sacramentos_ids = fields.One2many('iglesias.sacramento', 'oficio_id', 'Sacramentos')

    bautismos = fields.Integer('Bautismos')
    cantidad_bautizados = fields.Integer('Cantidad de bautizados')
    confirmados = fields.Integer('Confirmados')
    cantidad_confirmaciones = fields.Integer('Cantidad de confirmaciones')
    santa_comunion = fields.Integer('Santa comunión')
    cantidad_comulgantes = fields.Integer('Cantidad de comulgantes')
    bendiciones = fields.Integer('Bendición de matrimonios')
    cantidad_bendiciones = fields.Integer('Cantidad de matrimonios bendecidos')

    # Ingresos
    bandejas = fields.Float('Ofrendas de bandejas', digits=(16, 2))
    diezmos = fields.Float('Ofrendas de diezmos', digits=(16, 2))
    unidad_gracia = fields.Float('Ofrenda de unidad de gracia', digits=(16, 2))
    cuaresma = fields.Float('Ofrenda especial de Cuaresma', digits=(16, 2))
    navidad = fields.Float('Ofrendas para cena de Navidad', digits=(16, 2))
    diocesis_ninnos = fields.Float('Suplemento de la diócesis para niños', digits=(16, 2))
    diocesis_iglesia = fields.Float('Suplemento de la diócesis para iglesia', digits=(16, 2))
    otras_ofrendas = fields.Float('Otras ofrendas', digits=(16, 2))
    total_ofrendas = fields.Float('Total ofrendas', digits=(16, 2), compute='_calc_total_ofrendas')
    # Egresos
    egreso_01 = fields.Float('01', digits=(16, 2))
    egreso_02 = fields.Float('02', digits=(16, 2))
    egreso_03 = fields.Float('03', digits=(16, 2))
    egreso_04 = fields.Float('04', digits=(16, 2))
    egreso_05 = fields.Float('05', digits=(16, 2))
    egreso_06 = fields.Float('06', digits=(16, 2))
    egreso_07 = fields.Float('07', digits=(16, 2))
    egreso_08 = fields.Float('08', digits=(16, 2))
    egreso_09 = fields.Float('09', digits=(16, 2))
    egreso_10 = fields.Float('10', digits=(16, 2))
    egreso_11 = fields.Float('11', digits=(16, 2))
    egreso_12 = fields.Float('12', digits=(16, 2))
    egreso_13 = fields.Float('13', digits=(16, 2))
    egreso_14 = fields.Float('14', digits=(16, 2))
    egreso_15 = fields.Float('15', digits=(16, 2))
    egreso_16 = fields.Float('16', digits=(16, 2))
    egreso_17 = fields.Float('17', digits=(16, 2))
    egreso_18 = fields.Float('18', digits=(16, 2))
    total_egresos = fields.Float('Total de egresos', digits=(16, 2), compute='_calc_total_egresos')

    observaciones = fields.Text('Observaciones')
    ministro = fields.Many2one('hr.employee', 'Ministro', domain=[('es_miembro', '=', False)],
                               context={'default_es_miembro': False})
    titulo = fields.Char('Título de la predicación')

    @api.one
    @api.depends('bandejas', 'diezmos', 'unidad_gracia', 'cuaresma', 'navidad', 'diocesis_ninnos', 'diocesis_iglesia',
                 'otras_ofrendas')
    def _calc_total_ofrendas(self):
        self.total_ofrendas = self.bandejas + self.diezmos + self.unidad_gracia + self.cuaresma + self.navidad + \
                              self.diocesis_ninnos + self.diocesis_iglesia + self.otras_ofrendas

    @api.one
    @api.depends('egreso_01', 'egreso_02', 'egreso_03', 'egreso_05', 'egreso_06', 'egreso_07', 'egreso_08',
                 'egreso_09', 'egreso_10', 'egreso_11', 'egreso_12', 'egreso_13', 'egreso_14', 'egreso_15',
                 'egreso_16', 'egreso_17', 'egreso_18')
    def _calc_total_egresos(self):
        self.total_egresos = self.egreso_01 + self.egreso_02 + self.egreso_03 + self.egreso_04 + self.egreso_05 \
                             + self.egreso_06 + self.egreso_07 + self.egreso_08 + self.egreso_09 + self.egreso_10 + \
                             self.egreso_11 + self.egreso_12 + self.egreso_13 + self.egreso_14 + self.egreso_15 + \
                             self.egreso_16 + self.egreso_17 + self.egreso_18

    @api.onchange('congregacion_id')
    def onchange_congregacion_id(self):
        self.sacramentos_ids = False

    @api.onchange('sacramentos_ids')
    def onchange_sacramentos_ids(self):
        "Actualiza los totales"
        bautismos = cb = confirmados = cc = santa_comunion = ccomulgantes = bendiciones = cbendiciones = 0
        for s in self.sacramentos_ids:
            if s.tipo_sacramento == 'bautismo':
                bautismos += 1
            elif s.tipo_sacramento == 'confirmacion':
                confirmados += 1
            elif s.tipo_sacramento == 'bendicion':
                bendiciones += 1
        self.bautismos = bautismos
        self.cantidad_bautizados = bautismos
        self.confirmados = confirmados
        self.cantidad_confirmaciones = confirmados
        self.bendiciones = bendiciones
        self.cantidad_bendiciones = bendiciones

    @api.one
    @api.depends('fecha', 'congregacion_id')
    def _calc_nombre(self):
        if self.fecha and self.congregacion_id:
            self.nombre = str(self.fecha + '-' + self.congregacion_id.nombre).upper()
        else:
            self.nombre = 'Nuevo'