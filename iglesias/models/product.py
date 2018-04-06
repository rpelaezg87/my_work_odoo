# -*- coding: utf-8 -*-
from odoo import models, fields, api
ESTADO = [('bueno', 'Bueno'), ('regular', 'Regular'), ('deficiente', 'Deficiente')]
class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _order = 'default_code'

    congregacion_id = fields.Many2one('iglesias.congregacion', 'Congregación')
    ministro_id = fields.Many2one('hr.employee', 'Ministro a Cargo',
                                  related='congregacion_id.ministro_id', readonly=True)
    responsable_id = fields.Many2one('hr.employee', 'Responsable')
    direccion = fields.Text('Dirección')
    estado_tecnico = fields.Selection(ESTADO, 'Estado técnico')
    fecha_alta = fields.Date('Fecha de alta')
    fecha_baja = fields.Date('Fecha de baja')
    observaciones = fields.Text('Observaciones')

    @api.onchange('responsable_id')
    def onchange_responsable(self):
        if self.responsable_id and self.responsable_id.address_home_id:
            self.direccion = self.responsable_id.address_home_id.contact_address