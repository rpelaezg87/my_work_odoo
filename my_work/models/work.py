__author__ = 'reinaldo'
# -*- coding: utf-8
from odoo import models, api, fields


class WorkOrder(models.Model):
    _name = 'my_work.work_order'
    _rec_name = 'no_orden'

    @api.one
    def confirmar(self):
        self.state = 'abierto'
        if self.tipo_orden == 'pc':
            self.no_orden = self.env['ir.sequence'].get('work_order_pc')
        else:
            self.no_orden = self.env['ir.sequence'].get('work_order_hdd')

    @api.one
    def pendiente_revisar(self):
        self.state = 'p_revisar'
        if self.tipo_orden == 'pc':
            self.no_orden = self.env['ir.sequence'].get('work_order_pc')
        else:
            self.no_orden = self.env['ir.sequence'].get('work_order_hdd')

    @api.one
    def reparado(self):
        self.state = 'reparado'

    @api.one
    def entregar(self):
        self.state = 'cerrado'

    @api.one
    def sin_solucion(self):
        self.state = 'nts'

    @api.one
    def cancelar(self):
        self.state = 'cancelado'

    @api.one
    def reiniciar(self):
        self.state = 'nuevo'

    @api.model
    def create(self, vals):
        work_order_id = super(WorkOrder, self).create(vals)

        # TODO: this is needed to set given values to first variant after creation
        # these fields should be moved to product as lead to confusion
        vals.update({'work_order_id': work_order_id.id})
        if vals.get('tipo_orden') == 'hdd':
            self.env['my_work.work_order_hdd'].create(vals)
        else:
            self.env['my_work.work_order_pc'].create(vals)

        return work_order_id

    wpc_ids = fields.One2many('my_work.work_order_pc', 'work_order_id', string='ORDENES DE DISCO DURO')
    whdd_ids = fields.One2many('my_work.work_order_hdd', 'work_order_id', string='ORDENES DE HDD')

    a_nombre = fields.Many2one('res.partner', string="A NOMBRE DE")
    ci = fields.Char(related='a_nombre.ci')
    fecha_inicial = fields.Date('FECHA DE LA SOLICITUD', required=True)
    fecha = fields.Date('FECHA DE REPARACION', states={'abierto': [('required', True), ('invisible', False)],
                                                       'cerrado': [('invisible', False)]})
    no_orden = fields.Char('NO DE ORDEN', copy=False, readonly=True, states={'nuevo': [('invisible', True)]})
    piezas = fields.Text('PIEZAS O ACCESORIOS EMPLEADOS')
    state = fields.Selection([('nuevo', 'Nuevo'), ('p_revisar', 'Pendiente a Revisar'), ('abierto', 'En Proceso'),
                              ('reparado', 'Reparado'), ('cerrado', 'Entregado'),
                              ('nts', 'Sin Solucion'), ('cancelado', 'Cancelado')], default='nuevo', string='ESTADO')
    work_done_ids = fields.One2many('my_work.work_done', 'work_order_id', string='TRABAJOS REALIZADOS')
    costo = fields.Float('COSTO DEL SERVICIO')
    realizado_por = fields.Many2one('hr.employee', string="REALIZADO POR")
    entregado_por = fields.Many2one('hr.employee', string="ENTREGADO POR")
    recibido_por = fields.Many2one('res.partner', string="RECIBIDO POR")
    tipo_orden = fields.Selection([('pc', 'PC'), ('hdd', 'HDD')], string='TIPO DE ORDEN', required=True)
    # related de Work_order_PC
    pc = fields.Many2one('my_work.resource_pc', 'EQUIPO', related='wpc_ids.pc', invisible='self.tipo_orden == "hdd"')
    motherboard = fields.Many2one('resource.resource', string='MOTHERBOARD', related='pc.motherboard',
                                  invisible='self.tipo_orden == "hdd"')
    fuente = fields.Many2one('resource.resource', string='FUENTE', related='pc.fuente',
                             invisible='self.tipo_orden == "hdd"')
    memorias_ram = fields.Many2many(related='pc.memorias_ram', invisible='self.tipo_orden == "hdd"')
    lectores = fields.Many2many(related='pc.lectores', invisible='self.tipo_orden == "hdd"')
    hdd = fields.Many2many(related='pc.hdd', invisible='self.tipo_orden == "hdd"')
    chasis = fields.Char(string='CHASIS', related='pc.chasis', invisible='self.tipo_orden == "hdd"')
    cpu = fields.Many2one(related='pc.cpu', invisible='self.tipo_orden == "hdd"')
    otros_nota = fields.Text(related='pc.otros', invisible='self.tipo_orden == "hdd"')
    laptop = fields.Boolean('LAPTOP', related='pc.laptop', invisible='self.tipo_orden == "hdd"')
    # Tipo de trabajo
    mantenimiento = fields.Boolean('MANTENIMIENTO', related='wpc_ids.mantenimiento')
    rmenor = fields.Boolean('REPARACION MENOR', related='wpc_ids.rmenor')
    rmayor = fields.Boolean('REPARACION MAYOR', related='wpc_ids.rmayor')
    otros = fields.Boolean('OTROS SERVICIOS', related='wpc_ids.otros')
    so = fields.Boolean('SISTEMA OPERATIVO', related='wpc_ids.so')
    act = fields.Boolean('ACT. DE SOFT', related='wpc_ids.act')
    insoft = fields.Boolean(related='wpc_ids.insoft')
    antivirus = fields.Boolean('DE ANTIVIRUS', related='wpc_ids.antivirus')
    # related de Work_order_HDD
    hdd_resource = fields.Many2one('my_work.resource_hdd', 'DISCO DURO', related='whdd_ids.hdd')
    recuperacion_datos = fields.Boolean(related='whdd_ids.recuperacion_datos')
    reparcion_hardware = fields.Boolean(related='whdd_ids.reparcion_hardware')
    sus_placa = fields.Boolean('SUSTITUCION DE PLACA', related='whdd_ids.sus_placa')
    sus_componentes = fields.Boolean('SUSTITUCION DE COMPONENTES', related='whdd_ids.sus_componentes')
    no_placa = fields.Char('#PLACA', related='hdd_resource.no_placa')
    marca = fields.Many2one('my_work.marca_hdd', related='hdd_resource.marca')
    no_serie = fields.Char(related='hdd_resource.no_serie')
    firw = fields.Char(related='hdd_resource.firw')
    capacidad = fields.Many2one(related='hdd_resource.capacidad')
    tipo_conexion = fields.Selection(related='hdd_resource.tipo_conexion')


class WorkOrderPc(models.Model):
    _inherits = {'my_work.work_order': 'work_order_id'}
    _name = 'my_work.work_order_pc'

    # @api.one
    # def confirmar(self):
    #     self.work_order_id.no_orden = self.env['ir.sequence'].get('my_work.sequence_work_order_pc')

    pc = fields.Many2one('my_work.resource_pc', 'EQUIPO',
                         context="{'default_resource_type':'material'}")
    work_order_id = fields.Many2one('my_work.work_order', 'ORDEN DE TRABAJO', required=True, ondelete="cascade")
    mantenimiento = fields.Boolean('MANTENIMIENTO')
    rmenor = fields.Boolean('REPARACION MENOR')
    rmayor = fields.Boolean('REPARACION MAYOR')
    otros = fields.Boolean('OTROS SERVICIOS')
    so = fields.Boolean('SISTEMA OPERATIVO')
    act = fields.Boolean('ACT. DE SOFT')
    insoft = fields.Boolean('INST. SOFT ACT')
    antivirus = fields.Boolean('DE ANTIVIRUS')


class WorkOrderHdd(models.Model):
    _inherits = {'my_work.work_order': 'work_order_id'}
    _name = 'my_work.work_order_hdd'

    @api.one
    def confirmar(self):
        super(WorkOrderPc, self).confirmar()
        self.work_order_id.no_orden = self.env['ir.sequence'].get('my_work.sequence_work_order_hdd')

    hdd = fields.Many2one('my_work.resource_hdd', 'DISCO DURO',
                          context="{'default_resource_cat':'hdd',"
                                   "'default_resource_type':'material'}")
    recuperacion_datos = fields.Boolean('RECUPERACION DE DATOS')
    reparcion_hardware = fields.Boolean('REPARACION DE HARDWARE')
    sus_placa = fields.Boolean('SUSTITUCION DE PLACA')
    sus_componentes = fields.Boolean('SUSTITUCION DE COMPONENTES')
    no_placa = fields.Char('#PLACA', related='hdd.no_placa')
    work_order_id = fields.Many2one('my_work.work_order', 'ORDEN DE TRABAJO', required=True, ondelete="cascade")


class WorkType(models.Model):
    _name = 'my_work.work_type'

    nombre = fields.Char(string='TIPO DE SERVICIO', required=True)


class ResourceDescriptionPC(models.Model):
    _inherit = 'resource.resource'
    _name = 'my_work.resource_pc'

    motherboard = fields.Many2one('resource.resource', string='MOTHERBOARD',
                                  domain="[('resource_cat','=','motherboard')]",
                                  context="{'default_resource_cat':'motherboard',"
                                          "'default_resource_type':'material'}")
    fuente = fields.Many2one('resource.resource', string='FUENTE', domain="[('resource_cat','=','fuente_pc')]",
                             context="{'default_resource_cat':'fuente_pc',"
                                     "'default_resource_type':'material'}")
    memorias_ram = fields.Many2many('resource.resource', 'my_work_resource_pc_ram_rel', string='MEMORIAS RAM',
                                    domain="[('resource_cat','=','ram')]",
                                    context="{'default_resource_cat':'ram',"
                                            "'default_resource_type':'material'}")
    lectores = fields.Many2many('resource.resource', 'my_work_resource_pc_lectores_rel', string='LECTORES', domain="[('resource_cat','=','lectores')]",
                               context="{'default_resource_cat':'lectores',"
                                       "'default_resource_type':'material'}")
    hdd = fields.Many2many('my_work.resource_hdd', 'my_work_resources_pc_hdd_rel', string='HDD',
                           context="{'default_resource_cat':'hdd',"
                                   "'default_resource_type':'material'}")
    chasis = fields.Char(string='CHASIS')
    cpu = fields.Many2one('resource.resource', string='CPU', domain="[('resource_cat','=','cpu')]",
                          context="{'default_resource_cat':'cpu',"
                                  "'default_resource_type':'material'}")
    otros = fields.Text('OTROS')
    laptop = fields.Boolean('LAPTOP')


class MarcaHdd(models.Model):
    _name = 'my_work.marca_hdd'
    _rec_name = 'marca'

    code = fields.Char('CODIGO')
    marca = fields.Char('MARCA')


class ResourceDescriptionHDD(models.Model):
    _inherit = 'resource.resource'
    _name = 'my_work.resource_hdd'

    marca = fields.Many2one('my_work.marca_hdd', string='MARCA')
    no_placa = fields.Char('#PLACA')
    no_serie = fields.Char('#SERIE', related='code', readonly=True)
    firw = fields.Char('FIRW')
    capacidad = fields.Many2one('my_work.hdd_capacity', string='CAP')
    tipo_conexion = fields.Selection([('sata', 'SATA'), ('ide', 'IDE')], string='TIPO DE CONEX')


class HDDCapacity(models.Model):
    _name = 'my_work.hdd_capacity'

    name = fields.Char('CAPACIDAD', required=True)


class WorkDone(models.Model):
    _name = 'my_work.work_done'
    _order = 'no asc'

    no = fields.Integer('NO')
    denominacion = fields.Char('DENOMINACION')
    precio = fields.Float('PRECIO')
    importe = fields.Float('IMPORTE')
    work_order_id = fields.Many2one('my_work.work_order', 'Orden de Trabajo')


class ResourseResource(models.Model):
    _inherit = 'resource.resource'

    @api.multi
    def name_get(self):
        #result = super(ResourseResource, self).name_get()
        result = []
        for resource in self:
            result.append((resource.id,
                           '[%s] %s' % (resource.code, resource.name)))
        return result



    resource_cat = fields.Selection([('ram', 'MEMORIA RAM'), ('cpu', 'CPU'), ('lectores', 'LECTORES'),
                                     ('fuente_pc', 'FUENTE INTERNA DE PC'), ('motherboard', 'MOTHERBOARD'),
                                     ('hdd','DISCO DURO')],
                                    string="Categoria de recurso")
