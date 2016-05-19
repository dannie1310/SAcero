from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from decimal import Decimal
import datetime

# Create your models here.
class Modulo(models.Model):
	nombre = models.CharField(max_length=100)
	padre = models.IntegerField(default=0)
	url = models.CharField(max_length=100)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaActualizacion = models.DateTimeField(auto_now=True)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return self.nombre

class Grupo(models.Model):
	nombre = models.CharField(max_length=100)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaActualizacion = models.DateTimeField(auto_now=True)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return self.nombre

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
	tipo = models.CharField(max_length=10)
	peso = models.FloatField(default=0)
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

class Taller(models.Model):
	nombre = models.CharField(max_length=100)
	responsable = models.CharField(max_length=100, default=0)
	proveedor = models.CharField(default=0, max_length=20)
	ubicacion = models.CharField(max_length=100)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return self.nombre

class Funcion(models.Model):
	TIPOFUNCION = (
	    (1, 'Suministrador'),
	    (2, 'Habilitador'),
	    (3, 'Armador'),
	    (4, 'Colocador'),
	)
	tipo = models.IntegerField(choices=TIPOFUNCION, default=1)
	proveedor = models.CharField(default=0, max_length=20)
	tonelajeMaximo = models.FloatField(default=0)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return self.proveedor

class Frente(models.Model):
	nombre = models.CharField(max_length=100)
	identificacion = models.CharField(max_length=100)
	ubicacion = models.CharField(max_length=100)
	kilometros = models.FloatField(default=0)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
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
	fechaActualizacion = models.DateTimeField(auto_now=True)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return self.numero

class ProgramaSuministro(models.Model):
	idOrden = models.IntegerField()
	remision = models.IntegerField(null=True)
	funcion = models.ForeignKey(Funcion, null=True)
	pesoTara = models.DecimalField(max_digits=20,decimal_places=3,default=Decimal('0.000'), null=True)
	pesoBruto = models.DecimalField(max_digits=20,decimal_places=3,default=Decimal('0.000'), null=True)
	pesoNeto = models.DecimalField(max_digits=20,decimal_places=3,default=Decimal('0.000'), null=True)
	frente = models.ForeignKey(Frente)
	fechaInicial = models.DateField()
	fechaFinal = models.DateField()
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaActualizacion = models.DateTimeField(auto_now=True)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return self.idOrden

class ProgramaSuministroDetalle(models.Model):
	programaSuministro = models.ForeignKey(ProgramaSuministro, null=True)
	material = models.ForeignKey(Material, null=True)
	peso = models.DecimalField(max_digits=20,decimal_places=3,default=Decimal('0.000'), null=True)
	cantidad = models.DecimalField(max_digits=20,decimal_places=3,default=Decimal('0.000'), null=True)
	apoyo = models.ForeignKey(Apoyo)
	elemento = models.ForeignKey(Elemento)
	longitud = models.IntegerField(null=True)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaActualizacion = models.DateTimeField(auto_now=True)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return self.programaSuministro

class ControlAsignacion(models.Model):
	cantidad = models.DecimalField(max_digits=20,decimal_places=4,default=Decimal('0.0000'), null=True)
	tiempoEntrega = models.IntegerField()
	idOrden = models.IntegerField(null=True, blank=True)
	funcion = models.ForeignKey(Funcion)
	frente = models.ForeignKey(Frente)
	programaSuministro = models.ForeignKey(ProgramaSuministro, null=True)
	programaSuministroDetalle = models.ForeignKey(ProgramaSuministroDetalle, null=True)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return self.idOrden

class EtapaAsignacion(models.Model):
	peso = models.DecimalField(max_digits=20,decimal_places=3,default=Decimal('0.000'), null=True)
	cantidad = models.DecimalField(max_digits=20,decimal_places=3,default=Decimal('0.000'), null=True)
	tiempoEntrega = models.IntegerField(null=True)
	programaSuministro = models.ForeignKey(ProgramaSuministro, null=True)
	programaSuministroDetalle = models.ForeignKey(ProgramaSuministroDetalle, null=True)
	funcion = models.ForeignKey(Funcion)
	taller = models.ForeignKey(Taller, null=True)
	transporte = models.ForeignKey(Transporte, null=True)
	cantidadAsignada = models.DecimalField(max_digits=20,decimal_places=3,default=Decimal('0.000'), null=True)
	idEtapaPertenece = models.IntegerField(null=True)
	despiece = models.ForeignKey(Despiece, null=True)
	estatusEtapa = models.IntegerField()
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
	fechaActualizacion = models.DateTimeField(auto_now=True)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return unicode(self.estatus)

class Archivo(models.Model):
	archivo = models.BinaryField()
	etapaAsignacion = models.ForeignKey(EtapaAsignacion, null=True)
	ESTATUSTABLE = (
	    (0, 'Inactivo'),
	    (1, 'Activo'),
	)
	estatus = models.IntegerField(choices=ESTATUSTABLE, default=1)
	TIPOARCHIVO = (
	    (0, 'Certificado'),
	    (1, 'Remision'),
	)
	tipo = models.IntegerField(choices=TIPOARCHIVO, default=1)
	tipoArchivo = models.CharField(max_length=50, null=True)
	nombreArchivo = models.CharField(max_length=100, null=True)
	extension = models.CharField(max_length=8, null=True)
	fechaActualizacion = models.DateTimeField(auto_now=True)
	fechaRegistro = models.DateTimeField(auto_now_add=True)
	def __str__(self):              # __unicode__ on Python 2 REGRESA EL NOMBRE DE LA DESCRIPCION EN EL LISTADO DE ADMINISTRACION
		return unicode(self.estatus)