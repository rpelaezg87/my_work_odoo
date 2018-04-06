# -*- coding: utf-8 -*-

from odoo import models, _, api, fields


class WizardListadoBajas(models.TransientModel):
    _name = 'iglesias.wizard_reporte_lb'
    _inherit = 'iglesias.wizard_commun'

    def _print_report(self, data):
        return self.env['report'].get_action(self, 'iglesias.report_listado_bajas', data=data)

    @api.onchange('fecha_inicio', 'fecha_final')
    def _change_product_ids(self):
        super(WizardListadoBajas, self)._change_product_ids()
        if self.fecha_inicio:
            domain1 = [('miembros_ids.fecha_baja', '>=', self.fecha_inicio)]
            if self.fecha_final:
                domain1 += [('miembros_ids.fecha_baja', '<=', self.fecha_final)]
            domain = {'congregaciones_ids': domain1}
            self.congregaciones_ids = self.env['iglesias.congregacion'].get_congregaciones_con_bajas(self.fecha_inicio,
                                                                                                     self.fecha_final)
            return {'domain': domain}
