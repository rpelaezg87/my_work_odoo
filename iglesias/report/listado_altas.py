# -*- coding: utf-8 -*-

import time
from odoo import api, models, fields


class ReportListadoAltas(models.AbstractModel):
    _name = 'report.iglesias.report_listado_altas'

    def _get_miembross_con_altas(self, congregaciones, fecha1, fecha2):
        dom = [('es_miembro', '=', True), ('fecha_alta', '>=', fecha1), ('fecha_alta', '<=', fecha2)]
        if congregaciones:
            dom += [('congregacion_id', 'in', congregaciones.ids)]
        return self.env['hr.employee'].search(dom)

    def _get_result(self, congregaciones, fecha1, fecha2):
        result = {}
        miembros = self._get_miembross_con_altas(congregaciones, fecha1, fecha2)
        for miembro in miembros:
                result.setdefault(miembro.congregacion_id, []).append(miembro)
        return result

    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_ids', []))
        congregaciones = data['form'].get('congregaciones_ids', False)
        if congregaciones:
            congregaciones = self.env['iglesias.congregacion'].search([('id', 'in', congregaciones)])
        fecha_inicio = data['form'].get('fecha_inicio', False)
        fecha_final = data['form'].get('fecha_final', False)
        if not fecha_final:
            fecha_final = fields.date.today()
        result = self._get_result(congregaciones, fecha_inicio, fecha_final)

        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'fecha_inicial': fecha_inicio,
            'fecha_final': fecha_final,
            'result': result
        }
        return self.env['report'].render('iglesias.report_listado_altas', docargs)
