# -*- coding: utf-8 -*-

from odoo import models, _, api, fields

SACRAMENTOS = [('bautismo', 'Bautismo'),
               ('confirmacion', 'Confirmacion'),
               ('bendicion', 'Bendicion de matrimonio'),
               ('orden_sagrada', 'Orden sagrada'),
               ('obituario', 'Obituario')]


class WizardListadoXSacaramento(models.TransientModel):
    _name = 'iglesias.wizard_reporte_lbautizos'
    _inherit = 'iglesias.wizard_commun'

    tipo_sacramento = fields.Selection(SACRAMENTOS, required=True)

    def _print_report(self, data):
        return self.env['report'].get_action(self, 'iglesias.report_listado_bautizos', data=data)

    def _build_contexts(self, data):
        result = super(WizardListadoXSacaramento, self)._build_contexts(data)
        result.update({'tipo_sacramento': data['form']['tipo_sacramento'] or False})
        return result

    @api.multi
    def check_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['fecha_inicio', 'fecha_final', 'congregaciones_ids', 'tipo_sacramento'])[0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(used_context, lang=self.env.context.get('lang', 'en_US'))
        return self._print_report(data)

    @api.onchange('fecha_inicio', 'fecha_final', 'tipo_sacramento')
    def _change_product_ids(self):
        super(WizardListadoXSacaramento, self)._change_product_ids()
        if self.fecha_inicio:
            sacramentos = self.env['iglesias.sacramento'].get_sacramentos_entre_fechas(self.tipo_sacramento,
                                                                                       self.fecha_inicio,
                                                                                       self.fecha_final)
            miembro_ids = [s.miembro_id.id for s in sacramentos]
            domain1 = [('miembros_ids.id', 'in', miembro_ids)]
            domain = {'congregaciones_ids': domain1}
            self.congregaciones_ids = self.env['iglesias.congregacion'].search(domain1)
            return {'domain': domain}
