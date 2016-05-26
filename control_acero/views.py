# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from control_acero.report.models_auth import Empresa, Usuario
from .models import Apoyo, Elemento, Despiece, Material, Frente, Funcion, ControlAsignacion, ProgramaSuministro, ProgramaSuministroDetalle, Etapa, EtapaDescuento,  EtapaDespiece, EtapaDespieceDetalle, Taller, Transporte, Archivo
from django.utils import timezone
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages
from django.db.models import Count, Sum
import json
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import md5
from django.contrib import messages
from django.db import connections
from .forms import ApoyoForm, ElementoForm, DespieceForm, MaterialForm, FrenteForm, FuncionForm, TallerForm, TransporteForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from django.db import connection
from datetime import datetime
from base64 import b64encode
import os
from django.utils.crypto import get_random_string
from decimal import *
from django.conf import settings

class IndexView(generic.ListView):
	template_name = 'control_acero/login.html'
	context_object_name = 'ultimos_cinco_productos'
	def get_queryset(self):
		return Material.objects.order_by('despiece')[:9]
	#latest_question_list = Producto.objects.order_by('-fechaRegistro')[:5]
	#context = {'latest_question_list': latest_question_list}
	#return render(request, 'control_acero/index.html', context)

def principalView(request):
	template = 'control_acero/principal.html'
	return render(request, template)

def frenteTrabajoView(request):
	template = 'control_acero/frente_trabajo/frente_trabajo.html'
	return render(request, template)

def frenteTrabajoNuevoView(request):
	template = 'control_acero/frente_trabajo/frente_trabajo_nuevo.html'
	return render(request, template)

def frenteTrabajoShow(request):
	array = {}
	data = []
	mensaje = {"estatus":"ok", "mensaje":"Correcto"}
	idFrente = request.POST.get('idFrente', 0)
	frente = Frente.objects.filter(id=idFrente)
	for f in frente:
		resultado = {"idFrente":f.id,"nombreFrente":f.nombre,"identificacion":f.identificacion,"ubicacion":f.ubicacion,"kilometros":f.kilometros}
		data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def apoyoCombofiltrado(request):
	array = {}
	mensaje = {}
	data = []
	apoyo = Apoyo.objects.filter(estatus=1)
	for a in apoyo:
			resultado = {"idApoyo":a.id,
							"numero":a.numero}
			data.append(resultado)

	array = mensaje
	array["data"]=data
	return JsonResponse(array)


def movimientosShow(request): #pendiente....
	array = {}
	data = []
	mensaje = {"estatus":"ok", "mensaje":"Correcto"}

	idFrente = request.POST.get('idFrente', 0)
	frente = Frente.objects.filter(id=idFrente)
	elementos = ControlAsignacion.objects.values('id',
												'etapa__pesoSolicitado',
												'etapa__pesoRecibido',
												
												'programaSuministroDetalle__apoyo__numero',
												'programaSuministroDetalle__elemento__nombre',
												'funcion__id',
												'funcion__proveedor',
												'estatusEtapa',
												'programaSuministro__id')
	#.filter(frente=frente_id)

	for e in elementos:
		resultado = {"id":e["id"],
						"pesoSolicitado":e["etapa__pesoSolicitado"],
						"pesoRecibido":e["etapa__pesoRecibido"],
						"apoyo":e["programaSuministroDetalle__apoyo__numero"],
						"elemento":e["programaSuministroDetalle__elemento__nombre"],
						"funcion":e["funcion__id"],
						"funcionProveedor":e["funcion__proveedor"],
						"estatusEtapa":e["estatusEtapa"],
						"programaId":e["programaSuministro__id"]}
		print (resultado)
		data.append(resultado)
	array = mensaje
	array["data"]=data
	
	return JsonResponse(array)

def asignacionComboOrden(request):
	array = {}
	mensaje = {}
	data = []
	ordenControl = ProgramaSuministro.objects.all().values_list('idOrden', flat=True).distinct()
	for o in ordenControl:
		resultado = {"idOrden":o}
		data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def asignacionComboFrente(request):
	array = {}
	mensaje = {}
	data = []
	idOrden = request.POST.get('orden', 0)
	frenteControl = ProgramaSuministro.objects.filter(idOrden=idOrden).values_list('frente_id', flat=True).distinct()
	for fc in frenteControl:
		frente = Frente.objects.filter(id=fc)
		for f in frente:
			resultado = {"idFrente":f.id, "nombre":f.nombre}
			data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def asignacionComboPrograma(request):
	array = {}
	mensaje = {}
	data = []
	idOrden = request.POST.get('orden', 0)
	idFrente = request.POST.get('frente', 0)
	programa = ProgramaSuministro.objects.filter(idOrden=idOrden,frente_id=idFrente).values_list('id', flat=True).distinct()
	for p in programa:
		resultado = {"idPrograma":p}
		data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def asignacionComboElementos(request):
	array = {}
	mensaje = {}
	data = []
	idPrograma = request.POST.get('programa', 1)
	elementoDistinct = ProgramaSuministroDetalle.objects.filter(programaSuministro_id=idPrograma).values_list('elemento_id', flat=True).distinct()
	for ed in elementoDistinct:
		peso = ProgramaSuministroDetalle.objects.filter(programaSuministro_id=idPrograma,
														elemento_id=ed).aggregate(Sum('peso'))
		elementos = Elemento.objects.values('id',
											'nombre').filter(id=ed)
		for e in elementos:
			resultado = {"id":e["id"],
							"elementoNombre":e["nombre"],
							"total": peso["peso__sum"]}
			data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def suministroAsignaComboPrograma(request):
	array = {}
	mensaje = {}
	data = []
	programaSuministro = ControlAsignacion.objects.all().values_list('programaSuministro_id', flat=True).distinct()
	for p in programaSuministro:
		resultado = {"idPrograma":p}
		data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def suministroAsignaComboFuncion(request):
	array = {}
	mensaje = {}
	data = []
	controlFuncion = ControlAsignacion.objects.all().values_list('funcion_id', flat=True).distinct()
	for cf in controlFuncion:
		funcion = Funcion.objects.filter(id=cf)
		for f in funcion:
			resultado = {"idFuncion":f.id, "proveedor":f.proveedor}
			data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def suministroAsignaElementos(request):
	array = {}
	mensaje = {}
	data = []
	idPrograma = request.POST.get('programa', 0)
	idFuncion = request.POST.get('funcion', 0)
	elementos = ControlAsignacion.objects.values('id','cantidad', 'tiempoEntrega', 'frente__id', 'frente__nombre', 'funcion__id', 'funcion__proveedor', 'programaSuministro__id', 'programaSuministroDetalle__id').filter(programaSuministro_id=idPrograma, funcion_id=idFuncion)
	for e in elementos:
		resultado = {"id":e["id"],"cantidad":e["cantidad"],"tiempoEntrega":e["tiempoEntrega"],"frenteId":e["frente__id"],"frenteNombre":e["frente__nombre"],"funcionId":e["funcion__id"],"funcionProveedor":e["funcion__proveedor"],"suministroId":e["programaSuministro__id"],"suministroDetalleId":e["programaSuministroDetalle__id"]}
		data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def suministroAsignarComboPrograma(request):
	array = {}
	mensaje = {}
	data = []
	programaSuministro = ProgramaSuministro.objects.all().values_list('id', flat=True).distinct()
	for p in programaSuministro:
		resultado = {"idPrograma":p}
		data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def suministroAsignarComboFuncion(request):
	array = {}
	mensaje = {}
	data = []
	controlFuncion = ProgramaSuministro.objects.all().values_list('funcion_id', flat=True).distinct()
	for cf in controlFuncion:
		funcion = Funcion.objects.filter(id=cf)
		for f in funcion:
			resultado = {"idFuncion":f.id, "proveedor":f.proveedor}
			data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def suministroAsignarComboTaller(request):
	array = {}
	mensaje = {}
	data = []
	taller = Taller.objects.filter(estatus=1)
	for t in taller:
		resultado = {"idTaller":t.id, "nombre":t.nombre, "proveedor":t.proveedor}
		data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def suministroAsignarComboTransporte(request):
	array = {}
	mensaje = {}
	data = []
	transporte = Transporte.objects.filter(estatus=1)
	for t in transporte:
		resultado = {"idTransporte":t.id, "capacidad":t.capacidad, "placas":t.placas}
		data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def suministroAsignarcomboFuncionElegido(request):
	array = {}
	mensaje = {}
	data = []
	tipo = request.POST.get('tipo', 0)
	funcion = Funcion.objects.filter(tipo=tipo, estatus=1)
	for f in funcion:
		resultado = {"idFuncion":f.id, "proveedor":f.proveedor}
		data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def suministroAsignarCantidades(request):
	array = {}
	mensaje = {}
	data = []
	dataDetalle = []
	idFuncion = request.POST.get('funcion', 1)
	ps = ProgramaSuministroDetalle.objects\
									.values('material_id',
											'material__nombre')\
									.filter(programaSuministro__funcion__id=idFuncion) \
									.annotate(pesoMaterial = Sum('peso')) \
									.annotate(cantidadMaterial = Sum('cantidad')) \
									.order_by('material_id')

	psd = ProgramaSuministroDetalle.objects\
									.values('id',
											'material__id',
											'material__nombre',
											'peso')\
									.filter(programaSuministro__funcion__id=idFuncion)\
									.order_by('id')
	for p in ps:
		resultado = {"id":p["material_id"],
						"materialNombre":p["material__nombre"],
						"peso":p["pesoMaterial"],
						"cantidad":p["cantidadMaterial"]
					}
		data.append(resultado)


	for ps in psd:
		resultado = {"idDetalle":ps["id"],
						"idMaterial":ps["material__id"],
						"materialNombre":ps["material__nombre"],
						"peso":ps["peso"]
					}
		dataDetalle.append(resultado)

	array["data"]=data
	array["dataDetalle"]=dataDetalle
	return JsonResponse(array)

def extensiones(extension):
	ext = "";
	if(extension == ".jpg"):
		ext = "image/jpeg"
	if(extension == ".png"):
		ext = "image/png"
	if(extension == ".pdf"):
		ext = "application/pdf"
	return ext

def habilitadoAsignaComboPrograma(request):
	array = {}
	mensaje = {}
	data = []
	etapa = Etapa.objects.filter(estatusEtapa=1).values_list('programaSuministro_id', flat=True).distinct()
	for p in etapa:
		resultado = {"idPrograma":p}
		data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def habilitadoAsignaComboFuncion(request):
	array = {}
	mensaje = {}
	data = []
	etapaFuncion = Etapa.objects.filter(estatusEtapa=1).values_list('funcion_id', flat=True).distinct()
	for e in etapaFuncion:
		funcion = Funcion.objects.filter(id=e)
		for f in funcion:
			resultado = {"idFuncion":f.id, "proveedor":f.proveedor}
			data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def habilitadoRecepcionHabilitado(request):
	array = {}
	mensaje = {}
	data = []
	idPrograma = request.POST.get('programa', 0)
	idFuncion = request.POST.get('funcion', 0)
	etapa = Etapa.objects.values('id',
											'programaSuministroDetalle__material__nombre',
											'peso',
											'cantidad',
											'cantidadAsignada',
											'taller__id',
											'taller__nombre',
											'transporte__id',
											'transporte__placas',
											'programaSuministro_id')\
									.filter(
											funcion_id=idFuncion,
											estatusEtapa=1)
	for e in etapa:
		resultado = {"id":e["id"],
						"nombreMaterial":e["programaSuministroDetalle__material__nombre"],
						"peso":e["peso"],
						"cantidad":e["cantidad"],
						"cantidadAsignada":e["cantidadAsignada"],
						"tallerId":e["taller__id"],
						"tallerNombre":e["taller__nombre"],
						"transporteId":e["transporte__id"],
						"transportePlacas":e["transporte__placas"],
						"programaSuministro":e["programaSuministro_id"]
					}
		data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def habilitadoAsignarComboPrograma(request):
	array = {}
	mensaje = {}
	data = []
	etapa = Etapa.objects.filter(estatusEtapa=2)\
												.values_list('programaSuministro_id', flat=True)\
												.distinct()
	for p in etapa:
		resultado = {"idPrograma":p}
		data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def habilitadoAsignarComboFuncion(request):
	array = {}
	mensaje = {}
	data = []
	etapaFuncion = Etapa.objects.filter(estatusEtapa=2)\
											.values_list('funcion_id', flat=True)\
											.distinct()
	for e in etapaFuncion:
		funcion = Funcion.objects.filter(id=e)
		for f in funcion:
			resultado = {"idFuncion":f.id, "proveedor":f.proveedor}
			data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def habilitadoAsignarCantidades(request):
	array = {}
	mensaje = {}
	data = []
	idPrograma = request.POST.get('programa', 0)
	idFuncion = request.POST.get('funcion', 0)
	suministro = Etapa.objects.values('id', 'pesoSolicitado', 'pesoRecibido', 'controlAsignacion_id', 'funcion_id', 'programaSuministro_id').filter(programaSuministro_id=idPrograma, funcion_id=idFuncion, estatusEtapa=3)
	for s in suministro:
		resultado = {"id":s["id"],"pesoSolicitado":s["pesoSolicitado"],"pesoRecibido":s["pesoRecibido"],"idAsignacion":s["controlAsignacion_id"],"idFuncion":s["funcion_id"],"idPrograma":s["programaSuministro_id"]}
		data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def habilitadoAsignarComboElemento(request):
	idPrograma = request.POST.get('programa', 0)
	idFuncion = request.POST.get('funcion', 0)
	array = {}
	mensaje = {}
	data = []
	elemento = Elemento.objects.filter(estatus=1)
	for e in elemento:
		resultado = {"idElemento":e.id, "nombre":e.nombre}
		data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def habilitadoAsignarElemento(request):
	array = {}
	mensaje = {}
	data = []
	dataTotales = []
	dataEtapa = []
	programa = request.POST.get('programa', 1)
	funcion = request.POST.get('funcion', 5)
	elemento = request.POST.get('elemento', 2)
	cantidad = request.POST.get('cantidad', 1)
	pesoRecibido = 0;
	pesoAsignado = 0;
	etapaRegistro = 0;
	elementoRelacion = Elemento.objects.values("id",
												"nombre",
												"despiece__id",
												"despiece__nomenclatura",
												"despiece__figura",
												"despiece__longitud",
												"despiece__cantidad",
												"despiece__peso",
												"despiece__material__id",
												"despiece__material__nombre"
												)\
										.filter(id=elemento,
												estatus=1)\
										.order_by("despiece__material__id");
	for e in elementoRelacion:
		despiecePeso = Decimal(e["despiece__peso"])*Decimal(cantidad);
		resultadoDespiece = {"id":e["id"], 
						"nombre":e["nombre"],
						"despieceId":e["despiece__id"],
						"despieceNomenclatura":e["despiece__nomenclatura"],
						"despieceFigura":e["despiece__figura"],
						"despieceLongitud":e["despiece__longitud"],
						"despieceCantidad":e["despiece__cantidad"],
						"despiecePeso":despiecePeso,
						"materialId":e["despiece__material__id"],
						"materialNombre":e["despiece__material__nombre"]
					}
		data.append(resultadoDespiece)
	elementoTotales = Elemento.objects.values("despiece__material__id",
												"despiece__material__nombre"
												)\
										.annotate(despiecePeso = Sum('despiece__peso')) \
										.filter(id=elemento,
												estatus=1)\
										.order_by("despiece__material__id");
	etapa = Etapa.objects.values("id",
									"cantidadAsignada",
									"programaSuministroDetalle__material_id",
									"programaSuministroDetalle__material__nombre"
									)\
							.filter(
									funcion_id=funcion,
									estatusEtapa=2,
									estatus=1)
	for et in elementoTotales:
		despiecePeso = Decimal(et["despiecePeso"])*Decimal(cantidad);
		for etp in etapa:
			if et["despiece__material__id"] == etp["programaSuministroDetalle__material_id"]:
				etapaRegistro = etp["id"]
				pesoRecibido = etp["cantidadAsignada"];
				pesoAsignado =  etp["cantidadAsignada"] - despiecePeso
		resultadoTotales = {"idEtapa":etapaRegistro, 
						"idMaterial":et["despiece__material__id"], 
						"nombre":et["despiece__material__nombre"],
						"despiecePeso":despiecePeso,
						"pesoRecibido":pesoRecibido,
						"pesoAsignado":pesoAsignado
					}
		dataTotales.append(resultadoTotales)

	array = mensaje
	array["data"]=data
	array["dataTotales"]=dataTotales
	return JsonResponse(array)

def armadoAsignarComboPrograma(request):
	array = {}
	mensaje = {}
	data = []
	etapa = Etapa.objects.filter(estatusEtapa=3)\
							.values_list('programaSuministro_id', flat=True)\
							.distinct()
	for p in etapa:
		resultado = {"idPrograma":p}
		data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def armadoAsignarComboFuncion(request):
	array = {}
	mensaje = {}
	data = []
	etapaFuncion = Etapa.objects.filter(estatusEtapa=3)\
								.values_list('funcion_id', flat=True)\
								.distinct()
	for e in etapaFuncion:
		funcion = Funcion.objects.filter(id=e)
		for f in funcion:
			resultado = {"idFuncion":f.id, "proveedor":f.proveedor}
			data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def armadoAsignarComboElemento(request):
	array = {}
	mensaje = {}
	data = []
	programa = request.POST.get('programa', 0)
	funcion = request.POST.get('funcion', 0)
	etapa = Etapa.objects.filter(estatusEtapa=3,
									funcion_id=funcion,
									programaSuministro_id=programa)\
						.values_list('EtapaDespiece__elemento__id', flat=True)\
						.distinct()
	for e in etapa:
		elemento = Elemento.objects.filter(id=e)
		for e in elemento:
			resultado = {"idElemento":e.id, "nombre":e.nombre}
			data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def armadoAsignarElemento(request):
	array = {}
	mensaje = {}
	data = []
	dataEtapaDetalle = []
	programa = request.POST.get('programa', 1)
	funcion = request.POST.get('funcion', 17)
	elemento = request.POST.get('elemento', 2)
	etapa = Etapa.objects.values("id",
									"EtapaDespiece__id",
									"EtapaDespiece__despieceTotal",
									"EtapaDespiece__pesoRecibido",
									"EtapaDespiece__material__id",
									"EtapaDespiece__material__nombre",
									"EtapaDespiece__material__imagen")\
							.filter(estatusEtapa=3,
									funcion_id=funcion,
									programaSuministro_id=programa,
									EtapaDespiece__elemento__id=elemento)

	etapaDespieceDetalle = Etapa.objects.values("id",
													"EtapaDespiece__id",
													"EtapaDespiece__EtapaDespieceDetalle__id",
													"EtapaDespiece__despieceTotal",
													"EtapaDespiece__pesoRecibido",
													"EtapaDespiece__EtapaDespieceDetalle__despiece_id",
													"EtapaDespiece__EtapaDespieceDetalle__despiece__nomenclatura",
													"EtapaDespiece__EtapaDespieceDetalle__despiecePeso",
													"EtapaDespiece__EtapaDespieceDetalle__despiece__material__id",
													"EtapaDespiece__EtapaDespieceDetalle__despiece__material__nombre")\
							.filter(estatusEtapa=3,
									funcion_id=funcion,
									programaSuministro_id=programa,
									EtapaDespiece__elemento__id=elemento)
	for e in etapa:
		resultado = {"id":e["id"],
						"idDespiece":e["EtapaDespiece__id"],
						"despieceTotal":e["EtapaDespiece__despieceTotal"],
						"despieceRecibido":e["EtapaDespiece__pesoRecibido"],
						"idMaterial":e["EtapaDespiece__material__id"],
						"materialNombre":e["EtapaDespiece__material__nombre"],
						"materialImagen":e["EtapaDespiece__material__imagen"]
						}
		data.append(resultado)

	for edd in etapaDespieceDetalle:
		resultado = {"id":edd["id"],
						"idDespiece":edd["EtapaDespiece__id"],
						"idDespieceDetalle":edd["EtapaDespiece__EtapaDespieceDetalle__id"],
						"despieceTotal":edd["EtapaDespiece__despieceTotal"],
						"despieceRecibido":edd["EtapaDespiece__pesoRecibido"],
						"idDespieceOriginal":edd["EtapaDespiece__EtapaDespieceDetalle__despiece_id"],
						"despieceNomenclatura":edd["EtapaDespiece__EtapaDespieceDetalle__despiece__nomenclatura"],
						"despiecePeso":edd["EtapaDespiece__EtapaDespieceDetalle__despiecePeso"],
						"idMaterial":edd["EtapaDespiece__EtapaDespieceDetalle__despiece__material__id"],
						"materialNombre":edd["EtapaDespiece__EtapaDespieceDetalle__despiece__material__nombre"]
						}
		dataEtapaDetalle.append(resultado)
	array = mensaje
	array["data"]=data
	array["dataEtapaDetalle"]=dataEtapaDetalle
	return JsonResponse(array)

def armadoAsignacionComboPrograma(request):
	array = {}
	mensaje = {}
	data = []
	etapa = Etapa.objects.filter(estatusEtapa=4).values_list('programaSuministro_id', flat=True).distinct()
	for p in etapa:
		resultado = {"idPrograma":p}
		data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def armadoAsignacionComboFuncion(request):
	array = {}
	mensaje = {}
	data = []
	etapaFuncion = Etapa.objects.filter(estatusEtapa=4).values_list('funcion_id', flat=True).distinct()
	for e in etapaFuncion:
		funcion = Funcion.objects.filter(id=e)
		for f in funcion:
			resultado = {"idFuncion":f.id, "proveedor":f.proveedor}
			data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def armadoAsignacionComboElemento(request):
	idPrograma = request.POST.get('programa', 0)
	idFuncion = request.POST.get('funcion', 0)
	array = {}
	mensaje = {}
	data = []
	etapa = Etapa.objects.filter(estatusEtapa=4,
									funcion_id=idFuncion,
									programaSuministro_id=idPrograma).values_list('EtapaDespiece__elemento__id', flat=True).distinct()
	print etapa.query
	for e in etapa:
		elemento = Elemento.objects.filter(id=e)
		for e in elemento:
			resultado = {"idElemento":e.id, "nombre":e.nombre}
			data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def armadoAsignacionElemento(request):
	array = {}
	mensaje = {}
	data = []
	dataEtapaDetalle = []
	programa = request.POST.get('programa', 1)
	funcion = request.POST.get('funcion', 17)
	elemento = request.POST.get('elemento', 2)
	etapa = Etapa.objects.values("id",
									"EtapaDespiece__id",
									"EtapaDespiece__despieceTotal",
									"EtapaDespiece__pesoRecibido",
									"EtapaDespiece__material__id",
									"EtapaDespiece__material__nombre",
									"EtapaDespiece__material__imagen")\
							.filter(estatusEtapa=4,
									funcion_id=funcion,
									programaSuministro_id=programa,
									EtapaDespiece__elemento__id=elemento)

	etapaDespieceDetalle = Etapa.objects.values("id",
													"EtapaDespiece__id",
													"EtapaDespiece__EtapaDespieceDetalle__id",
													"EtapaDespiece__despieceTotal",
													"EtapaDespiece__pesoRecibido",
													"EtapaDespiece__EtapaDespieceDetalle__despiece_id",
													"EtapaDespiece__EtapaDespieceDetalle__despiece__nomenclatura",
													"EtapaDespiece__EtapaDespieceDetalle__despiecePeso",
													"EtapaDespiece__EtapaDespieceDetalle__despiece__material__id",
													"EtapaDespiece__EtapaDespieceDetalle__despiece__material__nombre")\
							.filter(estatusEtapa=4,
									funcion_id=funcion,
									programaSuministro_id=programa,
									EtapaDespiece__elemento__id=elemento)
	for e in etapa:
		resultado = {"id":e["id"],
						"idDespiece":e["EtapaDespiece__id"],
						"despieceTotal":e["EtapaDespiece__despieceTotal"],
						"despieceRecibido":e["EtapaDespiece__pesoRecibido"],
						"idMaterial":e["EtapaDespiece__material__id"],
						"materialNombre":e["EtapaDespiece__material__nombre"],
						"materialImagen":e["EtapaDespiece__material__imagen"]
						}
		data.append(resultado)

	for edd in etapaDespieceDetalle:
		resultado = {"id":edd["id"],
						"idDespiece":edd["EtapaDespiece__id"],
						"idDespieceDetalle":edd["EtapaDespiece__EtapaDespieceDetalle__id"],
						"despieceTotal":edd["EtapaDespiece__despieceTotal"],
						"despieceRecibido":edd["EtapaDespiece__pesoRecibido"],
						"idDespieceOriginal":edd["EtapaDespiece__EtapaDespieceDetalle__despiece_id"],
						"despieceNomenclatura":edd["EtapaDespiece__EtapaDespieceDetalle__despiece__nomenclatura"],
						"despiecePeso":edd["EtapaDespiece__EtapaDespieceDetalle__despiecePeso"],
						"idMaterial":edd["EtapaDespiece__EtapaDespieceDetalle__despiece__material__id"],
						"materialNombre":edd["EtapaDespiece__EtapaDespieceDetalle__despiece__material__nombre"]
						}
		dataEtapaDetalle.append(resultado)
	array = mensaje
	array["data"]=data
	array["dataEtapaDetalle"]=dataEtapaDetalle
	return JsonResponse(array)

def colocadoRecepcionComboPrograma(request):
	array = {}
	mensaje = {}
	data = []
	etapa = Etapa.objects.filter(estatusEtapa=6).values_list('programaSuministro_id', flat=True).distinct()
	for p in etapa:
		resultado = {"idPrograma":p}
		data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def colocadoRecepcionComboFuncion(request):
	array = {}
	mensaje = {}
	data = []
	etapaFuncion = Etapa.objects.filter(estatusEtapa=6).values_list('funcion_id', flat=True).distinct()
	for e in etapaFuncion:
		funcion = Funcion.objects.filter(id=e)
		for f in funcion:
			resultado = {"idFuncion":f.id, "proveedor":f.proveedor}
			data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def colocadoRecepcionComboApoyo(request):
	array = {}
	mensaje = {}
	data = []
	idPrograma = request.POST.get('programa', 0)
	idFuncion = request.POST.get('funcion', 0)
	etapa = Etapa.objects.values("controlAsignacion__programaSuministroDetalle__apoyo__id",
											"controlAsignacion__programaSuministroDetalle__apoyo__numero"
											).filter(estatusEtapa=6, funcion_id=idFuncion, programaSuministro_id=idPrograma).values_list('controlAsignacion__programaSuministroDetalle__apoyo__id', flat=True).distinct()
	print etapa
	for e in etapa:
		apoyo = Apoyo.objects.filter(id=e)
		for a in apoyo:
			resultado = {"idApoyo":a.id, "numero":a.numero}
			data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def programaCombofiltrado(request):
	array = {}
	mensaje = {}
	data = []
	programa = ProgramaSuministro.objects.filter(estatus=1)
	for p in programa:
			resultado = {"idPrograma":p.id}
			data.append(resultado)

	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def controlAsignacionView(request):
	template = 'control_acero/control_asignacion/control_asignacion.html'
	return render(request, template)

def controlAsignacionNuevoView(request):
	template = 'control_acero/control_asignacion/control_asignacion.html'
	return render(request, template)

def suministroRecepcionView(request):
	template = 'control_acero/suministro/suministro_recepcion.html'
	return render(request, template)

def suministroAsignacionView(request):
	template = 'control_acero/suministro/suministro_asignacion.html'
	return render(request, template)

def habilitadoRecepcionView(request):
	template = 'control_acero/habilitado/habilitado_recepcion.html'
	return render(request, template)

def habilitadoAsignacionView(request):
	template = 'control_acero/habilitado/habilitado_asignacion.html'
	return render(request, template)

def habilitadoCambioTallerView(request):
	template = 'control_acero/habilitado/habilitado_cambio_taller.html'
	return render(request, template)

def armadoRecepcionView(request):
	template = 'control_acero/armado/armado_recepcion.html'
	return render(request, template)

def armadoAsignacionView(request):
	template = 'control_acero/armado/armado_asignacion.html'
	return render(request, template)

def colocadoRecepcionView(request):
	template = 'control_acero/colocado/colocado_recepcion.html'
	return render(request, template)

def movimientosView(request):
	template = 'control_acero/inventario/movimientos.html'
	return render(request, template)

def fisicoView(request):
	template = 'control_acero/inventario/fisico.html'
	return render(request, template)

class AccesoView(generic.ListView):
	template_name = 'control_acero/acceso.html'
	context_object_name = 'permisos_a_bd'
	def get_queryset(self):
		return Material.objects.order_by('despiece')[:9]
		#cursor = connections['modulos_db'].cursor()
		#cursor.execute("SELECT [IDBaseDatos],[Nombre],[Mascara],[Servidor],[IDTipoSistemaOrigen],[IDTipoBaseDatos],[EstaActiva],[FechaHoraRegistro] FROM [BasesDatos].[BasesDatos] WHERE EstaActiva = 1")
		#row = cursor.fetchall()
		#return row
	#latest_question_list = Producto.objects.order_by('-fechaRegistro')[:5]
	#context = {'latest_question_list': latest_question_list}
	#return render(request, 'control_acero/index.html', context)

class RecepcionView(generic.ListView):
	template_name = 'control_acero/recepcion.html'
	context_object_name = 'permisos_a_bd'
	def get_queryset(self):
		return Material.objects.order_by('despiece')[:9]
		#cursor = connections['modulos_db'].cursor()
		#cursor.execute("SELECT [IDBaseDatos],[Nombre],[Mascara],[Servidor],[IDTipoSistemaOrigen],[IDTipoBaseDatos],[EstaActiva],[FechaHoraRegistro] FROM [BasesDatos].[BasesDatos] WHERE EstaActiva = 1")
		#row = cursor.fetchall()
		#return row
	#latest_question_list = Producto.objects.order_by('-fechaRegistro')[:5]
	#context = {'latest_question_list': latest_question_list}
	#return render(request, 'control_acero/index.html', context)

#class SuministroView(generic.ListView):
	#template_name = 'control_acero/suministro.html'
	#context_object_name = 'permisos_a_bd'
	#def get_queryset(self):
		#return Material.objects.order_by('despiece')[:9]
		#cursor = connections['modulos_db'].cursor()
		#cursor.execute("SELECT [IDBaseDatos],[Nombre],[Mascara],[Servidor],[IDTipoSistemaOrigen],[IDTipoBaseDatos],[EstaActiva],[FechaHoraRegistro] FROM [BasesDatos].[BasesDatos] WHERE EstaActiva = 1")
		#row = cursor.fetchall()
		#return row
	#latest_question_list = Producto.objects.order_by('-fechaRegistro')[:5]
	#context = {'latest_question_list': latest_question_list}
	#return render(request, 'control_acero/index.html', context)

class ControlView(generic.ListView):
	template_name = 'control_acero/control.html'
	context_object_name = 'permisos_a_bd'
	def get_queryset(self):
		return Material.objects.order_by('despiece')[:9]
		#cursor = connections['modulos_db'].cursor()
		#cursor.execute("SELECT [IDBaseDatos],[Nombre],[Mascara],[Servidor],[IDTipoSistemaOrigen],[IDTipoBaseDatos],[EstaActiva],[FechaHoraRegistro] FROM [BasesDatos].[BasesDatos] WHERE EstaActiva = 1")
		#row = cursor.fetchall()
		#return row
	#latest_question_list = Producto.objects.order_by('-fechaRegistro')[:5]
	#context = {'latest_question_list': latest_question_list}
	#return render(request, 'control_acero/index.html', context)

class FrenteView(generic.ListView):
	template_name = 'control_acero/frente.html'
	context_object_name = 'permisos_a_bd'
	def get_queryset(self):
		return Material.objects.order_by('despiece')[:9]
		#cursor = connections['modulos_db'].cursor()
		#cursor.execute("SELECT [IDBaseDatos],[Nombre],[Mascara],[Servidor],[IDTipoSistemaOrigen],[IDTipoBaseDatos],[EstaActiva],[FechaHoraRegistro] FROM [BasesDatos].[BasesDatos] WHERE EstaActiva = 1")
		#row = cursor.fetchall()
		#return row
	#latest_question_list = Producto.objects.order_by('-fechaRegistro')[:5]
	#context = {'latest_question_list': latest_question_list}
	#return render(request, 'control_acero/index.html', context)

#class HabilitadoView(generic.ListView):
	#template_name = 'control_acero/habilitado.html'
	#context_object_name = 'permisos_a_bd'
	#def get_queryset(self):
		#return Material.objects.order_by('despiece')[:9]
		#cursor = connections['modulos_db'].cursor()
		#cursor.execute("SELECT [IDBaseDatos],[Nombre],[Mascara],[Servidor],[IDTipoSistemaOrigen],[IDTipoBaseDatos],[EstaActiva],[FechaHoraRegistro] FROM [BasesDatos].[BasesDatos] WHERE EstaActiva = 1")
		#row = cursor.fetchall()
		#return row
	#latest_question_list = Producto.objects.order_by('-fechaRegistro')[:5]
	#context = {'latest_question_list': latest_question_list}
	#return render(request, 'control_acero/index.html', context)

class ArmadoView(generic.ListView):
	template_name = 'control_acero/armado.html'
	context_object_name = 'permisos_a_bd'
	def get_queryset(self):
		return Material.objects.order_by('despiece')[:9]
		#cursor = connections['modulos_db'].cursor()
		#cursor.execute("SELECT [IDBaseDatos],[Nombre],[Mascara],[Servidor],[IDTipoSistemaOrigen],[IDTipoBaseDatos],[EstaActiva],[FechaHoraRegistro] FROM [BasesDatos].[BasesDatos] WHERE EstaActiva = 1")
		#row = cursor.fetchall()
		#return row
	#latest_question_list = Producto.objects.order_by('-fechaRegistro')[:5]
	#context = {'latest_question_list': latest_question_list}
	#return render(request, 'control_acero/index.html', context)

class ColocadoView(generic.ListView):
	template_name = 'control_acero/colocado.html'
	context_object_name = 'permisos_a_bd'
	def get_queryset(self):
		return Material.objects.order_by('despiece')[:9]
		#cursor = connections['modulos_db'].cursor()
		#cursor.execute("SELECT [IDBaseDatos],[Nombre],[Mascara],[Servidor],[IDTipoSistemaOrigen],[IDTipoBaseDatos],[EstaActiva],[FechaHoraRegistro] FROM [BasesDatos].[BasesDatos] WHERE EstaActiva = 1")
		#row = cursor.fetchall()
		#return row
	#latest_question_list = Producto.objects.order_by('-fechaRegistro')[:5]
	#context = {'latest_question_list': latest_question_list}
	#return render(request, 'control_acero/index.html', context)

class HomeView(generic.ListView):
	template_name = 'control_acero/home.html'
	context_object_name = 'ultimos_cinco_productos'
	def get_queryset(self):
		return Material.objects.order_by('despiece')[:9]
	#context_object_name = 'ultimos_cinco_productos'
	#producto = get_object_or_404(Producto, pk=producto_id)
	#return render(request, template_name)
def loginUsuario(request):
	usuario = request.POST['usuario']
	clave = request.POST['clave']
	cursor = connections['modulos_db'].cursor()
	if (usuario == ""):
		resultado = {"estatus":"error","mensaje":"El campo usuario esta vacio"}
		return JsonResponse(resultado)
	if (clave == ""):
		resultado = {"estatus":"error","mensaje":"El campo clave esta vacio"}
		return JsonResponse(resultado)
	login = Usuario.objects.using('auth_db').filter(usuario=usuario, clave=md5.new(clave).hexdigest())
	for e in login:
		if(e != ""):
			request.session['idusuario'] = e.idusuario
			request.session['usuario'] = e.usuario
			url = '/control_acero/principal/'
			return HttpResponseRedirect(url)
	template_name = '/control_acero'
	messages.error(request, 'Usuario y/o Password invalidos')
	return HttpResponseRedirect(template_name)

def logout(request):
    try:
        del request.session['idusuario']
        del request.session['usuario']
        del request.session['clave']
    except KeyError:
        pass
    template_name = '/control_acero'
    return HttpResponseRedirect(template_name)

def frenteShow(request):
	array = {}
	arrayFrente = {}
	mensaje = {}
	dataFrente = []
	dataEstructura = []
	dataElemento = []
	dataDespiece = []
	dataMaterial = []
	frente = request.POST['frente']
	estructuraid = request.POST['estructura']
	frente = Frente.objects.filter(id=estructuraid)
	estructura = Estructura.objects.filter(id=estructuraid)
	elemento = Estructura.objects.values('nombre','elemento__id','elemento__nombre','elemento__numero','elemento__diametro', 'elemento__longitudTotal', 'elemento__peso').filter(id=estructuraid)
	mensaje = {"estatus":"ok", "mensaje":"Correcto"}
	for f in frente:
			resultado = {"idFrente":f.id,"nombreFrente":f.nombre,"identificacion":f.identificacion,"ubicacion":f.ubicacion,"kilometros":f.kilometros}
			dataFrente.append(resultado)
	for es in estructura:
			resultado = {"nombreEstructura":es.nombre}
			dataEstructura.append(resultado)
	for e in elemento:
			resultado = {"nombreEstructura":e['nombre'],"nombreElemento":e['elemento__nombre'],"numeroElemento":e['elemento__numero'],"diametroElemento":e['elemento__diametro'],"longitudtotalElemento":e['elemento__longitudTotal'],"pesoElemento":e['elemento__peso']}
			dataElemento.append(resultado)
			despiece = Elemento.objects.values('nombre','despiece__id','despiece__nombre','despiece__pieza','despiece__calibre','despiece__pija','despiece__longitud').filter(id=e['elemento__id'])
			for d in despiece:
				resultado = {"nombreElemento":d["nombre"],"nombreDespiece":d['despiece__nombre'],"piezaDespiece":d['despiece__pieza'],"calibreDespiece":d['despiece__calibre'],"pijaDespiece":d['despiece__pija'],"longitudDespiece":d['despiece__longitud']}
				dataDespiece.append(resultado)
				material = Despiece.objects.values('nombre','material__nombre','material__diametro','material__longitud','material__peso','material__proveedor','material__tipo').filter(id=d['despiece__id'])
				for m in material:
					resultado = {"nombreDespiece":m["nombre"],"nombreMaterial":m['material__nombre'],"diametroMaterial":m['material__diametro'],"longitudMaterial":m['material__longitud'],"pesoMaterial":m['material__peso'],"proveedorMaterial":m['material__proveedor'],"tipoMaterial":m['material__tipo']}
					dataMaterial.append(resultado)

	array = mensaje
	array["frente"]=dataFrente
	array["estructura"]=dataEstructura
	array["elementos"]=dataElemento
	array["despieces"]=dataDespiece
	array["materiales"]=dataMaterial
	return JsonResponse(array)

def frenteShowelemento(request):
	array = {}
	arrayFrente = {}
	mensaje = {}
	dataFrente = []
	dataElemento = []
	dataDespiece = []
	dataMaterial = []
	frente = request.POST['frente']
	elementoid = request.POST['elemento']
	frente = Frente.objects.filter(id=elementoid)
	elemento = Elemento.objects.filter(id=elementoid)
	print elemento
	mensaje = {"estatus":"ok", "mensaje":"Correcto"}
	for f in frente:
	 		resultado = {"idFrente":f.id,"nombreFrente":f.nombre,"identificacion":f.identificacion,"ubicacion":f.ubicacion,"kilometros":f.kilometros}
	 		dataFrente.append(resultado)
	for e in elemento:
	 		resultado = {"nombreElemento":e.nombre,"numeroElemento":e.numero,"diametroElemento":e.diametro,"longitudtotalElemento":e.longitudTotal,"pesoElemento":e.peso}
	 		dataElemento.append(resultado)
	 		despiece = Elemento.objects.values('nombre','despiece__id','despiece__nombre','despiece__pieza','despiece__calibre','despiece__pija','despiece__longitud').filter(id=e.id)
	 		for d in despiece:
	 			resultado = {"nombreElemento":d["nombre"],"nombreDespiece":d['despiece__nombre'],"piezaDespiece":d['despiece__pieza'],"calibreDespiece":d['despiece__calibre'],"pijaDespiece":d['despiece__pija'],"longitudDespiece":d['despiece__longitud']}
	 			dataDespiece.append(resultado)
	 			material = Despiece.objects.values('nombre','material__nombre','material__diametro','material__longitud','material__peso','material__proveedor','material__tipo').filter(id=d['despiece__id'])
	 			for m in material:
	 				resultado = {"nombreDespiece":m["nombre"],"nombreMaterial":m['material__nombre'],"diametroMaterial":m['material__diametro'],"longitudMaterial":m['material__longitud'],"pesoMaterial":m['material__peso'],"proveedorMaterial":m['material__proveedor'],"tipoMaterial":m['material__tipo']}
	 				dataMaterial.append(resultado)

	array = mensaje
	array["frente"]=dataFrente
	array["elementos"]=dataElemento
	array["despieces"]=dataDespiece
	array["materiales"]=dataMaterial
	return JsonResponse(array)

def funcionShow(request):
	array = {}
	mensaje = {}
	data = []
	funcion = Funcion.objects.all()
	for f in funcion:
			resultado = {"idFuncion":f.id,"proveedor":f.proveedor}
			data.append(resultado)

	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def funcionComboFiltrado(request):
	array = {}
	mensaje = {}
	data = []
	funcion = Funcion.objects.filter(tipo=1, estatus=1)
	for f in funcion:
			resultado = {"idFuncion":f.id,"proveedor":f.proveedor}
			data.append(resultado)

	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def frenteCombo(request):
	array = {}
	mensaje = {}
	data = []
	#v = Venta(usuario_id=usuario_id)
	frente = Frente.objects.all()
	for f in frente:
			resultado = {"idFrente":f.id,"nombre":f.nombre}
			data.append(resultado)

	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def frenteCombofiltrado(request):
	array = {}
	mensaje = {}
	data = []
	#v = Venta(usuario_id=usuario_id)
	frente = Frente.objects.filter(estatus=1)
	for f in frente:
			resultado = {"idFrente":f.id,"nombre":f.nombre}
			data.append(resultado)

	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def estructuraCombo(request):
	array = {}
	mensaje = {}
	data = []
	#v = Venta(usuario_id=usuario_id)
	estructura = Estructura.objects.all()
	for e in estructura:
			resultado = {"idEstructura":e.id,"nombre":e.nombre}
			data.append(resultado)

	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def elementoCombo(request):
	array = {}
	mensaje = {}
	data = []
	elemento = Elemento.objects.all()
	for e in elemento:
			resultado = {"idElemento":e.id,"nombre":e.nombre}
			data.append(resultado)

	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def elementoComboApoyoElemento(request):
	array = {}
	mensaje = {}
	data = []
	idApoyo = request.POST.get('idApoyo', 0)
	elemento = Elemento.objects.filter(apoyo=idApoyo)
	print elemento
	for e in elemento:
		resultado = {"idElemento":e.id,"nombre":e.nombre}
		data.append(resultado)

	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def programaSave(request):
	array = {}
	mensaje = {}
	idOrden = request.POST.get('idOrden', 0)
	idFrente = request.POST.get('idFrente', 0)
	funcion = request.POST.get('funcion', 0)
	funcionHabilitado = request.POST.get('funcionHabilitado', 0)
	fechaInicial = request.POST.get('fechaInicial', 0)
	fechaFinal = request.POST.get('fechaFinal', 0)
	remision = request.POST.get('remision', 0)
	pesoBruto = request.POST.get('pesoBruto', 0)
	pesoTara = request.POST.get('pesoTara', 0)
	pesoTotal = request.POST.get('pesoTotal', 0)
	respuesta = request.POST.get('json')
	json_object = json.loads(respuesta)
	p = ProgramaSuministro(idOrden=idOrden,
							remision=remision,
							funcion_id=funcion,
							funcionHabilitado_id=funcionHabilitado,
							pesoBruto=pesoBruto,
							pesoTara=pesoTara,
							pesoNeto=pesoTotal,
							fechaInicial=datetime.strptime(fechaInicial, '%d/%m/%Y'),
							fechaFinal=datetime.strptime(fechaFinal, '%d/%m/%Y'),
							frente_id=idFrente,
							estatus=1)
	p.save()
	for data in json_object:
		datos = data["data"]
		splitData = datos.split("|")
		apoyo = splitData[0]
		elemento = splitData[1]
		idMaterial = splitData[2]
		cantidadMaterial= splitData[3]
		pesoMaterial = splitData[4]
		longitud = splitData[5]
		pd = ProgramaSuministroDetalle(programaSuministro_id=p.pk,
										material_id=idMaterial,
										apoyo_id=apoyo,
										elemento_id=elemento,
										peso=pesoMaterial,
										cantidad=cantidadMaterial,
										longitud=longitud
										)
		pd.save();
	mensaje = {"estatus":"ok", "mensaje":"Se creo el Programa de Suministro exitosamente.", "folio":p.id}
	array = mensaje
	return JsonResponse(array)

def asignacionSave(request):
	array = {}
	mensaje = {}
	respuesta = request.POST.get('json')
	json_object = json.loads(respuesta)
	for data in json_object:
		datos = data["data"]
		splitData = datos.split("|")
		peso = splitData[0]
		dias = splitData[1]
		orden = splitData[2]
		frente = splitData[3]
		programa = splitData[4]
		elemento= splitData[5]
		funcion = splitData[6]
		c = ControlAsignacion(cantidad=peso, tiempoEntrega=dias, estatus=1, frente_id=frente, funcion_id=funcion, programaSuministro_id=programa, idOrden=orden, programaSuministroDetalle_id=elemento)
		c.save();
	mensaje = {"estatus":"ok", "mensaje":"Se realizaron las asignaciones correspondientes"}
	array = mensaje
	return JsonResponse(array)

def elementoMaterial(request):
	array = {}
	mensaje = {}
	data = []
	idElemento = request.POST.get('idElemento', 0)
	elemento = Material.objects.values(
										'id',
										'nombre',
										'numero',
										'peso',
										'diametro',
										'proveedor',
										'longitud',
										'factor__pva',
										'factor__factorPulgada',
										'factor__pi').filter()
	#print elemento.query
	for e in elemento:
		diametro = e['diametro']
		pva = e['factor__pva']
		factorPulgada = e['factor__factorPulgada']
		pi = e['factor__pi']
		diametroMetro = diametro / 1000
		factorCalculado = ((pi * diametroMetro * diametroMetro) / 4) * pva
		factorCalculadoDecimal = "%.4f" % factorCalculado
		resultado = {
						"idMaterial":e['id'],
						"nombreMaterial":e['nombre'],
						"materialNumero":e['numero'],
						"materialPeso":e['peso'],
						"materialProveedor":e['proveedor'],
						"materialLongitud":e['longitud'],
						"conversion":factorCalculadoDecimal}
		data.append(resultado)
	array["data"]=data
	return JsonResponse(array)

def frenteActualizaestatus(request):
	array = {}
	mensaje = {}
	data = []
	mensaje = {"estatus":"ok", "mensaje":"Correcto"}
	frente = request.POST['frente']
	Frente.objects.filter(id=frente).update(estatusFrente=1)
	array = mensaje
	return JsonResponse(array)


	#catalogos#

def apoyosView(request):
	apoyo_list = Apoyo.objects.filter(estatus=1)
	paginator = Paginator(apoyo_list, 10)
	page = request.GET.get('page')
	try:
		apoyos = paginator.page(page)
	except PageNotAnInteger:
		apoyos = paginator.page(1)
	except EmptyPage:
		apoyos = paginator.page(paginator.num_pages)
	return render_to_response('control_acero/catalogos/apoyos/apoyo.html', {"apoyos": apoyos})

def apoyosNewView(request):
	if request.method == "POST":
		form = ApoyoForm(request.POST)
		if(form.is_valid()):
			apoyo = form.save(commit=False)
			apoyo.save()
			#return render(request, 'control_acero/catalogos/apoyos/apoyo.html', {'form': form})
	else:
		form = ApoyoForm()
		
	return render(request, 'control_acero/catalogos/apoyos/apoyo_new.html', {'form': form})

def apoyosEditView(request, pk):
	apoyo = get_object_or_404(Apoyo, pk=pk)
	if request.method == "POST":
		form = ApoyoForm(request.POST, instance=apoyo)
		if(form.is_valid()):
			apoyo = form.save(commit=False)
			apoyo.save()
			#return render(request, 'control_acero/catalogos/apoyos/apoyo.html', {'form': form})
	else:
		form = ApoyoForm(instance=apoyo)
		
	return render(request, 'control_acero/catalogos/apoyos/apoyo_edit.html', {'form': form})

def apoyosLogicalDelete(request, pk):
	apoyo = get_object_or_404(Apoyo, pk=pk)

	
	if request.method == "POST":
		form = ApoyoForm(request.POST, estatus=0, instance=apoyo)
		if(form.is_valid()):
			apoyo = form.save(commit=False)
			apoyo.save()
			print estatus
			#return render(request, 'control_acero/catalogos/apoyos/apoyo.html', {'form': form})
	else:
		form = ApoyoForm(instance=apoyo)
		
	return render(request, 'control_acero/catalogos/apoyos/apoyo_delete.html', {'form': form})
	

def elementosView(request):
	elemento_list = Elemento.objects.filter(estatus=1)
	paginator = Paginator(elemento_list, 10)
	page = request.GET.get('page')
	try:
		elementos = paginator.page(page)
	except PageNotAnInteger:
		elementos = paginator.page(1)
	except EmptyPage:
		elementos = paginator.page(paginator.num_pages)
	return render_to_response('control_acero/catalogos/elementos/elementos.html', {"elementos": elementos})

def elementosNewView(request):
	if request.method == "POST":
		form = ElementoForm(request.POST)
		if(form.is_valid()):
			elemento = form.save(commit=False)
			elemento.save()
			#return render(request, 'control_acero/catalogos/apoyos/apoyo.html', {'form': form})
	else:
		form = ElementoForm()
		
	return render(request, 'control_acero/catalogos/elementos/elementos_new.html', {'form': form})

def elementosEditView(request, pk):
	elemento = get_object_or_404(Elemento, pk=pk)
	if request.method == "POST":
		form = ElementoForm(request.POST, instance=elemento)
		if(form.is_valid()):
			elemento = form.save(commit=False)
			elemento.save()
			#return render(request, 'control_acero/catalogos/apoyos/apoyo.html', {'form': form})
	else:
		form = ElementoForm(instance=elemento)
		
	return render(request, 'control_acero/catalogos/elementos/elementos_edit.html', {'form': form})

	
def despiecesView(request):
	despiece_list = Despiece.objects.filter(estatus=1)
	paginator = Paginator(despiece_list, 10)
	page = request.GET.get('page')
	try:
		despieces= paginator.page(page)
	except PageNotAnInteger:
		despieces = paginator.page(1)
	except EmptyPage:
		despieces = paginator.page(paginator.num_pages)
	return render_to_response('control_acero/catalogos/despieces/despiece.html', {"despieces": despieces})


def despiecesNewView(request):
	if request.method == "POST":
		form = DespieceForm(request.POST)
		if(form.is_valid()):
			despiece = form.save(commit=False)
			despiece.save()
			#return render(request, 'control_acero/catalogos/apoyos/apoyo.html', {'form': form})
	else:
		form = DespieceForm()
		
	return render(request, 'control_acero/catalogos/despieces/despiece_new.html', {'form': form})

def despiecesEditView(request, pk):
	despiece = get_object_or_404(Despiece, pk=pk)
	if request.method == "POST":
		form = DespieceForm(request.POST, instance=despiece)
		if(form.is_valid()):
			despiece = form.save(commit=False)
			despiece.save()
			#return render(request, 'control_acero/catalogos/apoyos/apoyo.html', {'form': form})
	else:
		form = DespieceForm(instance=despiece)
		
	return render(request, 'control_acero/catalogos/despieces/despiece_edit.html', {'form': form})

def materialesView(request):
	material_list = Material.objects.filter(estatus=1)
	paginator = Paginator(material_list, 10)
	page = request.GET.get('page')
	try:
		materiales = paginator.page(page)
	except PageNotAnInteger:
		materiales = paginator.page(1)
	except EmptyPage:
		materiales = paginator.page(paginator.num_pages)
	return render_to_response('control_acero/catalogos/materiales/material.html', {"materiales": materiales})

def materialesNewView(request):
	if request.method == "POST":
		form = MaterialForm(request.POST, request.FILES)
		if(form.is_valid()):
			material = form.save(commit=False)
			material.save()
			#return render(request, 'control_acero/catalogos/apoyos/apoyo.html', {'form': form})
	else:
		form = MaterialForm()
		
	return render(request, 'control_acero/catalogos/materiales/material_new.html', {'form': form})

def materialesEditView(request, pk):
	material = get_object_or_404(Material, pk=pk)
	if request.method == "POST":
		form = MaterialForm(request.POST, request.FILES, instance=material)
		if(form.is_valid()):
			material = form.save(commit=False)
			material.save()
			#return render(request, 'control_acero/catalogos/apoyos/apoyo.html', {'form': form})
	else:
		form = MaterialForm(instance=material)
		
	return render(request, 'control_acero/catalogos/materiales/material_edit.html', {'form': form})

def frentesView(request):
	frente_list = Frente.objects.filter(estatus=1)
	paginator = Paginator(frente_list, 10)
	page = request.GET.get('page')
	try:
		frentes = paginator.page(page)
	except PageNotAnInteger:
		frentes = paginator.page(1)
	except EmptyPage:
		frentes = paginator.page(paginator.num_pages)
	return render_to_response('control_acero/catalogos/frentes/frente.html', {"frentes": frentes})

def frentesNewView(request):
	if request.method == "POST":
		form = FrenteForm(request.POST)
		if(form.is_valid()):
			frente = form.save(commit=False)
			frente.save()
			#return render(request, 'control_acero/catalogos/apoyos/apoyo.html', {'form': form})
	else:
		form = FrenteForm()
		
	return render(request, 'control_acero/catalogos/frentes/frente_new.html', {'form': form})

def frentesEditView(request, pk):
	frente = get_object_or_404(Frente, pk=pk)
	if request.method == "POST":
		form = FrenteForm(request.POST, instance=frente)
		if(form.is_valid()):
			frente = form.save(commit=False)
			frente.save()
			#return render(request, 'control_acero/catalogos/apoyos/apoyo.html', {'form': form})
	else:
		form = FrenteForm(instance=frente)
		
	return render(request, 'control_acero/catalogos/frentes/frente_edit.html', {'form': form})


def funcionesView(request):
	funciones_list = Funcion.objects.filter(estatus=1)
	paginator = Paginator(funciones_list, 10)
	page = request.GET.get('page')
	try:
		funciones = paginator.page(page)
	except PageNotAnInteger:
		funciones = paginator.page(1)
	except EmptyPage:
		funciones = paginator.page(paginator.num_pages)
	return render_to_response('control_acero/catalogos/funciones/funcion.html', {"funciones": funciones})

def funcionesNewView(request):
	if request.method == "POST":
		form = FuncionForm(request.POST)
		if(form.is_valid()):
			funcion = form.save(commit=False)
			funcion.save()
			#return render(request, 'control_acero/catalogos/apoyos/apoyo.html', {'form': form})
	else:
		form = FuncionForm()
		
	return render(request, 'control_acero/catalogos/funciones/funcion_new.html', {'form': form})

def funcionesEditView(request, pk):
	funcion = get_object_or_404(Funcion, pk=pk)
	if request.method == "POST":
		form = FuncionForm(request.POST, instance=funcion)
		if(form.is_valid()):
			funcion = form.save(commit=False)
			funcion.save()
			#return render(request, 'control_acero/catalogos/apoyos/apoyo.html', {'form': form})
	else:
		form = FuncionForm(instance=funcion)
		
	return render(request, 'control_acero/catalogos/funciones/funcion_edit.html', {'form': form})

def talleresView(request):
	talleres_list = Taller.objects.filter(estatus=1)
	paginator = Paginator(talleres_list, 10)
	page = request.GET.get('page')
	try:
		talleres = paginator.page(page)
	except PageNotAnInteger:
		talleres = paginator.page(1)
	except EmptyPage:
		talleres = paginator.page(paginator.num_pages)
	return render_to_response('control_acero/catalogos/talleres/taller.html', {"talleres": talleres})

def talleresNewView(request):
	if request.method == "POST":
		form = TallerForm(request.POST)
		if(form.is_valid()):
			funcion = form.save(commit=False)
			funcion.save()
			#return render(request, 'control_acero/catalogos/apoyos/apoyo.html', {'form': form})
	else:
		form = TallerForm()
		
	return render(request, 'control_acero/catalogos/talleres/taller_new.html', {'form': form})

def talleresEditView(request, pk):
	taller = get_object_or_404(Taller, pk=pk)
	if request.method == "POST":
		form = TallerForm(request.POST, instance=taller)
		if(form.is_valid()):
			taller = form.save(commit=False)
			taller.save()
			#return render(request, 'control_acero/catalogos/apoyos/apoyo.html', {'form': form})
	else:
		form = TallerForm(instance=taller)
		
	return render(request, 'control_acero/catalogos/talleres/taller_edit.html', {'form': form})

def transportesView(request):
	transportes_list = Transporte.objects.filter(estatus=1)
	paginator = Paginator(transportes_list, 10)
	page = request.GET.get('page')
	try:
		transportes = paginator.page(page)
	except PageNotAnInteger:
		transportes = paginator.page(1)
	except EmptyPage:
		transportes = paginator.page(paginator.num_pages)
	return render_to_response('control_acero/catalogos/transportes/transporte.html', {"transportes": transportes})

def transportesNewView(request):
	if request.method == "POST":
		form = TransporteForm(request.POST)
		if(form.is_valid()):
			funcion = form.save(commit=False)
			funcion.save()
			#return render(request, 'control_acero/catalogos/apoyos/apoyo.html', {'form': form})
	else:
		form = TransporteForm()
		
	return render(request, 'control_acero/catalogos/transportes/transporte_new.html', {'form': form})

def transportesEditView(request, pk):
	transporte = get_object_or_404(Transporte, pk=pk)
	if request.method == "POST":
		form = TransporteForm(request.POST, instance=transporte)
		if(form.is_valid()):
			transporte = form.save(commit=False)
			transporte.save()
			#return render(request, 'control_acero/catalogos/apoyos/apoyo.html', {'form': form})
	else:
		form = TransporteForm(instance=transporte)
		
	return render(request, 'control_acero/catalogos/transportes/transporte_edit.html', {'form': form})


def suministroAsignaSave(request):
	array = {}
	mensaje = {}
	respuesta = request.POST.get('json')
	json_object = json.loads(respuesta)
	for data in json_object:
		datos = data["data"]
		splitData = datos.split("|")
		idSuministro = splitData[0]
		idAsignacion = splitData[1]
		pesoSolicitado = splitData[2]
		pesoRecibido = splitData[3]
		idFuncion = splitData[4]
		tipoRecepcion = splitData[5]
		archivos = splitData[6]
		archivosRemision = splitData[7]
		e = Etapa(pesoSolicitado = pesoSolicitado,
								pesoRecibido = pesoRecibido,
								estatusEtapa = 1,
								estatus = 1,
								controlAsignacion_id = idAsignacion,
								funcion_id = idFuncion, programaSuministro_id = idSuministro,
								tipoRecepcion = tipoRecepcion)
		e.save();
		if(archivos != ""):
			archivo = archivos.split("}{")
			for file in archivo:
				fileBase64 = leeArchivo("control_acero/tmp/"+file)
				fileExtension = os.path.splitext(file)
				a = Archivo(archivo = fileBase64,
								extension = fileExtension[1],
								nombreArchivo = file,
								etapa_id = e.pk,
								estatus = 1,
								tipo = 1)
				a.save();
		if(archivosRemision != ""):
			archivoRemision = archivosRemision.split("}{")
			for fileRemision in archivoRemision:
				fileRemisionBase64 = leeArchivo("control_acero/tmp/"+fileRemision)
				fileRemisionExtension = os.path.splitext(fileRemision)
				a = Archivo(archivo = fileRemisionBase64,
								extension = fileRemisionExtension[1],
								nombreArchivo = fileRemision,
								etapa_id = e.pk,
								estatus = 1,
								tipo = 2)
				a.save();
	mensaje = {"estatus":"ok", "mensaje":"Se realizo la recepcion de suministro correctamente."}
	array = mensaje
	return JsonResponse(array)

def leeArchivo(archivo):
	with open(archivo, "rb") as f:
		data = f.read()
		fileBase64Encode = data.encode("base64")
	os.remove(archivo);
	return fileBase64Encode

def suministroAsignarSave(request):
	array = {}
	mensaje = {}
	funcionMaterial = request.POST.get('funcionMaterial')
	respuesta = request.POST.get('json')
	json_object = json.loads(respuesta)
	cantidadRestante = 0;
	pesoDetalleDecimal = 0;
	for data in json_object:
		datos = data["data"]
		splitData = datos.split("|")
		idDetalleSuministro = splitData[0]
		peso = splitData[1]
		cantidad = splitData[2]
		idFuncion = splitData[3]
		idTaller = splitData[4]
		cantidadAsignada = splitData[5]
		idPrograma = splitData[6]
		funcion = Funcion.objects.filter(id=idFuncion)
		for f in funcion:
			if f.tipo == 2:
				etapa = 1
			if f.tipo == 3:
				etapa = 3
			if f.tipo == 4:
				etapa = 4
		e = Etapa.objects.create(peso=peso,
									cantidad=cantidad,
									estatusEtapa=etapa,
									estatus=1,
									funcion_id=idFuncion,
									taller_id=idTaller,
									cantidadAsignada=cantidadAsignada)
		programaSuministroDetalle = ProgramaSuministroDetalle.objects\
								.values("id", "peso")\
								.filter(programaSuministro__funcion_id=funcionMaterial,
										material_id=idDetalleSuministro)\
								.order_by("id")

		restante=0
		restanteVerifica = 0
		cantidadRestanteU = 0
		banderaValidaOtro = 0
		for p in programaSuministroDetalle:
			etapaDescuento = EtapaDescuento.objects.filter(remision=p["id"])
			if etapaDescuento.exists():
				for etapaDesc in etapaDescuento:
					if etapaDesc.remision == p["id"] and etapaDesc.estatusEtapa == 1:
						cantidadRestanteU =  etapaDesc.cantidadRestante - Decimal(cantidadAsignada)
						edu = EtapaDescuento.objects.create(peso=peso,
															cantidad=cantidad,
															remision=etapaDesc.remision,
															cantidadRemision = etapaDesc.cantidadRemision,
															cantidadAsignada = etapaDesc.cantidadRestante,
															cantidadRestante = cantidadRestanteU,
															etapa_id = e.pk,
															estatusEtapa = 1
														)
						if cantidadRestanteU <= 0:
							EtapaDescuento.objects.filter(id=etapaDesc.id).update(estatusEtapa=0)
							EtapaDescuento.objects.filter(id=edu.id).update(estatusEtapa=0)
							banderaValidaOtro = 1
						if cantidadRestanteU > 0:
							banderaValidaOtro = 2
						
			else:
				if banderaValidaOtro == 1:
					break
				if banderaValidaOtro == 2:
					break
				estatusEtapa = 1
				if restante < 0:
					restanteResta = abs(restante)
					restante = Decimal(p["peso"]) - restanteResta
				else:
					restanteVerifica = restante
					restante = Decimal(p["peso"]) - Decimal(cantidadAsignada)
					if restanteVerifica > 0:
						restante = abs(restante)

				if restante <= 0:
					estatusEtapa = 0
				ed = EtapaDescuento.objects.create(peso=peso,
													cantidad=cantidad,
													remision=p["id"],
													cantidadRemision = p["peso"],
													cantidadAsignada = cantidadAsignada,
													cantidadRestante = restante,
													etapa_id = e.pk,
													estatusEtapa = estatusEtapa
												)

				if restante > 0:
					break

	mensaje = {"estatus":"ok", "mensaje":"Se realizo la Asignación de Material correctamente."}
	array = mensaje
	return JsonResponse(array)

# def suministroAsignarSave(request):
# 	array = {}
# 	mensaje = {}
# 	funcionMaterial = request.POST.get('funcionMaterial')
# 	respuesta = request.POST.get('json')
# 	json_object = json.loads(respuesta)
# 	cantidadRestante = 0;
# 	pesoDetalleDecimal = 0;
# 	for data in json_object:
# 		datos = data["data"]
# 		splitData = datos.split("|")
# 		idDetalleSuministro = splitData[0]
# 		peso = splitData[1]
# 		cantidad = splitData[2]
# 		idFuncion = splitData[3]
# 		idTaller = splitData[4]
# 		cantidadAsignada = splitData[5]
# 		idPrograma = splitData[6]
# 		funcion = Funcion.objects.filter(id=idFuncion)
# 		for f in funcion:
# 			if f.tipo == 2:
# 				etapa = 1
# 			if f.tipo == 3:
# 				etapa = 3
# 			if f.tipo == 4:
# 				etapa = 4
# 		e = Etapa.objects.create(peso=peso,
# 									cantidad=cantidad,
# 									estatusEtapa=etapa,
# 									estatus=1,
# 									funcion_id=idFuncion,
# 									taller_id=idTaller,
# 									cantidadAsignada=cantidadAsignada)
# 		programaSuministroDetalle = ProgramaSuministroDetalle.objects\
# 								.values("id", "peso")\
# 								.filter(programaSuministro__funcion_id=funcionMaterial,
# 										material_id=idDetalleSuministro)\
# 								.order_by("id")

# 		restante=0
# 		restanteVerifica = 0
# 		cantidadRestanteU = 0
# 		banderaValidaOtro = 0
# 		for p in programaSuministroDetalle:
# 			etapaDescuento = EtapaDescuento.objects.filter(remision=p["id"])
# 			if etapaDescuento.exists():
# 				for etapaDesc in etapaDescuento:
# 					if etapaDesc.remision == p["id"] and etapaDesc.estatusEtapa == 1:
# 						cantidadRestanteU =  etapaDesc.cantidadRestante - Decimal(cantidadAsignada)
# 						edu = EtapaDescuento.objects.create(peso=peso,
# 															cantidad=cantidad,
# 															remision=etapaDesc.remision,
# 															cantidadRemision = etapaDesc.cantidadRemision,
# 															cantidadAsignada = etapaDesc.cantidadRestante,
# 															cantidadRestante = cantidadRestanteU,
# 															etapa_id = e.pk,
# 															estatusEtapa = 1
# 														)
# 						if cantidadRestanteU <= 0:
# 							EtapaDescuento.objects.filter(id=etapaDesc.id).update(estatusEtapa=0)
# 							EtapaDescuento.objects.filter(id=edu.id).update(estatusEtapa=0)
# 							banderaValidaOtro = 1
# 						if cantidadRestanteU > 0:
# 							banderaValidaOtro = 2
						
# 			else:
# 				if banderaValidaOtro == 1:
# 					break
# 				if banderaValidaOtro == 2:
# 					break
# 				estatusEtapa = 1
# 				if restante < 0:
# 					restanteResta = abs(restante)
# 					restante = Decimal(p["peso"]) - restanteResta
# 				else:
# 					restanteVerifica = restante
# 					restante = Decimal(p["peso"]) - Decimal(cantidadAsignada)
# 					if restanteVerifica > 0:
# 						restante = abs(restante)

# 				if restante < 0:
# 					estatusEtapa = 0
# 				ed = EtapaDescuento.objects.create(peso=peso,
# 													cantidad=cantidad,
# 													remision=p["id"],
# 													cantidadRemision = p["peso"],
# 													cantidadAsignada = cantidadAsignada,
# 													cantidadRestante = restante,
# 													etapa_id = e.pk,
# 													estatusEtapa = estatusEtapa
# 												)

# 				if restante > 0:
# 					break

# 	mensaje = {"estatus":"ok", "mensaje":"Se realizo la Asignación de Material correctamente."}
# 	array = mensaje
# 	return JsonResponse(array)

def habilitadoRecepcionSave(request):
	array = {}
	mensaje = {}
	respuesta = request.POST.get('json')
	json_object = json.loads(respuesta)
	for data in json_object:
		idEtapa = data["data"]
		etapaConsulta = Etapa.objects.filter(id=idEtapa)
		for ec in etapaConsulta:
			e = Etapa(peso=ec.peso,
								cantidad=ec.cantidad,
								cantidadAsignada=ec.cantidadAsignada,
								estatusEtapa=2,
								estatus=1,
								funcion_id=ec.funcion_id,
								taller_id=ec.taller_id,
								transporte_id=ec.transporte_id,
								programaSuministro_id=ec.programaSuministro_id,
								programaSuministroDetalle_id=ec.programaSuministroDetalle_id)
			e.save();
	mensaje = {"estatus":"ok", "mensaje":"Se realizo la recepcion de suministro correctamente."}
	array = mensaje
	return JsonResponse(array)

def habilitadoAsignarSave(request):
	array = {}
	mensaje = {}
	programa = request.POST.get('programa')
	funcion = request.POST.get('funcion')
	elemento = request.POST.get('elemento')
	funcionSelect = request.POST.get('funcionSelect')
	taller = request.POST.get('taller')
	transporte = request.POST.get('transporte')
	cantidad = request.POST.get('cantidad')
	respuesta = request.POST.get('json')
	json_object = json.loads(respuesta)

	respuestaAsignacion = request.POST.get('jsonAsignacion')
	json_objectAsignacion = json.loads(respuestaAsignacion)

	respuestaAsignacionDetalle = request.POST.get('jsonAsignacionDetalle')
	json_objectAsignacionDetalle = json.loads(respuestaAsignacionDetalle)

	for data in json_object:
		idEtapa = data["dataIdEtapa"]
		etapaConsulta = Etapa.objects.values("cantidad",
														"peso",
														"cantidadAsignada",
														"programaSuministroDetalle_id",
														"programaSuministroDetalle__material_id")\
												.filter(id=idEtapa)
		for ec in etapaConsulta:
			idMaterialEtapa = ec["programaSuministroDetalle__material_id"]
			ea = Etapa.objects.create(estatusEtapa=3,
												estatus=1,
												funcion_id=funcionSelect,
												taller_id=taller,
												transporte_id=transporte,
												programaSuministro_id=programa,
												cantidad=ec["cantidad"],
												peso=ec["peso"],
												cantidadAsignada=ec["cantidadAsignada"],
												programaSuministroDetalle_id=ec["programaSuministroDetalle_id"]
												)
			for dataA in json_objectAsignacion:
				dataAsignacion = dataA["dataAsignacion"]
				splitData = dataAsignacion.split("|")
				despiecePeso = splitData[0]
				pesoRecibido = splitData[1]
				pesoAsignado = splitData[2]
				idMaterialDespiece = splitData[3]
				if int(idMaterialEtapa) == int(idMaterialDespiece):
					ead = EtapaDespiece.objects.create(despieceTotal=despiecePeso,
																	pesoRecibido=pesoRecibido,
																	pesoRestante=pesoAsignado,
																	material_id=idMaterialDespiece,
																	cantidad=cantidad,
																	elemento_id=elemento)
					ea.EtapaDespiece.add(ead)
					for dataAD in json_objectAsignacionDetalle:
						dataAsignacionDetalle = dataAD["dataAsignacionDetalle"]
						splitDataDetalle = dataAsignacionDetalle.split("|")
						idDespiece = splitDataDetalle[0]
						despiecePesoDetalle = splitDataDetalle[1]
						idMaterialDetalle = splitDataDetalle[2]
						if int(idMaterialDespiece) == int(idMaterialDetalle):
							eadet = EtapaDespieceDetalle.objects.create(despiece_id=idDespiece,
																					despiecePeso=despiecePesoDetalle)
							ead.EtapaDespieceDetalle.add(eadet)
	mensaje = {"estatus":"ok", "mensaje":"Se realizo la asignacion de Habilitado."}
	array = mensaje
	return JsonResponse(array)

def armadoAsignaSave(request):
	array = {}
	mensaje = {}
	respuesta = request.POST.get('json')
	json_object = json.loads(respuesta)
	for data in json_object:
		datos = data["data"]
		splitData = datos.split("|")
		idEtapaDetalle = splitData[0]
		pesoRecibido = splitData[1]
		etapa = Etapa.objects.values("id",
										"peso",
										"cantidad",
										"cantidadAsignada",
										"funcion_id",
										"programaSuministro_id",
										"programaSuministroDetalle_id",
										"taller_id",
										"transporte_id")\
								.filter(EtapaDespiece__EtapaDespieceDetalle__id=idEtapaDetalle)
		etapaDespiece = Etapa.objects.values("EtapaDespiece__despieceTotal",
										"EtapaDespiece__pesoRecibido",
										"EtapaDespiece__pesoRestante",
										"EtapaDespiece__cantidad",
										"EtapaDespiece__elemento__id",
										"EtapaDespiece__material__id")\
								.filter(EtapaDespiece__EtapaDespieceDetalle__id=idEtapaDetalle)
		etapaDetalle = EtapaDespieceDetalle.objects.values("despiece_id")\
								.filter(id=idEtapaDetalle)
		for e in etapa:
			e = Etapa.objects.create(peso=e["peso"],
						cantidad=e["cantidad"],
						cantidadAsignada=e["cantidadAsignada"],
						estatusEtapa=4,
						estatus=1,
						funcion_id=e["funcion_id"],
						programaSuministro_id=e["programaSuministro_id"],
						programaSuministroDetalle_id=e["programaSuministroDetalle_id"],
						taller_id=e["taller_id"],
						transporte_id=e["transporte_id"])

		for edes in etapaDespiece:
			edes = EtapaDespiece.objects.create(despieceTotal=edes["EtapaDespiece__despieceTotal"],
												pesoRecibido=edes["EtapaDespiece__pesoRecibido"],
												pesoRestante=edes["EtapaDespiece__pesoRestante"],
												cantidad=edes["EtapaDespiece__cantidad"],
												elemento_id=edes["EtapaDespiece__elemento__id"],
												material_id=edes["EtapaDespiece__material__id"])
			e.EtapaDespiece.add(edes)
		for ed in etapaDetalle:
			eds = EtapaDespieceDetalle.objects.create(despiece_id=ed["despiece_id"],
						despiecePeso=pesoRecibido)
			edes.EtapaDespieceDetalle.add(eds)
	mensaje = {"estatus":"ok", "mensaje":"Se realizo la recepcion de Armado correctamente."}
	array = mensaje
	return JsonResponse(array)

def armadoAsignacionSave(request):
	array = {}
	mensaje = {}
	suministroEtapa = request.POST.get('suministro')
	funcionEtapa = request.POST.get('funcion')
	elementoEtapa = request.POST.get('elemento')
	respuesta = request.POST.get('json')
	json_object = json.loads(respuesta)
	for data in json_object:
		datos = data["data"]
		splitData = datos.split("|")
		funcion = splitData[0]
		transporte = splitData[1]
		etapa = Etapa.objects.values("id",
												"pesoSolicitado",
												"pesoRecibido",
												"tiempoEntrega", 
												"cantidadAsignada",
												"controlAsignacion_id",
												"funcion_id",
												"taller_id",
												"transporte_id",
												"programaSuministro_id",
												"idEtapaPertenece",
												"piezasRecibidas",
												"despiece_id"
											).filter(estatusEtapa = 5, 
														funcion_id = funcionEtapa, 
														programaSuministro_id = suministroEtapa,
														controlAsignacion__programaSuministroDetalle__elemento__id = elementoEtapa)
		for e in etapa:
			e = Etapa(pesoSolicitado = e["pesoSolicitado"],
									pesoRecibido = e["pesoRecibido"],
									tiempoEntrega = e["tiempoEntrega"],
									cantidadAsignada = e["cantidadAsignada"],
									estatusEtapa = 6,
									controlAsignacion_id = e["controlAsignacion_id"],
									funcion_id =funcion,
									transporte_id = e["transporte_id"],
									programaSuministro_id = e["programaSuministro_id"],
									idEtapaPertenece = e["idEtapaPertenece"],
									piezasRecibidas = e["piezasRecibidas"],
									despiece_id = e["despiece_id"])
			e.save()
	mensaje = {"estatus":"ok", "mensaje":"Se realizo la asignacion de Colocado correctamente."}
	array = mensaje
	return JsonResponse(array)

def colocadoRecepcionDetalle(request):
	array = {}
	mensaje = {}
	data = []
	dataFrente = []
	dataApoyo = []
	dataDetalle = []
	programa = request.POST.get('programa', 0)
	funcion = request.POST.get('funcion', 0)
	apoyo = request.POST.get('apoyo', 0)
	etapa = Etapa.objects.values("id",
											"controlAsignacion__frente__id",
											"controlAsignacion__frente__nombre",
											"controlAsignacion__frente__identificacion",
											"controlAsignacion__frente__ubicacion",
											"controlAsignacion__frente__kilometros"
											).filter(estatusEtapa = 6,
														funcion_id = funcion,
														programaSuministro_id = programa,
														controlAsignacion__programaSuministroDetalle__apoyo__id = apoyo)[:1]
	for e in etapa:
		resultado = {"idFrente":e["controlAsignacion__frente__id"],
						"frenteNombre":e["controlAsignacion__frente__nombre"],
						"frenteIdentificacion":e["controlAsignacion__frente__identificacion"],
						"frenteUbicacion":e["controlAsignacion__frente__ubicacion"],
						"frenteKilometro":e["controlAsignacion__frente__kilometros"]
						}
		dataFrente.append(resultado)

	etapa = Etapa.objects.values("controlAsignacion__programaSuministroDetalle__apoyo__id",
									"controlAsignacion__programaSuministroDetalle__apoyo__numero",
									"controlAsignacion__programaSuministroDetalle__elemento__id",
									"controlAsignacion__programaSuministroDetalle__elemento__nombre"
									).filter(estatusEtapa = 1,
												programaSuministro_id = programa)
	for e in etapa:
		resultado = {"apoyoId":e["controlAsignacion__programaSuministroDetalle__apoyo__id"],
						"apoyoNumero":e["controlAsignacion__programaSuministroDetalle__apoyo__numero"],
						"elementoId":e["controlAsignacion__programaSuministroDetalle__elemento__id"],
						"elementoNombre":e["controlAsignacion__programaSuministroDetalle__elemento__nombre"]
						}
		dataApoyo.append(resultado)

	etapaDetalle = Etapa.objects.values("id",
											"pesoRecibido",
											"piezasRecibidas",
											"controlAsignacion__programaSuministroDetalle__apoyo__numero", 
											"controlAsignacion__programaSuministroDetalle__elemento__nombre",
											"despiece__nomenclatura",
											"despiece__cantidad",
											"despiece__longitud",
											"despiece__peso",
											"despiece__figura",
											"despiece__material__nombre"
											).filter(estatusEtapa=6,
														programaSuministro_id=programa,
														controlAsignacion__programaSuministroDetalle__apoyo__id=apoyo)
	for ed in etapaDetalle:
		resultado = {"id":ed["id"],
						"pesoRecibido":ed["pesoRecibido"],
						"piezasRecibidas":ed["piezasRecibidas"],
						"apoyo":ed["controlAsignacion__programaSuministroDetalle__apoyo__numero"],
						"elemento":ed["controlAsignacion__programaSuministroDetalle__elemento__nombre"],
						"despieceNomenclatura":ed["despiece__nomenclatura"],
						"despieceCantidad":ed["despiece__cantidad"],
						"despieceLongitud":ed["despiece__longitud"],
						"despiecePeso":ed["despiece__peso"],
						"despieceFigura":ed["despiece__figura"],
						"despieceMaterial":ed["despiece__material__nombre"]
						}
		dataDetalle.append(resultado)
	array = mensaje
	array["frente"]=dataFrente
	array["apoyo"]=dataApoyo
	array["detalle"]=dataDetalle
	return JsonResponse(array)

def colocadoRecepcionSave(request):
	array = {}
	mensaje = {}
	programa = request.POST.get('programa', 0)
	etapa = Etapa.objects.values("id",
											"pesoSolicitado",
											"pesoRecibido",
											"tiempoEntrega", 
											"cantidadAsignada",
											"controlAsignacion_id",
											"funcion_id",
											"taller_id",
											"transporte_id",
											"programaSuministro_id",
											"idEtapaPertenece",
											"piezasRecibidas",
											"despiece_id"
										).filter(estatusEtapa = 1, 
													programaSuministro_id = programa)
	for e in etapa:
		e = Etapa(pesoSolicitado = e["pesoSolicitado"],
								pesoRecibido = e["pesoRecibido"],
								tiempoEntrega = e["tiempoEntrega"],
								cantidadAsignada = e["cantidadAsignada"],
								estatusEtapa = 7,
								controlAsignacion_id = e["controlAsignacion_id"],
								funcion_id =e["funcion_id"],
								transporte_id = e["transporte_id"],
								programaSuministro_id = e["programaSuministro_id"],
								idEtapaPertenece = e["idEtapaPertenece"],
								piezasRecibidas = e["piezasRecibidas"],
								despiece_id = e["despiece_id"])
		e.save()
	mensaje = {"estatus":"ok", "mensaje":"Se realizo la recepcion del Colocado."}
	array = mensaje
	return JsonResponse(array)

def imagenesBase64(request):
	archivo = request.FILES['archivo']
	archivoName = request.FILES['archivo'].name
	typeFile = request.FILES['archivo'].content_type
	unique_string = get_random_string(length=10)
	nameFile = unique_string+"_"+archivoName
	path = handle_uploaded_file(archivo, nameFile)
	mensaje = {"imagen":nameFile}
	array = mensaje
	return JsonResponse(array)

def handle_uploaded_file(archivo, archivoName):
    with open("control_acero/tmp/"+archivoName, 'wb+') as destination:
        for chunk in archivo.chunks():
            return destination.write(chunk)

def fisicoBusquedaView(request):
	array = {}
	mensaje = {}
	data = []
	dataSuministro = []
	#dataApoyo = []
	#dataDetalle = []
	fechaInicial = request.POST.get('fechaInicial', '17/05/2016')
	fechaFinal = request.POST.get('fechaFinal', '17/05/2016')
	fechaInicialFormat = datetime.strptime(fechaInicial+" 00:00:00", '%d/%m/%Y %H:%M:%S')
	fechaFinalFormat = datetime.strptime(fechaFinal+" 23:59:59", '%d/%m/%Y %H:%M:%S')
	etapas = Etapa.objects.values("id",
												"pesoSolicitado",
												"pesoRecibido",
												"cantidadAsignada").filter(fechaRegistro__gte=fechaInicialFormat,
															fechaRegistro__lte=fechaFinalFormat);
	for e in etapas:
		resultado = {"id":e["id"],
						"pesoSolicitado":e["pesoSolicitado"],
						"pesoRecibido":e["pesoRecibido"],
						"cantidadAsignada":e["cantidadAsignada"]

					}
		dataSuministro.append(resultado)

	array = mensaje
	array["Suministro"]=dataSuministro
	#array["apoyo"]=dataApoyo
	#array["detalle"]=dataDetalle
	return JsonResponse(array)