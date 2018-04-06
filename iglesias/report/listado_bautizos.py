# -*- coding: utf-8 -*-

import time
from odoo import api, models, fields


class ReportListadoBajas(models.AbstractModel):
    _name = 'report.iglesias.report_listado_bautizos'

    def _get_result(self, congregaciones, fecha1, fecha2):
        result = {}
        sacramentos = self.env['iglesias.sacramento'].get_sacramentos_entre_fechas('bautismo', fecha1, fecha2, congregaciones.ids)
        for s in sacramentos:
                result.setdefault(s.miembro_id.congregacion_id, []).append(s)
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
        tipo_sacramento = data['form'].get('tipo_sacramento', False)
        if not fecha_final:
            fecha_final = fields.date.today()
        result = self._get_result(congregaciones, fecha_inicio, fecha_final)
        if tipo_sacramento == 'bautismo':
            title = "Listado de los hermanos bautizados"
        elif tipo_sacramento == 'confirmacion':
            title = "Listado de los hermanos confirmados"
        elif tipo_sacramento == 'bendicion':
            title = "Listado de los hermanos bendecidos en matrimonio"
        elif tipo_sacramento == 'orden_sagrada':
            title = "Listado de los hermanos en Orden sagrada"
        else:
            title = "Listado de los hermanos en Obituario"

        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'fecha_inicial': fecha_inicio,
            'fecha_final': fecha_final,
            'result': result,
            'tipo_sacramento': tipo_sacramento,
            'title': title
        }
        return self.env['report'].render('iglesias.report_listado_bautizos', docargs)
