# -*- coding: utf-8 -*-

from odoo import models, _


class WizardComun(models.TransientModel):
    _name = 'iglesias.wizard_reporte_ec'
    _inherit = 'iglesias.wizard_commun'

    def _print_report(self, data):
        return self.env['report'].get_action(self, 'iglesias.report_ce', data=data)

