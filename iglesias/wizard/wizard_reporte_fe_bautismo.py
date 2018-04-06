# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class WizardFeBautismo(models.TransientModel):
    _name = 'iglesias.wizard_fe_bautismo'

    congregacion_id = fields.Many2one('iglesias.congregacion', 'Congregación')
    fecha = fields.Date(string='Fecha de bautismo')
    miembros_ids = fields.Many2many('hr.employee', string='Hermanos', required=True)

    @api.onchange('congregacion_id', 'fecha')
    def _change_miembros_ids(self):
        bautismo_ids = self.env['iglesias.sacramento'].search([('tipo_sacramento', '=', 'bautismo')])
        confirmacion_ids = self.env['iglesias.sacramento'].search([('tipo_sacramento', '=', 'confirmacion')])
        if bautismo_ids and confirmacion_ids:
            domain1 = [('id', 'in', [c.miembro_id.id for c in confirmacion_ids])]
            if self.congregacion_id:
                domain1 += [('congregacion_id', '=', self.congregacion_id.id)]
            if self.fecha:
                bautismofecha_ids = self.env['iglesias.sacramento'].search([('id', 'in', bautismo_ids.ids),
                                                                            ('fecha', '=', self.fecha)])
                domain1 += [('id', 'in', [b.miembro_id.id for b in bautismofecha_ids])]
            else:
                domain1 += [('id', 'in', [b.miembro_id.id for b in bautismo_ids])]
            domain = {'miembros_ids': domain1}
            if self.congregacion_id or self.fecha:
                self.miembros_ids = self.env['hr.employee'].search(domain1)
            return {'domain': domain}

    @api.multi
    def print_report(self):
        self.ensure_one()
        return self.miembros_ids.print_fe_bautismo()