# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from control_acero.report.models_auth import Empresa, Usuario
###SE AGREGAN LOS MODELOS A CONSULTAR
from .models import *
from django.utils import timezone
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages
from django.db.models import Count, Sum
import json
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
import md5
from django.contrib import messages
from django.db import connections
from .forms import UserForm, GroupForm, ApoyoForm, ElementoForm, DespieceForm, MaterialForm, FrenteForm, FuncionForm, TallerForm, TransporteForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from django.db import connection
from datetime import datetime
from base64 import b64encode
import os
from django.utils.crypto import get_random_string
from decimal import *
from django.conf import settings
from django.contrib.auth.models import Permission, User

def loginUsuario(request):
	logout(request)
	username = password = ''
	if request.POST:
		username = request.POST['usuario']
		password = request.POST['clave']

		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				url = '/control_acero/principal/'
				return HttpResponseRedirect(url)
	template_name = '/control_acero'
 	messages.error(request, 'Usuario y/o Password invalidos')
 	return HttpResponseRedirect(template_name)

# def loginUsuario(request):
# 	usuario = request.POST['usuario']
# 	clave = request.POST['clave']
# 	if (usuario == ""):
# 		resultado = {"estatus":"error","mensaje":"El campo usuario esta vacio"}
# 		return JsonResponse(resultado)
# 	if (clave == ""):
# 		resultado = {"estatus":"error","mensaje":"El campo clave esta vacio"}
# 		return JsonResponse(resultado)
# 	login = Usuario.objects.using('auth_db').filter(usuario=usuario, clave=md5.new(clave).hexdigest())
# 	for e in login:
# 		if(e != ""):
# 			request.session['idusuario'] = e.idusuario
# 			request.session['usuario'] = e.usuario
# 			url = '/control_acero/principal/'
# 			return HttpResponseRedirect(url)
# 	template_name = '/control_acero'
# 	messages.error(request, 'Usuario y/o Password invalidos')
# 	return HttpResponseRedirect(template_name)

def logout_view(request):
	logout(request)
    	template_name = '/control_acero'
    	return HttpResponseRedirect(template_name)
######################################################
################VISTA DE LOS CATALOGOS################
######################################################
def usuariosNewView(request):
	if request.method == "POST":
		form = UserForm(request.POST)
		if(form.is_valid()):
			new_user = User.objects.create_user(**form.cleaned_data)
			login(new_user)
			#return render(request, 'control_acero/catalogos/apoyos/apoyo.html', {'form': form})
	else:
		form = UserForm()
	return render(request, 'control_acero/catalogos/usuarios/usuario_new.html', {'form': form})

def gruposNewView(request):
	if request.method == "POST":
		form = GroupForm(request.POST)
		if(form.is_valid()):
			new_user = User.objects.create_user(**form.cleaned_data)
			login(new_user)
			#return render(request, 'control_acero/catalogos/apoyos/apoyo.html', {'form': form})
	else:
		form = GroupForm()
	return render(request, 'control_acero/catalogos/grupos/grupo_new.html', {'form': form})

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
		form = DespieceForm(request.POST, request.FILES)
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
		form = DespieceForm(request.POST, request.FILES, instance=despiece)
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

######################################################
######################################################
######################################################

######################################################
###################MODULO1############################
######################################################
def comboFuncion(request):
	array = {}
	mensaje = {}
	data = []
	tipo = request.POST.get('tipo', 0)
	funciones = Funcion.objects.all()\
								.filter(
										tipo = tipo,
										estatus = 1
										)\
								.order_by("proveedor")
	for funcion in funciones:
		resultado = {
						"id":funcion.id,
						"proveedor":funcion.proveedor
					}
		data.append(resultado)
	array["data"]=data
	return JsonResponse(array)

def comboFrente(request):
	array = {}
	mensaje = {}
	data = []
	frentes = Frente.objects.all()\
								.filter(
										estatus = 1
										)\
								.order_by("nombre")
	for frente in frentes:
		resultado = {
						"id":frente.id,
						"nombre":frente.nombre
					}
		data.append(resultado)
	array["data"]=data
	return JsonResponse(array)

def comboApoyo(request):
	array = {}
	mensaje = {}
	data = []
	apoyos = Apoyo.objects.all()\
								.filter(
										estatus = 1
										)\
								.order_by("numero")
	for apoyo in apoyos:
		resultado = {
						"id":apoyo.id,
						"numero":apoyo.numero
					}
		data.append(resultado)
	array["data"]=data
	return JsonResponse(array)

def comboElemento(request):
	array = {}
	mensaje = {}
	data = []
	elementos = Elemento.objects.all()\
								.filter(
										estatus = 1
										)\
								.order_by("nombre")
	for elemento in elementos:
		resultado = {
						"id":elemento.id,
						"nombre":elemento.nombre
					}
		data.append(resultado)
	array["data"]=data
	return JsonResponse(array)

def recepcionMaterialSave(request):
	array = {}
	mensaje = {}
	idOrden = request.POST.get('idOrden', 0)
	numFolio = 0
	#idFrente = request.POST.get('idFrente', 0)
	funcion = request.POST.get('funcion', 0)
	fechaRemision = request.POST.get('fechaRemision', 0)
	remision = request.POST.get('remision', 0)
	pesoBruto = request.POST.get('pesoBruto', 0)
	pesoTara = request.POST.get('pesoTara', 0)
	pesoTotal = request.POST.get('pesoTotal', 0)
	respuesta = request.POST.get('json')
	json_object = json.loads(respuesta)
	p = Remision.objects\
				.create(
						idOrden=idOrden,
						remision=remision,
						funcion_id=funcion,
						pesoBruto=pesoBruto,
						pesoTara=pesoTara,
						pesoNeto=pesoTotal,
						fechaRemision=datetime.strptime(fechaRemision, '%d/%m/%Y'),
						estatus=1
						)
	folio = RemisionDetalle.objects.all().order_by("-numFolio")[:1]
	if folio.exists():
		numFolio = folio[0].numFolio
	numFolioInt = int(numFolio)+1
	numFolio = "%04d" % (numFolioInt,)
	numFolio = "RMH-"+numFolio
	for data in json_object:
		datos = data["data"]
		splitData = datos.split("|")
		apoyo = splitData[0]
		elemento = splitData[1]
		idMaterial = splitData[2]
		cantidadMaterial= splitData[3]
		pesoMaterial = splitData[4]
		longitud = splitData[5]
		pd = RemisionDetalle.objects\
							.create(
									remision_id=p.pk,
									material_id=idMaterial,
									apoyo_id=apoyo,
									elemento_id=elemento,
									peso=pesoMaterial,
									cantidad=cantidadMaterial,
									longitud=longitud,
									folio = numFolio,
									numFolio = numFolioInt
									)
	mensaje = {"estatus":"ok", "mensaje":"Recepción del Material Exitoso. Folio: "+numFolio, "folio":numFolio}
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
						"conversion":factorCalculadoDecimal
					}
		data.append(resultado)
	array["data"]=data
	return JsonResponse(array)

def salidaHabilitadoMaterial(request):
	array = {}
	mensaje = {}
	data = []
	dataDetalle = []
	idFuncion = request.POST.get('funcion', 1)
	cantidadReal = 0
	remisionDetalles = RemisionDetalle.objects\
						.values(
								'material_id',
								'material__nombre'
								)\
						.annotate(pesoMaterial = Sum('peso')) \
						.annotate(cantidadMaterial = Sum('cantidad')) \
						.order_by('material_id')
	for remisionDetalle in remisionDetalles:
		resultado = {
						"id":remisionDetalle["material_id"],
						"materialNombre":remisionDetalle["material__nombre"],
						"peso":remisionDetalle["pesoMaterial"],
						"cantidad":remisionDetalle["cantidadMaterial"]
					}
		data.append(resultado)

	array["data"]=data
	return JsonResponse(array)

def salidaHabilitadoSave(request):
	apoyo = request.POST.get('apoyo', 0)
	elemento = request.POST.get('elemento', 0)
	frente = request.POST.get('frente', 0)
	respuesta = request.POST.get('json')
	jsonDataInfo = json.loads(respuesta)
	numFolio = 0
	array = {}
	mensaje = {}
	data = []
	folio = Salida.objects.all().filter(estatusEtapa = 1).order_by("-numFolio")[:1]
	if folio.exists():
		numFolio = folio[0].numFolio
	numFolioInt = int(numFolio)+1
	numFolio = "%04d" % (numFolioInt,)
	numFolio = "SMH-"+numFolio
	for jsonData in jsonDataInfo:
		material = jsonData["material"]
		cantidadReal = jsonData["cantidadReal"]
		cantidadAsignada = jsonData["cantidadAsignada"]
		salida = Salida.objects\
						.create(
								apoyo_id = apoyo,
								elemento_id = elemento,
								material_id = material,
								frente_id = frente,
								cantidadReal = cantidadReal,
								cantidadAsignada = cantidadAsignada,
								estatusEtapa = 1,
								folio = numFolio,
								numFolio = numFolioInt
								)
	mensaje = {"estatus":"ok", "mensaje":"Salida de Material Exitosa. Folio: "+numFolio, "folio":numFolio}
	array = mensaje
	return JsonResponse(array)

def entradaArmadoComboApoyo(request):
	array = {}
	mensaje = {}
	data = []
	salidaApoyos = Salida.objects.values('apoyo_id').distinct()
	for salidaApoyo in salidaApoyos:
		apoyos = Apoyo.objects.all().filter(id = salidaApoyo["apoyo_id"])
		for apoyo in apoyos:
			resultado = {
							"id":apoyo.id,
							"numero":apoyo.numero
						}
			data.append(resultado)
	array["data"]=data
	return JsonResponse(array)

def entradaArmadoComboElemento(request):
	array = {}
	mensaje = {}
	data = []
	salidaElementos = Salida.objects.values('elemento_id').distinct()
	for salidaElemento in salidaElementos:
		elementos = Elemento.objects.all().filter(id = salidaElemento["elemento_id"])
		for elemento in elementos:
			resultado = {
							"id":elemento.id,
							"nombre":elemento.nombre
						}
			data.append(resultado)
	array["data"]=data
	return JsonResponse(array)

def entradaArmadoMaterial(request):
	array = {}
	mensaje = {}
	data = []
	dataDetalle = []
	idFuncion = request.POST.get('funcion', 1)
	cantidadReal = 0
	remisionDetalles = Salida.objects\
						.values(
								'material_id',
								'material__nombre'
								)\
						.annotate(cantidadAsignada = Sum('cantidadAsignada')) \
						.order_by('material_id')
	for remisionDetalle in remisionDetalles:
		resultado = {
						"id":remisionDetalle["material_id"],
						"materialNombre":remisionDetalle["material__nombre"],
						"cantidadAsignada":remisionDetalle["cantidadAsignada"]
					}
		data.append(resultado)

	array["data"]=data
	return JsonResponse(array)

def entradaArmadoSave(request):
	remision = request.POST.get('remision', 0)
	apoyo = request.POST.get('apoyo', 0)
	elemento = request.POST.get('elemento', 0)
	funcion = request.POST.get('funcion', 0)
	respuesta = request.POST.get('json')
	jsonDataInfo = json.loads(respuesta)
	numFolio = 0
	array = {}
	mensaje = {}
	data = []
	folio = Entrada.objects.all().filter(estatusEtapa = 1).order_by("-numFolio")[:1]
	if folio.exists():
		numFolio = folio[0].numFolio
	numFolioInt = int(numFolio)+1
	numFolio = "%04d" % (numFolioInt,)
	numFolio = "EMA-"+numFolio
	for jsonData in jsonDataInfo:
		material = jsonData["material"]
		cantidadReal = jsonData["cantidadReal"]
		cantidadAsignada = jsonData["cantidadAsignada"]
		entrada = Entrada.objects\
						.create(
								remision = remision,
								elemento_id = elemento,
								material_id = material,
								funcion_id = funcion,
								cantidadReal = cantidadReal,
								cantidadAsignada = cantidadAsignada,
								folio = numFolio,
								numFolio = numFolioInt
								)
	mensaje = {"estatus":"ok", "mensaje":"Entrada de Material Exitosa. Folio: "+numFolio, "folio":numFolio}
	array = mensaje
	return JsonResponse(array)

def foliosMostrar(request):
	modulo = request.POST.get('modulo', 0)
	numFolio = 0
	array = {}
	mensaje = {}
	data = []
	if int(modulo) == 1:
		folio = RemisionDetalle.objects.all().order_by("-numFolio")[:1]
		if folio.exists():
			numFolio = folio[0].numFolio
		numFolioInt = int(numFolio)+1
		numFolio = "%04d" % (numFolioInt,)
		numFolio = "RMH-"+numFolio
	if int(modulo) == 2:
		folio = Salida.objects.all().filter(estatusEtapa = 1).order_by("-numFolio")[:1]
		if folio.exists():
			numFolio = folio[0].numFolio
		numFolioInt = int(numFolio)+1
		numFolio = "%04d" % (numFolioInt,)
		numFolio = "SMH-"+numFolio
	if int(modulo) == 3:
		folio = Entrada.objects.all().filter(estatusEtapa = 1).order_by("-numFolio")[:1]
		if folio.exists():
			numFolio = folio[0].numFolio
		numFolioInt = int(numFolio)+1
		numFolio = "%04d" % (numFolioInt,)
		numFolio = "EMA-"+numFolio
	mensaje = {"estatus":"ok", "folio":numFolio}
	array = mensaje
	return JsonResponse(array)

class IndexView(generic.ListView):
	template_name = 'control_acero/login.html'
	context_object_name = 'ultimos_cinco_productos'
	def get_queryset(self):
		return Material.objects.order_by('despiece')[:9]
	#latest_question_list = Producto.objects.order_by('-fechaRegistro')[:5]
	#context = {'latest_question_list': latest_question_list}
	#return render(request, 'control_acero/index.html', context)

@login_required(login_url='/control_acero/usuario/login/')
def principalView(request):
	template = 'control_acero/principal.html'
	return render(request, template)

@permission_required('control_acero.add_apoyo')
def recepcionMaterialView(request):
	template = 'control_acero/material/recepcion_material_view.html'
	return render(request, template)

def salidaHabilitadoView(request):
	template = 'control_acero/material/salida_habilitado_view.html'
	return render(request, template)

def entradaArmadoView(request):
	template = 'control_acero/armado/entrada_armado_view.html'
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
	cantidadReal = 0
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

	etapas = Etapa.objects\
					.values('material_id')\
					.filter(funcionAnterior_id=idFuncion) \
					.annotate(cantidadAsignada = Sum('cantidadAsignada')) \
					.order_by('material_id')
	for p in ps:
		cantidadReal = p["pesoMaterial"]
		for etapa in etapas:
			if p["material_id"] == etapa["material_id"]:
				cantidadReal = Decimal(p["pesoMaterial"]) - Decimal(etapa["cantidadAsignada"])
		resultado = {"id":p["material_id"],
						"materialNombre":p["material__nombre"],
						"peso":cantidadReal,
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
	idOrdenTrabajo = 0
	etapa = Etapa.objects.values('id',
									'material__nombre',
									'peso',
									'cantidad',
									'cantidadAsignada',
									'taller__id',
									'taller__nombre',
									'transporte__id',
									'transporte__placas',
									'idOrdenTrabajo')\
							.filter(
									funcion_id=idFuncion,
									estatusEtapa=1,
									tipoRecepcion=1)
	print etapa.query
	for e in etapa:
		idOrdenTrabajo = e["idOrdenTrabajo"]
		if e["idOrdenTrabajo"] is None:
			idOrdenTrabajo = 0
		idOrdenTrabajo = idOrdenTrabajo

		resultado = {"id":e["id"],
						"nombreMaterial":e["material__nombre"],
						"peso":e["peso"],
						"cantidad":e["cantidad"],
						"cantidadAsignada":e["cantidadAsignada"],
						"tallerId":e["taller__id"],
						"tallerNombre":e["taller__nombre"],
						"transporteId":e["transporte__id"],
						"transportePlacas":e["transporte__placas"],
						"idOrdenTrabajo":idOrdenTrabajo
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
	etapaFuncion = Etapa.objects.filter(estatusEtapa=1)\
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
	programa = request.POST.get('programa', 0)
	funcion = request.POST.get('funcion', 0)
	elemento = request.POST.get('elemento', 0)
	cantidad = request.POST.get('cantidad', 0)
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
	print elementoRelacion.query
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
									"material_id",
									"material__nombre"
									)\
							.filter(
									funcion_id=funcion,
									estatusEtapa=1,
									estatus=1)
	for et in elementoTotales:
		despiecePeso = Decimal(et["despiecePeso"])*Decimal(cantidad);
		for etp in etapa:
			if et["despiece__material__id"] == etp["material_id"]:
				etapaRegistro = etp["id"]
				pesoRecibido += etp["cantidadAsignada"]
				pesoAsignado =  pesoRecibido - despiecePeso
		resultadoTotales = {"idEtapa":etapaRegistro, 
						"idMaterial":et["despiece__material__id"], 
						"nombre":et["despiece__material__nombre"],
						"despiecePeso":despiecePeso,
						"pesoRecibido":pesoRecibido,
						"pesoAsignado":pesoAsignado
					}
		pesoRecibido = 0
		pesoAsignado = 0
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
	etapaFuncion = Etapa.objects.filter(estatusEtapa=5).values_list('funcion_id', flat=True).distinct()
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
	orden = request.POST.get('orden', 0)
	idFuncion = request.POST.get('funcion', 0)
	etapa = Etapa.objects.values("apoyo__id",
											"apoyo__numero"
											).filter(estatusEtapa=5, funcion_id=idFuncion, idOrdenTrabajo=orden).values_list('apoyo_id', flat=True).distinct()
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

class HomeView(generic.ListView):
	template_name = 'control_acero/home.html'
	context_object_name = 'ultimos_cinco_productos'
	def get_queryset(self):
		return Material.objects.order_by('despiece')[:9]
	#context_object_name = 'ultimos_cinco_productos'
	#producto = get_object_or_404(Producto, pk=producto_id)
	#return render(request, template_name)