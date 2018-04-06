from odoo import models, api, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    ci = fields.Char('CARNET DE IDENTIDAD')