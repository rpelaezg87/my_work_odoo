# -*- coding: utf-8 -*-

import time
from odoo import api, models, fields


class ReportTrialBalance(models.AbstractModel):
    _name = 'report.iglesias.report_ef'

    def _get_saldo_hasta_fecha(self, congregaciones, fecha):
        saldo = 0
        domain = [('congregacion_id', 'in', congregaciones.ids), ('fecha', '<', fecha)]
        servicios = self.env['iglesias.oficio'].search(domain)
        for s in servicios:
            saldo += s.total_ofrendas
            saldo -= s.total_egresos
        return saldo

    def _get_desgloze_entre_fechas(self, congregaciones, fecha1, fecha2):
        result = {}
        domain = [('congregacion_id', 'in', congregaciones.ids), ('fecha', '<=', fecha2)]
        if fecha1:
            domain += [('fecha', '>=', fecha1)]
        servicios = self.env['iglesias.oficio'].search(domain)
        result.update({'diezmos': 0,
                       'bandejas': 0,
                       'unidad_gracia': 0,
                       'cuaresma': 0,
                       'navidad': 0,
                       'diocesis_ninnos': 0,
                       'diocesis_iglesia': 0,
                       'otras_ofrendas': 0,
                       'egreso_01': 0,
                       'egreso_02': 0,
                       'egreso_02': 0,
                       'egreso_03': 0,
                       'egreso_04': 0,
                       'egreso_05': 0,
                       'egreso_06': 0,
                       'egreso_07': 0,
                       'egreso_08': 0,
                       'egreso_09': 0,
                       'egreso_10': 0,
                       'egreso_11': 0,
                       'egreso_12': 0,
                       'egreso_13': 0,
                       'egreso_14': 0,
                       'egreso_15': 0,
                       'egreso_16': 0,
                       'egreso_17': 0,
                       'egreso_18': 0,
                       'saldo': 0
                       })
        for s in servicios:
            result.update({'diezmos': result.get('diezmos', 0) + s.diezmos,
                           'bandejas': result.get('bandejas', 0) + s.bandejas,
                           'unidad_gracia': result.get('unidad_gracia', 0) + s.unidad_gracia,
                           'cuaresma': result.get('cuaresma', 0) + s.cuaresma,
                           'navidad': result.get('navidad', 0) + s.navidad,
                           'diocesis_ninnos': result.get('diocesis_ninnos', 0) + s.diocesis_ninnos,
                           'diocesis_iglesia': result.get('diocesis_iglesia', 0) + s.diocesis_iglesia,
                           'otras_ofrendas': result.get('otras_ofrendas', 0) + s.otras_ofrendas,
                           'egreso_01': result.get('egreso_01', 0) + s.egreso_01,
                           'egreso_02': result.get('egreso_02', 0) + s.egreso_02,
                           'egreso_02': result.get('egreso_02', 0) + s.egreso_02,
                           'egreso_03': result.get('egreso_03', 0) + s.egreso_03,
                           'egreso_04': result.get('egreso_04', 0) + s.egreso_04,
                           'egreso_05': result.get('egreso_05', 0) + s.egreso_05,
                           'egreso_06': result.get('egreso_06', 0) + s.egreso_06,
                           'egreso_07': result.get('egreso_07', 0) + s.egreso_07,
                           'egreso_08': result.get('egreso_08', 0) + s.egreso_08,
                           'egreso_09': result.get('egreso_09', 0) + s.egreso_09,
                           'egreso_10': result.get('egreso_10', 0) + s.egreso_10,
                           'egreso_11': result.get('egreso_11', 0) + s.egreso_11,
                           'egreso_12': result.get('egreso_12', 0) + s.egreso_12,
                           'egreso_13': result.get('egreso_13', 0) + s.egreso_13,
                           'egreso_14': result.get('egreso_14', 0) + s.egreso_14,
                           'egreso_15': result.get('egreso_15', 0) + s.egreso_15,
                           'egreso_16': result.get('egreso_16', 0) + s.egreso_16,
                           'egreso_17': result.get('egreso_17', 0) + s.egreso_17,
                           'egreso_18': result.get('egreso_18', 0) + s.egreso_18,
                           'saldo': result.get('saldo', 0) + s.total_ofrendas - s.total_egresos
                           })

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

        saldo_inicial = self._get_saldo_hasta_fecha(congregaciones, fecha_inicio)
        desgloze = self._get_desgloze_entre_fechas(congregaciones, fecha_inicio, fecha_final)

        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'fecha_inicial': fecha_inicio,
            'fecha_final': fecha_final or fields.date.today(),
            'saldo_inicial': saldo_inicial,
            'desgloze': desgloze,
            'congregaciones':congregaciones
        }
        return self.env['report'].render('iglesias.report_ef', docargs)
