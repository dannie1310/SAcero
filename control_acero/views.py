# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from control_acero.report.models_auth import Empresa, Usuario
from .models import Apoyo, Elemento, Despiece, Material, Frente, Funcion, ControlAsignacion, ProgramaSuministro, ProgramaSuministroDetalle, EtapaAsignacion, Taller, Transporte, Archivo
from django.utils import timezone
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages
from django.db.models import Count
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
	idPrograma = request.POST.get('programa', 0)
	elementos = ProgramaSuministroDetalle.objects.values('id','numeroCuatro','numeroCuatro','numeroCinco','numeroSeis','numeroSiete','numeroOcho','numeroNueve','numeroDiez','numeroOnce','numeroDoce','total','apoyo__numero','elemento__nombre').filter(idProgramaSuministro=idPrograma)
	for e in elementos:
		resultado = {"id":e["id"],"numeroCuatro":e["numeroCuatro"],"numeroCinco":e["numeroCinco"],"numeroSeis":e["numeroSeis"],"numeroSiete":e["numeroSiete"],"numeroOcho":e["numeroOcho"],"numeroNueve":e["numeroNueve"],"numeroDiez":e["numeroDiez"],"numeroOnce":e["numeroOnce"],"numeroDoce":e["numeroDoce"],"total":e["total"],"apoyoNumero":e["apoyo__numero"],"elementoNombre":e["elemento__nombre"]}
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
	programaSuministro = EtapaAsignacion.objects.all().values_list('programaSuministro_id', flat=True).distinct()
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
	controlFuncion = EtapaAsignacion.objects.all().values_list('funcion_id', flat=True).distinct()
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
	dataFiles = []
	idPrograma = request.POST.get('programa', 1)
	idFuncion = request.POST.get('funcion', 1)
	suministro = EtapaAsignacion.objects.values('id',
													'pesoSolicitado',
													'pesoRecibido',
													'controlAsignacion_id',
													'funcion_id',
													'programaSuministro_id'
													).filter(
													programaSuministro_id = idPrograma,
													funcion_id=idFuncion)
	for s in suministro:
		resultado = {"id":s["id"],
						"pesoSolicitado":s["pesoSolicitado"],
						"pesoRecibido":s["pesoRecibido"],
						"idAsignacion":s["controlAsignacion_id"],
						"idFuncion":s["funcion_id"],
						"idPrograma":s["programaSuministro_id"]}
		data.append(resultado)
		suministroFiles = Archivo.objects.values('id',
													'archivo',
													'etapaAsignacion_id',
													'extension',
													'nombreArchivo',
													'tipo'
													).filter(
													etapaAsignacion_id = s["id"])
		for sf in suministroFiles:
			archivo = sf["archivo"]
			extension = sf["extension"]
			ext = extensiones(extension)
			resultado = {"id":sf["id"],
							"etapaAsignacionId":sf["etapaAsignacion_id"],
							"nombreArchivo":sf["nombreArchivo"],
							"tipo":sf["tipo"],
							"file":"data:"+ext+";charset=utf-8;base64,"+archivo}
			dataFiles.append(resultado)
	array = mensaje
	array["data"]=data
	array["files"]=dataFiles
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
	estapaAsignacion = EtapaAsignacion.objects.filter(estatusEtapa=2).values_list('programaSuministro_id', flat=True).distinct()
	for p in estapaAsignacion:
		resultado = {"idPrograma":p}
		data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def habilitadoAsignaComboFuncion(request):
	array = {}
	mensaje = {}
	data = []
	etapaFuncion = EtapaAsignacion.objects.filter(estatusEtapa=2).values_list('funcion_id', flat=True).distinct()
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
	etapa = EtapaAsignacion.objects.values('id', 'pesoSolicitado', 'pesoRecibido', 'cantidadAsignada', 'taller__id', 'taller__nombre', 'transporte__id', 'transporte__placas', 'programaSuministro_id', 'idEtapaPertenece', 'controlAsignacion_id').filter(programaSuministro_id=idPrograma, funcion_id=idFuncion)
	for e in etapa:
		resultado = {"id":e["id"], "pesoSolicitado":e["pesoSolicitado"], "pesoRecibido":e["pesoRecibido"], "cantidadAsignada":e["cantidadAsignada"], "tallerId":e["taller__id"], "tallerNombre":e["taller__nombre"], "transporteId":e["transporte__id"], "transportePlacas":e["transporte__placas"], "programaSuministro":e["programaSuministro_id"], "idEtapaPertenece":e["idEtapaPertenece"], "idAsignacion":e["controlAsignacion_id"]}
		data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def habilitadoAsignarComboPrograma(request):
	array = {}
	mensaje = {}
	data = []
	estapaAsignacion = EtapaAsignacion.objects.filter(estatusEtapa=3).values_list('programaSuministro_id', flat=True).distinct()
	for p in estapaAsignacion:
		resultado = {"idPrograma":p}
		data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def habilitadoAsignarComboFuncion(request):
	array = {}
	mensaje = {}
	data = []
	etapaFuncion = EtapaAsignacion.objects.filter(estatusEtapa=3).values_list('funcion_id', flat=True).distinct()
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
	suministro = EtapaAsignacion.objects.values('id', 'pesoSolicitado', 'pesoRecibido', 'controlAsignacion_id', 'funcion_id', 'programaSuministro_id').filter(programaSuministro_id=idPrograma, funcion_id=idFuncion, estatusEtapa=3)
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
	etapa = EtapaAsignacion.objects.filter(estatusEtapa=3,
											funcion_id=idFuncion,
											programaSuministro_id=idPrograma).values_list('controlAsignacion__programaSuministroDetalle__elemento__id', flat=True).distinct()
	for e in etapa:
		elemento = Elemento.objects.filter(id=e)
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
	programa = request.POST.get('programa', 0)
	funcion = request.POST.get('funcion', 0)
	elemento = request.POST.get('elemento', 0)
	etapa = EtapaAsignacion.objects.values("id", 
											"pesoSolicitado", 
											"pesoRecibido", 
											"cantidadAsignada", 
											"controlAsignacion_id", 
											"controlAsignacion__programaSuministroDetalle__numeroCuatro", 
											"controlAsignacion__programaSuministroDetalle__numeroCinco", 
											"controlAsignacion__programaSuministroDetalle__numeroSeis", 
											"controlAsignacion__programaSuministroDetalle__numeroSiete", 
											"controlAsignacion__programaSuministroDetalle__numeroOcho", 
											"controlAsignacion__programaSuministroDetalle__numeroNueve", 
											"controlAsignacion__programaSuministroDetalle__numeroDiez", 
											"controlAsignacion__programaSuministroDetalle__numeroOnce", 
											"controlAsignacion__programaSuministroDetalle__numeroDoce", 
											"controlAsignacion__programaSuministroDetalle__total",
											"controlAsignacion__programaSuministroDetalle__elemento__material__numero",
											"controlAsignacion__programaSuministroDetalle__elemento__material__peso",
											"controlAsignacion__programaSuministroDetalle__elemento__material__diametro",
											"controlAsignacion__programaSuministroDetalle__apoyo__numero", 
											"controlAsignacion__programaSuministroDetalle__elemento__nombre"
											).filter(estatusEtapa=3,
														funcion_id=funcion,
														programaSuministro_id=programa,
														controlAsignacion__programaSuministroDetalle__elemento__id=elemento)
	for e in etapa:
		resultado = {"id":e["id"], 
						"pesoSolicitado":e["pesoSolicitado"], 
						"pesoRecibido":e["pesoRecibido"],
						"cantidadAsignada":e["cantidadAsignada"],
						"asignacionId":e["controlAsignacion_id"],
						"suministroNumeroCuatro":e["controlAsignacion__programaSuministroDetalle__numeroCuatro"],
						"suministroNumeroCinco":e["controlAsignacion__programaSuministroDetalle__numeroCinco"],
						"suministroNumeroSeis":e["controlAsignacion__programaSuministroDetalle__numeroSeis"],
						"suministroNumeroSiete":e["controlAsignacion__programaSuministroDetalle__numeroSiete"],
						"suministroNumeroOcho":e["controlAsignacion__programaSuministroDetalle__numeroOcho"],
						"suministroNumeroNueve":e["controlAsignacion__programaSuministroDetalle__numeroNueve"],
						"suministroNumeroDiez":e["controlAsignacion__programaSuministroDetalle__numeroDiez"],
						"suministroNumeroOnce":e["controlAsignacion__programaSuministroDetalle__numeroOnce"],
						"suministroNumeroDoce":e["controlAsignacion__programaSuministroDetalle__numeroDoce"],
						"asignacionTotal":e["controlAsignacion__programaSuministroDetalle__total"],
						"materialNumero":e["controlAsignacion__programaSuministroDetalle__elemento__material__numero"],
						"materialPeso":e["controlAsignacion__programaSuministroDetalle__elemento__material__peso"],
						"materialDiametro":e["controlAsignacion__programaSuministroDetalle__elemento__material__diametro"],
						"apoyo":e["controlAsignacion__programaSuministroDetalle__apoyo__numero"],
						"elemento":e["controlAsignacion__programaSuministroDetalle__elemento__nombre"]}
		data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def armadoAsignarComboPrograma(request):
	array = {}
	mensaje = {}
	data = []
	estapaAsignacion = EtapaAsignacion.objects.filter(estatusEtapa=4).values_list('programaSuministro_id', flat=True).distinct()
	for p in estapaAsignacion:
		resultado = {"idPrograma":p}
		data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def armadoAsignarComboFuncion(request):
	array = {}
	mensaje = {}
	data = []
	etapaFuncion = EtapaAsignacion.objects.filter(estatusEtapa=4).values_list('funcion_id', flat=True).distinct()
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
	etapa = EtapaAsignacion.objects.filter(estatusEtapa=4,
												funcion_id=funcion,
												programaSuministro_id=programa).values_list('controlAsignacion__programaSuministroDetalle__elemento__id', flat=True).distinct()
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
	programa = request.POST.get('programa', 0)
	funcion = request.POST.get('funcion', 0)
	elemento = request.POST.get('elemento', 0)
	etapa = EtapaAsignacion.objects.values("id",
											"controlAsignacion__programaSuministroDetalle__apoyo__numero", 
											"controlAsignacion__programaSuministroDetalle__elemento__nombre",
											"controlAsignacion__programaSuministroDetalle__elemento__despiece__id",
											"controlAsignacion__programaSuministroDetalle__elemento__despiece__nomenclatura",
											"controlAsignacion__programaSuministroDetalle__elemento__despiece__cantidad",
											"controlAsignacion__programaSuministroDetalle__elemento__despiece__longitud",
											"controlAsignacion__programaSuministroDetalle__elemento__despiece__peso",
											"controlAsignacion__programaSuministroDetalle__elemento__despiece__figura",
											"controlAsignacion__programaSuministroDetalle__elemento__despiece__material__nombre"
											).filter(estatusEtapa=4,
														funcion_id=funcion,
														programaSuministro_id=programa,
														controlAsignacion__programaSuministroDetalle__elemento__id=elemento)
	for e in etapa:
		resultado = {"id":e["id"], 
						"apoyo":e["controlAsignacion__programaSuministroDetalle__apoyo__numero"],
						"elemento":e["controlAsignacion__programaSuministroDetalle__elemento__nombre"],
						"despieceId":e["controlAsignacion__programaSuministroDetalle__elemento__despiece__id"],
						"despieceNomenclatura":e["controlAsignacion__programaSuministroDetalle__elemento__despiece__nomenclatura"],
						"despieceCantidad":e["controlAsignacion__programaSuministroDetalle__elemento__despiece__cantidad"],
						"despieceLongitud":e["controlAsignacion__programaSuministroDetalle__elemento__despiece__longitud"],
						"despiecePeso":e["controlAsignacion__programaSuministroDetalle__elemento__despiece__peso"],
						"despieceFigura":e["controlAsignacion__programaSuministroDetalle__elemento__despiece__figura"],
						"despieceMaterial":e["controlAsignacion__programaSuministroDetalle__elemento__despiece__material__nombre"]
						}
		data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def armadoAsignacionComboPrograma(request):
	array = {}
	mensaje = {}
	data = []
	estapaAsignacion = EtapaAsignacion.objects.filter(estatusEtapa=5).values_list('programaSuministro_id', flat=True).distinct()
	for p in estapaAsignacion:
		resultado = {"idPrograma":p}
		data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def armadoAsignacionComboFuncion(request):
	array = {}
	mensaje = {}
	data = []
	etapaFuncion = EtapaAsignacion.objects.filter(estatusEtapa=5).values_list('funcion_id', flat=True).distinct()
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
	etapa = EtapaAsignacion.objects.filter(estatusEtapa=5,
											funcion_id=idFuncion,
											programaSuministro_id=idPrograma).values_list('controlAsignacion__programaSuministroDetalle__elemento__id', flat=True).distinct()
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
	programa = request.POST.get('programa', 0)
	funcion = request.POST.get('funcion', 0)
	elemento = request.POST.get('elemento', 0)
	etapa = EtapaAsignacion.objects.values("id",
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
											).filter(estatusEtapa=5,
														funcion_id=funcion,
														programaSuministro_id=programa,
														controlAsignacion__programaSuministroDetalle__elemento__id=elemento)
	for e in etapa:
		resultado = {"id":e["id"],
						"pesoRecibido":e["pesoRecibido"],
						"piezasRecibidas":e["piezasRecibidas"],
						"apoyo":e["controlAsignacion__programaSuministroDetalle__apoyo__numero"],
						"elemento":e["controlAsignacion__programaSuministroDetalle__elemento__nombre"],
						"despieceNomenclatura":e["despiece__nomenclatura"],
						"despieceCantidad":e["despiece__cantidad"],
						"despieceLongitud":e["despiece__longitud"],
						"despiecePeso":e["despiece__peso"],
						"despieceFigura":e["despiece__figura"],
						"despieceMaterial":e["despiece__material__nombre"]
						}
		data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def colocadoRecepcionComboPrograma(request):
	array = {}
	mensaje = {}
	data = []
	estapaAsignacion = EtapaAsignacion.objects.filter(estatusEtapa=6).values_list('programaSuministro_id', flat=True).distinct()
	for p in estapaAsignacion:
		resultado = {"idPrograma":p}
		data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def colocadoRecepcionComboFuncion(request):
	array = {}
	mensaje = {}
	data = []
	etapaFuncion = EtapaAsignacion.objects.filter(estatusEtapa=6).values_list('funcion_id', flat=True).distinct()
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
	etapa = EtapaAsignacion.objects.values("controlAsignacion__programaSuministroDetalle__apoyo__id",
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
	fechaInicial = request.POST.get('fechaInicial', 0)
	fechaFinal = request.POST.get('fechaFinal', 0)
	respuesta = request.POST.get('json')
	json_object = json.loads(respuesta)
	p = ProgramaSuministro(idOrden=idOrden,
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
		pesoMaterial= splitData[3]
		cantidadMaterial = splitData[4]
		pd = ProgramaSuministroDetalle(programaSuministro_id=p.pk,
										material_id=idMaterial,
										apoyo_id=apoyo,
										elemento_id=elemento,
										peso=pesoMaterial,
										cantidad=cantidadMaterial)
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
	elemento = Elemento.objects.values('id',
										'nombre',
										'material__id',
										'material__nombre',
										'material__numero',
										'material__peso',
										'material__diametro',
										'material__proveedor',
										'material__longitud',
										'material__factor__pva',
										'material__factor__factorPulgada',
										'material__factor__pi').filter(id=idElemento)
	print elemento.query
	for e in elemento:
		diametro = e['material__diametro']
		pva = e['material__factor__pva']
		factorPulgada = e['material__factor__factorPulgada']
		pi = e['material__factor__pi']
		diametroMetro = diametro / 1000
		factorCalculado = ((pi * diametroMetro * diametroMetro) / 4) * pva
		factorCalculadoDecimal = "%.4f" % ((factorCalculado) * e['material__longitud'])
		resultado = {"idElemento":e["id"],
						"nombreElemento":e['nombre'],
						"idMaterial":e['material__id'],
						"nombreMaterial":e['material__nombre'],
						"materialNumero":e['material__numero'],
						"materialPeso":e['material__peso'],
						"materialProveedor":e['material__proveedor'],
						"materialLongitud":e['material__longitud'],
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

def apoyosLogicalDelete(request):
	print request
	#c = Apoyo(id=idApoyo, estatus=0)
	#c.save()

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
		form = MaterialForm(request.POST)
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
		form = MaterialForm(request.POST, instance=material)
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
		
	return render(request, 'control_acero/catalogos/frentes/frentes_new.html', {'form': form})


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
		e = EtapaAsignacion(pesoSolicitado = pesoSolicitado,
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
								etapaAsignacion_id = e.pk,
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
								etapaAsignacion_id = e.pk,
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
	respuesta = request.POST.get('json')
	json_object = json.loads(respuesta)
	print json_object
	for data in json_object:
		datos = data["data"]
		splitData = datos.split("|")
		idAsignacion = splitData[0]
		pesoSolicitado = splitData[1]
		pesoRecibido = splitData[2]
		idFuncion = splitData[3]
		idTaller = splitData[4]
		idTransporte = splitData[5]
		cantidadAsignada = splitData[6]
		idPrograma = splitData[7]
		etapaPertenece = splitData[8]
		funcion = Funcion.objects.filter(id=idFuncion)
		for f in funcion:
			if f.tipo == 2:
				etapa = 2
			if f.tipo == 3:
				etapa = 4
			if f.tipo == 4:
				etapa = 6
		e = EtapaAsignacion(controlAsignacion_id=idAsignacion,
								pesoSolicitado=pesoSolicitado,
								pesoRecibido=pesoRecibido,
								estatusEtapa=etapa,
								estatus=1,
								funcion_id=idFuncion,
								taller_id=idTaller,
								transporte_id=idTransporte,
								cantidadAsignada=cantidadAsignada,
								programaSuministro_id=idPrograma,
								idEtapaPertenece=etapaPertenece)
		e.save();
	mensaje = {"estatus":"ok", "mensaje":"Se realizo la asignación de Suministro correctamente."}
	array = mensaje
	return JsonResponse(array)

def habilitadoRecepcionSave(request):
	array = {}
	mensaje = {}
	respuesta = request.POST.get('json')
	json_object = json.loads(respuesta)
	for data in json_object:
		idEtapa = data["data"]
		etapaConsulta = EtapaAsignacion.objects.filter(id=idEtapa)
		for ec in etapaConsulta:
			e = EtapaAsignacion(pesoSolicitado=ec.pesoSolicitado, pesoRecibido=ec.pesoRecibido, cantidadAsignada=ec.cantidadAsignada, estatusEtapa=3, estatus=1, controlAsignacion_id=ec.controlAsignacion_id, funcion_id=ec.funcion_id, taller_id=ec.taller_id, transporte_id=ec.transporte_id, programaSuministro_id=ec.programaSuministro_id, idEtapaPertenece=ec.idEtapaPertenece)
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
	etapa = EtapaAsignacion.objects.values('id', 'pesoSolicitado', 'pesoRecibido', 'cantidadAsignada', 'controlAsignacion_id', 'funcion_id', 'taller_id', 'transporte_id', 'programaSuministro_id').filter(programaSuministro_id=programa,funcion_id=funcion, controlAsignacion__programaSuministroDetalle__elemento__id=elemento).order_by('-id')[:1]
	for e in etapa:
		e = EtapaAsignacion(pesoSolicitado=e["pesoSolicitado"], pesoRecibido=e["pesoRecibido"], cantidadAsignada=e["cantidadAsignada"], estatusEtapa=4, estatus=1, controlAsignacion_id=e["controlAsignacion_id"], funcion_id=funcionSelect, taller_id=taller, transporte_id=transporte, programaSuministro_id=e["programaSuministro_id"])
		e.save();
		#resultado = {"idElemento":e["id"],"nombreElemento":e['nombre'],"idMaterial":e['material__id'],"nombreMaterial":e['material__nombre'],"materialNumero":e['material__numero'],"materialPeso":e['material__peso'],"materialProveedor":e['material__proveedor']}
	mensaje = {"estatus":"ok", "mensaje":"Se realizo la asignacion de Habilitado."}
	array = mensaje
	return JsonResponse(array)

def armadoAsignaSave(request):
	array = {}
	mensaje = {}
	respuesta = request.POST.get('json')
	json_object = json.loads(respuesta)
	print json_object
	for data in json_object:
		datos = data["data"]
		splitData = datos.split("|")
		idEtapa = splitData[0]
		pesoRecibido = splitData[1]
		piezasRecibidas = splitData[2]
		despieceId = splitData[3]
		etapa = EtapaAsignacion.objects.filter(id=idEtapa);
		for e in etapa:
			e = EtapaAsignacion(pesoSolicitado=e.pesoSolicitado, pesoRecibido=pesoRecibido, cantidadAsignada=e.cantidadAsignada, estatusEtapa=5, estatus=1, controlAsignacion_id=e.controlAsignacion_id, funcion_id=e.funcion_id, programaSuministro_id=e.programaSuministro_id, piezasRecibidas=piezasRecibidas, idEtapaPertenece=idEtapa, despiece_id=despieceId)
			e.save()
	mensaje = {"estatus":"ok", "mensaje":"Se realizo la recepcion de suministro correctamente."}
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
		etapa = EtapaAsignacion.objects.values("id",
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
			e = EtapaAsignacion(pesoSolicitado = e["pesoSolicitado"],
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
	etapa = EtapaAsignacion.objects.values("id",
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

	etapa = EtapaAsignacion.objects.values("controlAsignacion__programaSuministroDetalle__apoyo__id",
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

	etapaDetalle = EtapaAsignacion.objects.values("id",
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
	etapa = EtapaAsignacion.objects.values("id",
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
		e = EtapaAsignacion(pesoSolicitado = e["pesoSolicitado"],
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