# -*- coding: utf-8 -*-
from odoo import models, fields

class Contacts(models.Model):
    _inherit = 'res.partner'

    congregacion_id = fields.Many2one('iglesias.congregacion', 'Congregación')