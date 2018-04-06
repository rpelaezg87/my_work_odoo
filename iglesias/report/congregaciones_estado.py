# -*- coding: utf-8 -*-

import time
from odoo import api, models, fields


class ReportTrialBalance(models.AbstractModel):
    _name = 'report.iglesias.report_ce'

    def _get_total_sacramento(self, congregaciones, tipo_sacramento, fecha1=False, fecha2=fields.Date.today()):
        domain = [('congregacion_id', 'in', congregaciones.ids), ('tipo_sacramento', '=', tipo_sacramento),
                  ('fecha', '<=', fecha2)]

        if fecha1:
            domain += [('fecha', '>=', fecha1)]
        sacramentos = self.env['iglesias.sacramento'].search(domain)
        return len(sacramentos)

    def _get_totales_sin_fecha(self, congregaciones):
        result = {}
        fecha = fields.Date.today()
        parroquias = misiones = extensiones = 0
        for c in congregaciones:
            if c.status == 'parroquia':
                parroquias += 1
            elif c.status == 'misiones':
                misiones += 1
            elif c.status == 'extensiones':
                extensiones += 1
        miembros = self.env['hr.employee'].search([('congregacion_id', 'in', congregaciones.ids),
                                                   ('es_miembro', '=', True)])
        for c in congregaciones:
            for l in c.liderazgo_ids:
                miembros |= l.employee_id
        diezmadores = 0
        ninnas = 0
        ninnos = 0
        m_jovenes = 0
        h_jovenes = 0
        m_adultos = 0
        h_adultos = 0
        ancianas = 0
        ancianos = 0
        familias = set()
        for miembro in miembros:
            if miembro.es_diezmador:
                diezmadores += 1
            familias.add(miembro.no_familia)
            if fecha >= miembro.birthday:
                if miembro.edad <= 14:
                    if miembro.gender == 'female':
                        ninnas += 1
                    else:
                        ninnos += 1
                elif miembro.edad >= 15 and miembro.edad <= 29:
                    if miembro.gender == 'female':
                        m_jovenes += 1
                    else:
                        h_jovenes += 1
                elif miembro.edad >= 30 and miembro.edad <= 59:
                    if miembro.gender == 'female':
                        m_adultos += 1
                    else:
                        h_adultos += 1
                elif miembro.edad >= 60:
                    if miembro.gender == 'female':
                        ancianas += 1
                    else:
                        ancianos += 1
        result.update({'diezmadores': diezmadores,
                       'parroquias': parroquias,
                       'misiones': misiones,
                       'extensiones': extensiones,
                       'familias': len(familias),
                       'ninnas': ninnas,
                       'ninnos': ninnos,
                       'm_jovenes': m_jovenes,
                       'h_jovenes': h_jovenes,
                       'm_adultos': m_adultos,
                       'h_adultos': h_adultos,
                       'ancianas': ancianas,
                       'ancianos': ancianos,
                       'bautizados': self._get_total_sacramento(congregaciones, 'bautismo'),
                       'confirmaciones': self._get_total_sacramento(congregaciones, 'confirmacion'),
                       'bendiciones': self._get_total_sacramento(congregaciones, 'bendicion'),
                       'total_miembros': len(miembros)
                       })
        return result

    def _get_servicios(self, congregaciones, fecha1=False, fecha2=fields.Date.today()):
        sta_com = otros = 0
        domain = [('congregacion_id', 'in', congregaciones.ids), ('fecha', '<=', fecha2)]
        if fecha1:
            domain += [('fecha', '>=', fecha1)]
        servicios = self.env['iglesias.oficio'].search(domain)
        asistencias_comunion = asistencias_otros = 0
        for s in servicios:
            if s.actividad == 'comunion':
                asistencias_comunion += s.asistencia_total
                sta_com += 1
            elif s.actividad == 'otros':
                otros += 1
                asistencias_otros += s.asistencia_total
        promedio_comunion = promedio_otros = 0
        if asistencias_comunion:
            promedio_comunion = round(float(asistencias_comunion) / sta_com, 2)
        if asistencias_otros:
            promedio_otros = round(float(asistencias_otros) / otros, 2)

        return sta_com, otros, promedio_comunion, promedio_otros,

    def _get_total_membresia_hasta_fecha(self, congregaciones, fecha):
        result = {}
        altas = self.env['hr.employee'].search([('congregacion_id', 'in', congregaciones.ids),
                                                ('fecha_alta', '<=', fecha),
                                                ('es_miembro', '=', True)])
        bajas = self.env['hr.employee'].search([('congregacion_id', 'in', congregaciones.ids),
                                                ('fecha_baja', '<=', fecha),
                                                ('es_miembro', '=', True)])

        bajas_traslado = 0
        bajas_fallecidos = 0
        for miembro in bajas:
            if miembro.causa == 'traslado':
                bajas_traslado += 1
            elif miembro.causa == 'fallecido':
                bajas_fallecidos += 1

        visitantes = 0
        catecumenos = 0
        comulgantes = 0
        pasivos = 0

        for miembro in altas:
            if miembro.membresia == 'visitante':
                visitantes += 1
            elif miembro.membresia == 'catecumeno':
                catecumenos += 1
            elif miembro.membresia == 'comulgante':
                comulgantes += 1
            elif miembro.membresia == 'pasivo':
                pasivos += 1
        sta_comunion, otros, promedio_comunion, promedio_otros = self._get_servicios(congregaciones, False, fecha)
        result.update({'altas': len(altas),
                       'bajas': len(bajas),
                       'bajas_traslado': bajas_traslado,
                       'bajas_fallecido': bajas_fallecidos,
                       'visitantes': visitantes,
                       'catecumenos': catecumenos,
                       'comulgantes': comulgantes,
                       'pasivos': pasivos,
                       'bautizados': self._get_total_sacramento(congregaciones, 'bautismo', False, fecha),
                       'confirmaciones': self._get_total_sacramento(congregaciones, 'confirmacion', False, fecha),
                       'bendiciones': self._get_total_sacramento(congregaciones, 'bendicion', False, fecha),
                       'servicio_sta_comunion': sta_comunion,
                       'servicio_otros': otros,
                       'promedio_comunion': promedio_comunion,
                       'promedio_otros': promedio_otros
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
            fecha_final = fields.Date.today()
        total_membresia_fecha1 = {}
        total_membresia_fecha2 = {}
        if fecha_inicio:
            total_membresia_fecha1 = self._get_total_membresia_hasta_fecha(congregaciones, fecha_inicio)
            total_membresia_fecha2 = self._get_total_membresia_hasta_fecha(congregaciones, fecha_final)
        sta_com, otros, promedio_comunion, promedio_otros = self._get_servicios(congregaciones, fecha_inicio,
                                                                                fecha_final)

        totales_sin_fecha = self._get_totales_sin_fecha(congregaciones)

        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'congregaciones': congregaciones,
            'total_membresia_fecha1': total_membresia_fecha1,
            'total_membresia_fecha2': total_membresia_fecha2,
            'totales_sin_fecha': totales_sin_fecha,
            'pc_entre_fechas': promedio_comunion,
            'po_entre_fechas': promedio_otros,
            'fecha_inicio': fecha_inicio,
            'fecha_final': fecha_final or fields.Date.today()
        }
        return self.env['report'].render('iglesias.report_ce', docargs)
