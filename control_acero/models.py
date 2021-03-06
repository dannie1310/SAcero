from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from decimal import Decimal
import datetime
from django.contrib.auth.models import User

class Factor(models.Model):
	pva = models.IntegerField()
	factorPulgada = models.DecimalField(max_digits=20,decimal_places=4,default=Decimal('0.0000'), null=True)
	pi = models.DecimalField(max_digits=20,decimal_places=4,default=Decimal('0.0000'), null=True)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaActualizacion = models.DateTimeField(auto_now=True, null=True)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return unicode(self.estatus)

class Material(models.Model):
	nombre = models.CharField(blank=True, max_length=100)
	numero = models.IntegerField(default=0)
	proveedor = models.CharField(default=0, max_length=20)
	ESTATUSTIPO = (
	    (1, 'Recto'),
	    (2, 'Rollo'),
	)
	tipo = models.IntegerField(choices=ESTATUSTIPO, default=1)
	diametro = models.DecimalField(max_digits=20,decimal_places=4,default=Decimal('0.0000'), null=True)
	peso = models.DecimalField(max_digits=20,decimal_places=4,default=Decimal('0.0000'), null=True)
	longitud = models.IntegerField(null=True)
	factor = models.ForeignKey(Factor, null=True)
	imagen = models.FileField(upload_to='materiales', null=True)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return self.nombre

class Despiece(models.Model):
	nomenclatura = models.CharField(max_length=100)
	cantidad = models.IntegerField(default=1)
	longitud = models.FloatField(default=0)
	peso = models.DecimalField(max_digits=20,decimal_places=4,default=Decimal('0.0000'), null=True)
	figura = models.CharField(default=1, max_length=20)
	imagen = models.FileField(upload_to='despieces', null=True)
	material = models.ManyToManyField(
		'material',
		blank=True,
	)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaActualizacion = models.DateTimeField(auto_now=True, null=True)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return self.nomenclatura

class Elemento(models.Model):
	nombre = models.CharField(max_length=100)
	ESTATUSTIPO = (
	    (0, 'Un apoyo'),
	    (1, 'Entre apoyos'),
	)
	tipo = models.IntegerField(choices=ESTATUSTIPO, default=0)
	peso = models.FloatField(default=0)
	imagen = models.FileField(upload_to='imagen', null=True)
	material = models.ManyToManyField(
		'material',
		blank=True,
	)
	despiece = models.ManyToManyField(
		'despiece',
		blank=True,
	)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaActualizacion = models.DateTimeField(auto_now=True, null=True)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return self.nombre

class Transporte(models.Model):
	TIPOTRANSPORTE = (
	    (1, 'Local'),
	    (2, 'Tercero'),
	)
	tipo = models.IntegerField(choices=TIPOTRANSPORTE, default=1)
	capacidad = models.IntegerField()
	placas = models.CharField(max_length=20)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return self.placas

class Funcion(models.Model):
	TIPOFUNCION = (
	    (1, 'Suministrador'),
	    (2, 'Habilitador'),
	    (3, 'Armador'),
	    (4, 'Colocador'),
	)
	tipo = models.IntegerField(choices=TIPOFUNCION, default=1)
	proveedor = models.CharField(max_length=20)
	porcentajeMaximo = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return self.proveedor

class Taller(models.Model):
	nombre = models.CharField(max_length=100)
	responsable = models.CharField(max_length=100, null=True)
	identificacionFolio = models.CharField(max_length=20, null=True)
	ubicacion = models.CharField(max_length=100)
	funcion = models.ForeignKey(Funcion, null=True)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	user = models.ManyToManyField(
		User,
		blank=True,
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return self.nombre

class Frente(models.Model):
	nombre = models.CharField(max_length=100)
	identificacion = models.CharField(max_length=100)
	ubicacion = models.CharField(max_length=100)
	ideFolio = models.CharField(max_length=20, null=True)
	kilometros = models.FloatField(default=0)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	user = models.ManyToManyField(
		User,
		blank=True,
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return self.nombre

class Apoyo(models.Model):
	numero = models.CharField(max_length=100)
	elemento = models.ManyToManyField(
		'elemento',
	)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	frente = models.ForeignKey(Frente, null=True)
	fechaActualizacion = models.DateTimeField(auto_now=True)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return unicode(self.estatus)

class Entrada(models.Model):
	taller = models.ForeignKey(Taller, null=True)
	apoyo = models.ForeignKey(Apoyo, null=True)
	elemento = models.ForeignKey(Elemento, null=True)
	funcion = models.ForeignKey(Funcion, null=True)
	total = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	folioSalida = models.CharField(max_length=20,null=True)
	remision = models.CharField(max_length=50,null=True)
	armador = models.CharField(max_length=100,null=True)
	frente = models.ForeignKey(Frente, null=True)
	numFolio = models.IntegerField(null=True)
	folio = models.CharField(max_length=20,null=True)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaActualizacion = models.DateTimeField(auto_now=True)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return unicode(self.estatus)

class EntradaResumen(models.Model):
	material = models.ForeignKey(Material, null=True)
	pesoRemision = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	pesoReal = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	TIPORECEPCION = (
	    (0, 'Completo'),
	    (1, 'Faltante'),
	    (2, 'Sobrante'),
	)
	tipoRecepcion = models.IntegerField(choices=TIPORECEPCION, default=1)
	entrada = models.ForeignKey(Entrada, null=True)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaActualizacion = models.DateTimeField(auto_now=True)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return unicode(self.estatus)

class EntradaDetalle(models.Model):
	nomenclatura = models.CharField(max_length=20,null=True)
	longitud = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	piezas = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	calculado = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	entradaResumen = models.ForeignKey(EntradaResumen, null=True)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaActualizacion = models.DateTimeField(auto_now=True)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return self.nomenclatura

class Folio(models.Model):
	modulo = models.IntegerField()
	descripcion = models.CharField(max_length=10)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaActualizacion = models.DateTimeField(auto_now=True)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return unicode(self.estatus)

class InventarioFisico(models.Model):
	numFolio = models.IntegerField(null=True)
	folio = models.CharField(max_length=20,null=True)
	numConteo = models.IntegerField(null=True)
	tallerAsignado = models.ForeignKey(Taller, null=True, related_name='tallerAsignadoInventario')
	noEntradas = models.IntegerField(null=True)
	totalEntradas = models.IntegerField(null=True)
	noSalidas = models.IntegerField(null=True)
	totalSalidas = models.IntegerField(null=True)
	totalExistencias = models.IntegerField(null=True)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	ESTATUSREGISTRO = (
	    (0, 'Abierto'),
	    (1, 'Cerrado'),
	)
	estatusRegistro = models.IntegerField(choices=ESTATUSREGISTRO, default=0)
	ESTATUSCIERRE = (
	    (0, 'Abierto'),
	    (1, 'Cerrado'),
	)
	estatusCierre = models.IntegerField(choices=ESTATUSCIERRE, default=0)
	fechaActualizacion = models.DateTimeField(auto_now=True)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return unicode(self.estatus)

class InventarioFisicoDetalle(models.Model):
	inventarioFisico = models.ForeignKey(InventarioFisico, null=True)
	material = models.ForeignKey(Material, null=True)
	pesoExistencia = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	pesoFisico = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	diferencia = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	EXISTENCIA = (
	    (0, 'Existente'),
	    (1, 'Inexistente'),
	)
	tipoExistencia = models.IntegerField(choices=EXISTENCIA, default=0)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaActualizacion = models.DateTimeField(auto_now=True)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return unicode(self.estatus)

class InventarioFisicoDetalleCompleto(models.Model):
	InventarioFisicoDetalle = models.ForeignKey(InventarioFisicoDetalle, null=True)
	material = models.ForeignKey(Material, null=True)
	peso = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	piezas = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	longitud = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	ESTATUSTIPOV = (
	    (0, 'No'),
	    (1, 'No Habilitada'),
	    (2, 'Proceso'),
	    (3, 'Habilitada'),
	)
	estatusTipoV = models.IntegerField(choices=ESTATUSTIPOV, default=0)
	referencia = models.CharField(max_length=50, null=True)
	ESTATUSPENDIENTE = (
	    (0, 'Pendiente'),
	    (1, 'Activo'),
	)
	estatusDetalle = models.IntegerField(choices=ESTATUSPENDIENTE, default=0)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaActualizacion = models.DateTimeField(auto_now=True)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return unicode(self.estatus)

class InventarioFisicoDetalleCierre(models.Model):
	inventarioFisico = models.ForeignKey(InventarioFisico, null=True)
	material = models.ForeignKey(Material, null=True)
	pesoExistencia = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	pesoFisico = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	diferencia = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	cantidadEntrada = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	observacionEntrada = models.CharField(max_length=150,null=True)
	cantidadSalida = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	observacionSalida = models.CharField(max_length=150,null=True)
	numFolio = models.IntegerField(null=True)
	folio = models.CharField(max_length=20,null=True)
	tallerAsignado = models.ForeignKey(Taller, null=True, related_name='tallerAsignadoInventarioCierre')
	EXISTENCIA = (
	    (0, 'Existente'),
	    (1, 'Inexistente'),
	)
	tipoExistencia = models.IntegerField(choices=EXISTENCIA, default=0)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaActualizacion = models.DateTimeField(auto_now=True)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return unicode(self.estatus)

class Remision(models.Model):
	idOrden = models.CharField(max_length=20,null=True)
	remision = models.CharField(max_length=50,null=True)
	funcion = models.ForeignKey(Funcion, null=True)
	tallerAsignado = models.ForeignKey(Taller, null=True, related_name='tallerAsignado')
	pesoTara = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	pesoBruto = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	pesoNeto = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	pesoRemision = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	observacion = models.CharField(max_length=100,null=True)
	frente = models.ForeignKey(Frente, null=True)
	ajuste= models.ForeignKey(InventarioFisico, null=True, related_name='ajusteEntrada')
	fechaRemision = models.DateField()
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaActualizacion = models.DateTimeField(auto_now=True)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return self.idOrden

	class Meta:
	    permissions = (
	        ("add_materiales", "Puede Agregar Materiales"),
	        ("change_materiales", "Puede Actualizar Materiales"),
	        ("delete_materiales", "Puede Borrar Materiales"),
	        ("add_despieces", "Puede Agregar Despieces"),
	        ("change_despieces", "Puede Actualizar Despieces"),
	        ("delete_despieces", "Puede Borrar Despieces"),
	        ("add_elementos", "Puede Agregar Elementos"),
	        ("change_elementos", "Puede Actualizar Elementos"),
	        ("delete_elementos", "Puede Borrar Elementos"),
	        ("add_apoyos", "Puede Agregar Apoyos"),
	        ("change_apoyos", "Puede Actualizar Apoyos"),
	        ("delete_apoyos", "Puede Borrar Apoyos"),
	        ("add_frentes", "Puede Agregar Frentes"),
	        ("change_frentes", "Puede Actualizar Frentes"),
	        ("delete_frentes", "Puede Borrar Frentes"),
	        ("add_proveedores", "Puede Agregar Proveedores"),
	        ("change_proveedores", "Puede Actualizar Proveedores"),
	        ("delete_proveedores", "Puede Borrar Proveedores"),
	        ("add_talleres", "Puede Agregar Talleres"),
	        ("change_talleres", "Puede Actualizar Talleres"),
	        ("delete_talleres", "Puede Borrar Talleres"),
	        ("add_transportes", "Puede Agregar Transportes"),
	        ("change_transportes", "Puede Actualizar Transportes"),
	        ("delete_transportes", "Puede Borrar Transportes"),
	        ("view_recepcion_material", "Puede Visualizar Recepcion del Material del Fabricante"),
	        ("view_salida_habilitado", "Puede Visualizar Salida de Habilitado"),
	        ("view_armado_recepcion", "Puede Visualizar Armado Recepcion"),
	        ("view_inventario_fisico", "Puede Visualizar el Inventario Fisico"),
	        ("view_reportes", "Puede Visualizar Reportes"),
	        ("view_movimientos", "Puede Visualizar los Movimientos Realizados"),
	        ("closing_inventarios", "Puede Ajustar un Inventario Fisico"),
	        ("delete_folios", "Puede Borrar Folios"),
	    )

class RemisionDetalle(models.Model):
	remision = models.ForeignKey(Remision, null=True)
	material = models.ForeignKey(Material, null=True)
	peso = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	cantidad = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	apoyo = models.ForeignKey(Apoyo)
	elemento = models.ForeignKey(Elemento)
	longitud = models.IntegerField(null=True)
	numFolio = models.IntegerField(null=True)
	folio = models.CharField(max_length=20,null=True)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	ESTATUSINVENTARIO = (
	    (0, 'No'),
	    (1, 'En Proceso'),
	    (2, 'Si'),
	)
	estatusInventario = models.IntegerField(choices=ESTATUSINVENTARIO, default=0)
	folioInventario = models.IntegerField(null=True)
	ESTATUSTIPO = (
	    (0, 'No'),
	    (1, 'Recta'),
	    (2, 'Rollo'),
	)
	estatusTipo = models.IntegerField(choices=ESTATUSTIPO, default=0)
	fechaActualizacion = models.DateTimeField(auto_now=True)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return self.remision

class InventarioRemisionDetalle(models.Model):
	remision = models.ForeignKey(Remision, null=True)
	material = models.ForeignKey(Material, null=True)
	peso = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	cantidad = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	apoyo = models.ForeignKey(Apoyo)
	elemento = models.ForeignKey(Elemento)
	longitud = models.IntegerField(null=True)
	numFolio = models.IntegerField(null=True)
	folio = models.CharField(max_length=20,null=True)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	estatusTotalizado = models.IntegerField(default=1)
	ESTATUSINVENTARIO = (
	    (0, 'No'),
	    (1, 'En Proceso'),
	    (2, 'Si'),
	)
	estatusInventario = models.IntegerField(choices=ESTATUSINVENTARIO, default=0)
	folioInventario = models.IntegerField(null=True)
	fechaActualizacion = models.DateTimeField(auto_now=True)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return self.remision

class Salida(models.Model):
	peso = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	cantidad = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	tiempoEntrega = models.IntegerField(null=True)
	funcion = models.ForeignKey(Funcion, null=True)
	taller = models.ForeignKey(Taller, null=True)
	material = models.ForeignKey(Material, null=True)
	transporte = models.ForeignKey(Transporte, null=True)
	apoyo = models.ForeignKey(Apoyo, null=True)
	elemento = models.ForeignKey(Elemento, null=True)
	cantidadReal = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	cantidadAsignada = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	idEtapaPertenece = models.IntegerField(null=True)
	idOrdenTrabajo = models.IntegerField(null=True)
	remision = models.CharField(max_length=50,null=True)
	frente = models.ForeignKey(Frente, null=True)
	estatusEtapa = models.IntegerField(default=1)
	ajuste= models.ForeignKey(InventarioFisico, null=True, related_name='ajusteSalida')
	numFolio = models.IntegerField(null=True)
	folio = models.CharField(max_length=20,null=True)
	tallerAsignado = models.ForeignKey(Taller, null=True, related_name='tallerAsignadoSalida')
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	TIPOESTATUS = (
	    (1, 'En proceso'),
	    (2, 'Recepcionado'),
	    (3, 'Enviado'),
	    (4, 'Rechazado'),
	)
	tipoEstatus = models.IntegerField(choices=TIPOESTATUS, default=1)
	TIPORECEPCION = (
	    (0, 'Parcial'),
	    (1, 'Total'),
	)
	tipoRecepcion = models.IntegerField(choices=TIPORECEPCION, default=1)
	ESTATUSINVENTARIO = (
	    (0, 'No'),
	    (1, 'En Proceso'),
	    (2, 'Si'),
	)
	estatusInventario = models.IntegerField(choices=ESTATUSINVENTARIO, default=0)
	folioInventario = models.IntegerField(null=True)
	fechaActualizacion = models.DateTimeField(auto_now=True)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	ESTATUSREPOSICION = (
	    (2, 'No'),
	    (1, 'Si'),
	)
	estatusReposicion = models.IntegerField(choices=ESTATUSREPOSICION, default=0)
	estatusApoyo = models.IntegerField(default=0)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return unicode(self.estatus)

class InventarioSalida(models.Model):
	peso = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	cantidad = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	tiempoEntrega = models.IntegerField(null=True)
	funcion = models.ForeignKey(Funcion, null=True)
	taller = models.ForeignKey(Taller, null=True)
	material = models.ForeignKey(Material, null=True)
	transporte = models.ForeignKey(Transporte, null=True)
	apoyo = models.ForeignKey(Apoyo, null=True)
	elemento = models.ForeignKey(Elemento, null=True)
	cantidadReal = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	cantidadAsignada = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	idEtapaPertenece = models.IntegerField(null=True)
	idOrdenTrabajo = models.IntegerField(null=True)
	remision = models.CharField(max_length=50,null=True)
	frente = models.ForeignKey(Frente, null=True)
	estatusEtapa = models.IntegerField(default=1)
	numFolio = models.IntegerField(null=True)
	folio = models.CharField(max_length=20,null=True)
	tallerAsignado = models.ForeignKey(Taller, null=True, related_name='tallerAsignadoSalidaInventario')
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	estatusTotalizado = models.IntegerField(default=1)
	TIPOESTATUS = (
	    (1, 'En proceso'),
	    (2, 'Recepcionado'),
	    (3, 'Enviado'),
	    (4, 'Rechazado'),
	)
	tipoEstatus = models.IntegerField(choices=TIPOESTATUS, default=1)
	TIPORECEPCION = (
	    (0, 'Parcial'),
	    (1, 'Total'),
	)
	tipoRecepcion = models.IntegerField(choices=TIPORECEPCION, default=1)
	ESTATUSINVENTARIO = (
	    (0, 'No'),
	    (1, 'En Proceso'),
	    (2, 'Si'),
	)
	estatusInventario = models.IntegerField(choices=ESTATUSINVENTARIO, default=0)
	folioInventario = models.IntegerField(null=True)
	fechaActualizacion = models.DateTimeField(auto_now=True)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	estatusApoyo = models.IntegerField(default=0)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return unicode(self.estatus)

class Modulo(models.Model):
	descripcion = models.CharField(max_length=100)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaActualizacion = models.DateTimeField(auto_now=True)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return unicode(self.estatus)

class Bitacora(models.Model):
	user = models.ForeignKey(User)
	modulo = models.ForeignKey(Modulo)
	accion = models.CharField(max_length=100)
	id_afectado = models.IntegerField()
	observacion = models.CharField(max_length=200)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaActualizacion = models.DateTimeField(auto_now=True)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	justificacion = models.CharField(max_length=200, null=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return unicode(self.estatus)

class DescuentoSalida(models.Model):
	salida = models.ForeignKey(Salida, null=True)
	inventarioRemisionDetalle = models.ForeignKey(InventarioRemisionDetalle, null=True)
	pesoSalida = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	pesoRemision = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	resta = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'), null=True)
	ESTATUSSALIDA = (
	    (0, 'Pendiente'),
	    (1, 'Guardado'),
	)
	estatusSalida = models.IntegerField(choices=ESTATUSSALIDA, default=0)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaActualizacion = models.DateTimeField(auto_now=True)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return unicode(self.estatus)