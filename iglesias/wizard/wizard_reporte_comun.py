# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class WizardComun(models.TransientModel):
    _name = 'iglesias.wizard_commun'

    fecha_inicio = fields.Date(string='Fecha de inicio', required=True)
    fecha_final = fields.Date(string='Fecha final')
    congregaciones_ids = fields.Many2many('iglesias.congregacion', string='Congregaciones', required=True,
                                          default=lambda self: self.env['iglesias.congregacion'].search([]))

    @api.onchange('fecha_inicio', 'fecha_final')
    def _change_product_ids(self):
        if self.fecha_final and self.fecha_final:
           if self.fecha_final > self.fecha_final:
                return {
                    'warning': {
                        'title': _("Fecha incorrecta"),
                        'message': _("La fecha de inicio debe ser menor que la fecha final."),
                    },
                }

    def _build_contexts(self, data):
        result = {}
        result['fecha_inicio'] = data['form']['fecha_inicio'] or False
        result['fecha_final'] = data['form']['fecha_final'] or False
        return result

    def _print_report(self, data):
        raise (_('Error!'), _('Not implemented.'))

    @api.multi
    def check_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['fecha_inicio', 'fecha_final', 'congregaciones_ids'])[0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(used_context, lang=self.env.context.get('lang', 'en_US'))
        return self._print_report(data)
