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
from django.db.models import Count, Sum, Q
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
from django.contrib.auth.models import User, Permission, Group
from django.template import RequestContext
from django.contrib.staticfiles.templatetags.staticfiles import static
import xlsxwriter
import StringIO
import uuid
import csv

logo = static('img/hs.png')

def loginUsuario(request):

	logout(request)
	username = password = ''
	if request.POST:
		username = request.POST['usuario']
		password = request.POST['clave']
        userIGH = Usuario.objects.using('auth_db').filter(usuario=username, clave=md5.new(password).hexdigest()).first()
        if userIGH:
            try:
                user = User.objects.get(username=userIGH.usuario)
            except User.DoesNotExist:
                user = User(username=userIGH.usuario, password=userIGH.clave, email=userIGH.correo, first_name=userIGH.nombre, last_name=userIGH.apaterno + ' ' + userIGH.amaterno)
                user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
				if user.is_active:
					login(request, user)
					current_user = request.user
					user_id = current_user.id
					getTallerAsignado(request, 0)
					getFrenteAsignado(request, 0)
					if current_user.is_superuser:
						url = '/control_acero/principal/'
					else:
						url = '/control_acero/perfil/'
					return HttpResponseRedirect(url)
	template_name = '/control_acero'
 	messages.error(request, 'Usuario y/o Password invalidos')
 	return HttpResponseRedirect(template_name)
 	
# def loginUsuario(request):
# 	logout(request)
# 	username = password = ''
# 	if request.POST:
# 		username = request.POST['usuario']
# 		password = request.POST['clave']

# 		user = authenticate(username=username, password=password)
# 		if user is not None:
# 			if user.is_active:
# 				login(request, user)
# 				current_user = request.user
# 				user_id = current_user.id
# 				getTallerAsignado(request, 0)
# 				url = '/control_acero/perfil/'
# 				return HttpResponseRedirect(url)
# 	template_name = '/control_acero'
#  	messages.error(request, 'Usuario y/o Password invalidos')
#  	return HttpResponseRedirect(template_name)

def fecha(request):
	array = {}
	mensaje = {}
	data = []

	today = datetime.now()
	dateFormat = today.strftime("%d/%m/%Y")
	#print dateFormat
	#mensaje = {"estatus":"ok", "folio":numFolio, "date":dateFormat}
	mensaje = {"date":dateFormat}
	array = mensaje
	return JsonResponse(array)

def getTallerAsignado(request, taller):
	taller = Taller.objects.filter(id = taller).order_by()
	if taller.exists():
		request.session['idTaller'] = taller[0].id
		request.session['nombreTaller'] = taller[0].nombre
		request.session['proveedorTaller'] = taller[0].identificacionFolio
		request.session['ubicacionTaller'] = taller[0].ubicacion
		request.session['responsableTaller'] = taller[0].responsable
		request.session['idfuncion']= taller[0].funcion_id
	else:
		request.session['idTaller'] = 0
		request.session['nombreTaller'] = 0
		request.session['proveedorTaller'] = 0
		request.session['ubicacionTaller'] = 0
		request.session['responsableTaller'] = 0
		request.session['idfuncion']= 0


def getFrenteAsignado(request, frente):
	frente = Frente.objects.filter(id = frente).order_by()
	if frente.exists():
		request.session['idFrente'] = frente[0].id
		request.session['nombreFrente'] = frente[0].nombre
		request.session['identificacionFrente'] = frente[0].identificacion
		request.session['ubicacionFrente'] = frente[0].ubicacion
		request.session['ideF'] = frente[0].ideFolio
	else:
		request.session['idFrente'] = 0
		request.session['nombreFrente'] = 0
		request.session['identificacionFrente'] = 0
		request.session['ubicacionFrente'] = 0
		request.session['ideF'] = 0

def logout_view(request):
	del request.session['idTaller']
	del	request.session['nombreTaller']
	del	request.session['proveedorTaller']
	del	request.session['ubicacionTaller']
	del	request.session['responsableTaller']
	del	request.session['idFrente']
	del	request.session['nombreFrente']
	del	request.session['identificacionFrente']
	del	request.session['ubicacionFrente']
	logout(request)
    	template_name = '/control_acero'
    	return HttpResponseRedirect(template_name)
######################################################
################VISTA DE LOS CATALOGOS################
######################################################
@login_required(login_url='/control_acero/usuario/login/')
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

@login_required(login_url='/control_acero/usuario/login/')
def usuariosEditView(request, pk):
	usuario = get_object_or_404(User, pk=pk)
	if request.method == "POST":
		# for key in request.POST:
		#     #print(key)
		#     value = request.POST[key]
		#     #print(value)
		form = UserForm(request.POST, instance=usuario)
		if(form.is_valid()):
			user = form.save(commit=False)
			user.save()
			#user.groups.add(Group.objects.get(name=user))
	else:
		user_grupos = usuario.groups.all()
		grupos = Group.objects.exclude(user__id = usuario.id)

		user_permisos = usuario.user_permissions.all()
		permisos = Permission.objects.exclude(user__id = usuario.id).filter(content_type_id=36)

	return render(request, 'control_acero/catalogos/usuarios/usuario_edit.html', {'user': usuario,'grupos': grupos,'user_grupos': user_grupos,'permisos': permisos,'user_permisos': user_permisos})

@login_required(login_url='/control_acero/usuario/login/')
def usuariosUpdateView(request, pk):
	usuario = get_object_or_404(User, pk=pk)
	permisos = request.POST.getlist('permisos[]')
	grupos = request.POST.getlist('grupos[]')
	first_name = request.POST['first_name']
	last_name = request.POST['last_name']
	email = request.POST['email']
	is_superuser = request.POST['is_superuser']
	superuser = 0 if is_superuser == "false" else 1
	is_active = request.POST['is_active']
	activo = 0 if is_active == "false" else 1
	usuario.first_name = first_name
	usuario.last_name = last_name
	usuario.email = email
	usuario.is_superuser = superuser
	usuario.is_active = activo
	usuario.save()
	usuario.user_permissions.clear()
	usuario.groups.clear()
	for grupo in grupos:
		usuario.groups.add(grupo)
	for permiso in permisos:
		usuario.user_permissions.add(permiso)

	return JsonResponse({'msj': 'Se modifico Correctamente el Usuario'})

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

@login_required(login_url='/control_acero/usuario/login/')
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
	return render(request,'control_acero/catalogos/apoyos/apoyo.html', {"apoyos": apoyos})

@login_required(login_url='/control_acero/usuario/login/')
def usuariosView(request):
	usuario_list = User.objects.all()
	paginator = Paginator(usuario_list, 10)
	page = request.GET.get('page')
	try:
		usuarios = paginator.page(page)
	except PageNotAnInteger:
		usuarios = paginator.page(1)
	except EmptyPage:
		usuarios = paginator.page(paginator.num_pages)
	return render(request,'control_acero/catalogos/usuarios/usuario.html', {"usuarios": usuarios})

@login_required(login_url='/control_acero/usuario/login/')
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

@login_required(login_url='/control_acero/usuario/login/')
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
			#print estatus
			#return render(request, 'control_acero/catalogos/apoyos/apoyo.html', {'form': form})
	else:
		form = ApoyoForm(instance=apoyo)
		
	return render(request, 'control_acero/catalogos/apoyos/apoyo_delete.html', {'form': form})

@login_required(login_url='/control_acero/usuario/login/')	
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
	return render(request,'control_acero/catalogos/elementos/elementos.html', {"elementos": elementos})

@login_required(login_url='/control_acero/usuario/login/')
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

@login_required(login_url='/control_acero/usuario/login/')
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
	
@login_required(login_url='/control_acero/usuario/login/')
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
	return render(request,'control_acero/catalogos/despieces/despiece.html', {"despieces": despieces})

@login_required(login_url='/control_acero/usuario/login/')
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

@login_required(login_url='/control_acero/usuario/login/')
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

@login_required(login_url='/control_acero/usuario/login/')
def materialesView(request):
	material_list = Material.objects.filter(estatus=1).order_by("numero");
	paginator = Paginator(material_list, 12)
	page = request.GET.get('page')
	try:
		materiales = paginator.page(page)
	except PageNotAnInteger:
		materiales = paginator.page(1)
	except EmptyPage:
		materiales = paginator.page(paginator.num_pages)
	return render(request,'control_acero/catalogos/materiales/material.html', {"materiales": materiales})

@login_required(login_url='/control_acero/usuario/login/')
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

@login_required(login_url='/control_acero/usuario/login/')
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

@login_required(login_url='/control_acero/usuario/login/')
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
	return render(request,'control_acero/catalogos/frentes/frente.html', {"frentes": frentes})

@login_required(login_url='/control_acero/usuario/login/')
def frentesNewView(request):
	if request.method == "POST":
		form = FrenteForm(request.POST)
		if(form.is_valid()):
			frente = form.save(commit=False)
			frente.save()
			form.save_m2m()
			#return render(request, 'control_acero/catalogos/apoyos/apoyo.html', {'form': form})
	else:
		form = FrenteForm()
		
	return render(request, 'control_acero/catalogos/frentes/frente_new.html', {'form': form})

@login_required(login_url='/control_acero/usuario/login/')
def frentesEditView(request, pk):
	frente = get_object_or_404(Frente, pk=pk)
	if request.method == "POST":
		form = FrenteForm(request.POST, instance=frente)
		if(form.is_valid()):
			frente = form.save(commit=False)
			frente.save()
			form.save_m2m()
			#return render(request, 'control_acero/catalogos/apoyos/apoyo.html', {'form': form})
	else:
		form = FrenteForm(instance=frente)
		
	return render(request, 'control_acero/catalogos/frentes/frente_edit.html', {'form': form})

@login_required(login_url='/control_acero/usuario/login/')
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
	return render(request,'control_acero/catalogos/funciones/funcion.html', {"funciones": funciones})

@login_required(login_url='/control_acero/usuario/login/')
def funcionesNewView(request):
	if request.method == "POST":
		form = FuncionForm(request.POST)
		#print form
		if(form.is_valid()):
			funcion = form.save(commit=False)
			funcion.save()
			#return render(request, 'control_acero/catalogos/apoyos/apoyo.html', {'form': form})
	else:
		form = FuncionForm()
		
	return render(request, 'control_acero/catalogos/funciones/funcion_new.html', {'form': form})

@login_required(login_url='/control_acero/usuario/login/')
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

@login_required(login_url='/control_acero/usuario/login/')
def talleresView(request):
	talleres_list = Taller.objects.values(
						"id",
						"nombre",
						"ubicacion",
						"identificacionFolio",
						"funcion__proveedor")\
					.filter(estatus=1)
	paginator = Paginator(talleres_list, 10)
	page = request.GET.get('page')
	try:
		talleres = paginator.page(page)
	except PageNotAnInteger:
		talleres = paginator.page(1)
	except EmptyPage:
		talleres = paginator.page(paginator.num_pages)
	return render(request,'control_acero/catalogos/talleres/taller.html', {"talleres": talleres})

@login_required(login_url='/control_acero/usuario/login/')
def talleresNewView(request):
	if request.method == "POST":
		form = TallerForm(request.POST)
		if(form.is_valid()):
			funcion = form.save(commit=False)
			funcion.save()
			form.save_m2m()
			#return render(request, 'control_acero/catalogos/apoyos/apoyo.html', {'form': form})
	else:
		form = TallerForm()
		
	return render(request, 'control_acero/catalogos/talleres/taller_new.html', {'form': form})

@login_required(login_url='/control_acero/usuario/login/')
def talleresEditView(request, pk):
	taller = get_object_or_404(Taller, pk=pk)
	if request.method == "POST":
		form = TallerForm(request.POST, instance=taller)
		if(form.is_valid()):
			taller = form.save(commit=False)
			taller.save()
			form.save_m2m()
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
	return render(request,'control_acero/catalogos/transportes/transporte.html', {"transportes": transportes})

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

@login_required(login_url='/control_acero/usuario/login/')
def movimientosView(request):

	movimientos_list = Bitacora.objects.values("id",
										"accion",
										"observacion",
										"estatus",
										"id_afectado",
										"fechaRegistro",
										"modulo__id",
										"modulo__descripcion",
										"user__id",
										"user__first_name",
										"user__last_name")\
								.filter(
										estatus = 1
										)\
								.order_by("id")

	paginator = Paginator(movimientos_list, 20)
	page = request.GET.get('page')
	try:
		movimientos = paginator.page(page)
	except PageNotAnInteger:
		movimientos = paginator.page(1)
	except EmptyPage:
		movimientos = paginator.page(paginator.num_pages)
	return render(request,'control_acero/catalogos/movimientos/movimiento.html', {"movimientos": movimientos})

def movimientosFecha(request):
	array = {}
	mensaje = {}
	data = []
	fecha = request.POST.get('fecha', '17/05/2016')
	
	fechaInicialFormat = datetime.strptime(fecha+" 00:00:00", '%d/%m/%Y %H:%M:%S')
	fechaFinalFormat = datetime.strptime(fecha+" 23:59:59", '%d/%m/%Y %H:%M:%S')
	movimientos = Bitacora.objects.values(
											"id",
											"accion",
											"observacion",
											"id_afectado",
											"fechaRegistro",
											"modulo__id",
											"modulo__descripcion",
											"user__id",
											"user__first_name",
											"user__last_name"
										)\
										.filter(		fechaRegistro__gte=fechaInicialFormat,
														fechaRegistro__lte=fechaFinalFormat,
														estatus=1)\
												.order_by("id")
	for m in movimientos:
		fecha = m['fechaRegistro'].strftime("%d/%m/%Y")
		respuesta={
			"id":m["id"],
			"accion":m["accion"],
			"observacion":m["observacion"],
			"id_afectado":m["id_afectado"],
			"fechaRegistro":fecha,
			"modulo__id":m["modulo__id"],
			"descripcion":m["modulo__descripcion"],
			"idUss":m["user__id"],
			"nombre":m["user__first_name"],
			"apellidos":m["user__last_name"]
		}
		data.append(respuesta)

	array["data"]=data

	return JsonResponse(array)

@login_required(login_url='/control_acero/usuario/login/')
def movimientosDetalleView(request, pk):
	folios=0
	movimiento = get_object_or_404(Bitacora, pk=pk)
	detalle = Bitacora.objects.values("id",
										"accion",
										"observacion",
										"id_afectado",
										"fechaRegistro",
										"modulo__id",
										"modulo__descripcion",
										"user__id",
										"user__first_name",
										"user__last_name")\
									.filter(id=movimiento.id);
	
	modulo = detalle[0]["modulo__id"]
	idAfectado = detalle[0]["id_afectado"]
	#print idAfectado
	if modulo == 1 or modulo == 6 :
		datos = Remision.objects.values("id",
									    "idOrden",
									    "remision",
									    "funcion__proveedor",
									    "remisiondetalle__folio",
									    "remisiondetalle__material__nombre",
									    "remisiondetalle__peso",
									    "remisiondetalle__longitud",
									    "pesoNeto",
									    "tallerAsignado__nombre")\
				.filter(id=idAfectado)
	if modulo == 2 or modulo == 7:
		folios = Salida.objects.values(
										"fechaRegistro",
										"apoyo__numero",
										"tallerAsignado__nombre",
										"frente__nombre",
										"elemento__nombre",
										"folio")\
				.filter(id=idAfectado)
		folio = folios[0]["folio"]
		datos = Salida.objects.values(
										"material__nombre",
										"cantidadAsignada")\
				.filter(folio=folio)
	if modulo== 3 or modulo==8:
		folios = Entrada.objects.values("folio",
										"elemento__nombre",
										"remision",
										"fechaRegistro",
										"apoyo__numero",
										"frente__nombre",
										"funcion__proveedor").filter(id=idAfectado)
		folio = folios[0]["folio"]
		datos = Entrada.objects.values("cantidadAsignada",
										"material__nombre",
										"cantidadReal",
										"entradadetalle__nomenclatura",
										"entradadetalle__longitud",
										"entradadetalle__piezas",
										"entradadetalle__calculado")\
				.filter(folio=folio)\
				.order_by("material_id")

		
	if modulo == 4 :
		datos = InventarioFisico.objects.values( "folio",
													"fechaRegistro",
													"tallerAsignado__nombre",
													"totalExistencias",
													"inventariofisicodetalle__pesoExistencia",
													"inventariofisicodetalle__pesoFisico",
													"inventariofisicodetalle__diferencia",
													"inventariofisicodetalle__material__nombre")\
		.filter(id=idAfectado)

	if modulo == 5 :
		datos = InventarioFisico.objects.values( "folio",
													"fechaRegistro",
													"tallerAsignado__nombre",
													"totalExistencias",
													"inventariofisicodetallecierre__pesoExistencia",
													"inventariofisicodetallecierre__pesoFisico",
													"inventariofisicodetallecierre__diferencia",
													 "inventariofisicodetallecierre__cantidadEntrada",
													 "inventariofisicodetallecierre__observacionEntrada",
													 "inventariofisicodetallecierre__cantidadSalida",
													 "inventariofisicodetallecierre__observacionSalida",
													 "inventariofisicodetallecierre__material__nombre")\
		.filter(id=idAfectado)
	
	template = 'control_acero/catalogos/movimientos/movimientoDetalle.html'
	
	return render(request, template, {"movimiento": movimiento, "detalles": detalle, "afectado" : datos, "modulo": modulo, "datos": folios})

@login_required(login_url='/control_acero/usuario/login/') 
def inventario(request):
	i = 0
	inventario_list = InventarioFisico.objects.filter(tallerAsignado_id=request.session["idTaller"], estatus=1)
	ajuste = InventarioFisico.objects.filter(tallerAsignado_id=request.session["idTaller"], estatusRegistro=0)
	for r in ajuste:
		i=i+1
	paginator = Paginator(inventario_list, 20)
	page = request.GET.get('page')
	try:
		inventario = paginator.page(page)
	except PageNotAnInteger:
		inventario = paginator.page(1)
	except EmptyPage:
		inventario = paginator.page(paginator.num_pages)
	return render(request,'control_acero/inventario/inventario.html', {"inventario": inventario, "ajuste" : i})

@login_required(login_url='/control_acero/usuario/login/')
def inventarioFisicoEditView(request, pk):
	inventario = get_object_or_404(InventarioFisico, pk=pk)
	inventarioDetalle = InventarioFisicoDetalle.objects.values("id",
														"pesoExistencia",
														"pesoFisico",
														"diferencia",
														"inventarioFisico_id",
														"material_id",
														"material__nombre").filter(inventarioFisico_id=inventario.id);
	inventarioDetalleCierre = InventarioFisicoDetalleCierre.objects.filter(inventarioFisico_id=inventario.id);
	template = 'control_acero/inventario/inventarioFisicoEdit.html'
	#inventario = InventarioFisico.objects.filter(id=pk, estatus=1)
	return render(request, template, {"inventario": inventario, "detalles": inventarioDetalle, "cierres": inventarioDetalleCierre})

@login_required(login_url='/control_acero/usuario/login/')
def inventarioFisicoCierreView(request):
	inventario = InventarioFisico.objects.all().filter(tallerAsignado_id=request.session["idTaller"],estatusRegistro=0).distinct()
	template = 'control_acero/inventario/inventarioFisicoCierre.html'
	idI = inventario[0].id
	totales = InventarioFisico.objects.all().filter(tallerAsignado_id=request.session["idTaller"],id=idI);
	return render(request, template, {"totales": totales})

@login_required(login_url='/control_acero/usuario/login/')
def inventarioFisicoCierreAjusteView(request):
	inr = InventarioFisico.objects.all().filter(tallerAsignado_id=request.session["idTaller"], estatusRegistro=0).order_by("-numConteo").order_by("-id")[:1]
	##print "AQUI"
	##print inr.query
	template = 'control_acero/inventario/inventarioFisicoCierreAjuste.html'
	idI = inr[0].id
	##print idI
	inventario = get_object_or_404(InventarioFisico, pk=idI)
	inventarioDetalle = InventarioFisicoDetalle.objects.values("id",
														"pesoExistencia",
														"pesoFisico",
														"diferencia",
														"inventarioFisico_id",
														"material_id",
														"material__nombre").filter(inventarioFisico_id=idI);
	template = 'control_acero/inventario/inventarioFisicoCierreAjuste.html'
	#inventario = InventarioFisico.objects.filter(id=pk, estatus=1)
	return render(request, template, {"inventario": inventario, "detalles": inventarioDetalle})
######################################################	
def inventarioFisicoCierreDetalle(request):
	array = {}
	mensaje = {}
	data = []
	data2 = []
	idInventario = request.GET.get('idInventario')
	inventario = InventarioFisico.objects.all().filter(tallerAsignado_id=request.session["idTaller"],id=idInventario).order_by("id")
	for i in inventario:
		resultado={
				"id":i.id,
				"folio":i.folio,
				"fechaR":i.fechaRegistro				
			}
		data.append(resultado)
		detalle = InventarioFisicoDetalle.objects.values(
												"id",
												"inventarioFisico_id",
												"material__nombre",
												"material_id",
												"pesoExistencia",
												"pesoFisico").filter(inventarioFisico_id=idInventario, estatus=1).distinct().order_by("inventarioFisico_id").order_by("material_id")
		
		for d in detalle :
			resultado2={
				"id":d["id"],
				"idInventario":d["inventarioFisico_id"],
				"material": d["material__nombre"],
				"idMaterial": d["material_id"],
				"pesoExistencia": d["pesoExistencia"],
				"pesoFisico":d["pesoFisico"]
			}
			
			data2.append(resultado2)
	array["data"]=data
	array["detalle"]=data2
	
	return JsonResponse(array)

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
	frente = request.POST.get('frente', 0)

	apoyos = Apoyo.objects.all()\
								.filter(frente_id=frente,
										estatus = 1
										)\
								.order_by("id")
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
	funcion = request.POST.get('funcion', 0)
	fechaRemision = request.POST.get('fechaRemision', 0)
	remision = request.POST.get('remision', 0)
	pesoBruto = request.POST.get('pesoBruto', 0)
	pesoTara = request.POST.get('pesoTara', 0)
	pesoNeto = request.POST.get('pesoNeto', 0)
	observacion = request.POST.get('observacion',' ')
	respuesta = request.POST.get('json')
	json_object = json.loads(respuesta)
	p = Remision.objects\
				.create(
						idOrden=idOrden,
						remision=remision,
						funcion_id=funcion,
						pesoBruto=pesoBruto,
						pesoTara=pesoTara,
						pesoNeto=pesoNeto,
						observacion=observacion,
						fechaRemision=datetime.strptime(fechaRemision, '%d/%m/%Y'),
						estatus=1,
						tallerAsignado_id=request.session['idTaller']
						)
	bitacora = Bitacora.objects.create(accion="Inserción", id_afectado=p.pk, observacion="El id guardado es de la remisión", estatus=1, modulo_id=1, user_id=request.user.id)
	folio = RemisionDetalle.objects.all().filter(remision__tallerAsignado_id=request.session["idTaller"]).order_by("-numFolio")[:1]
	if folio.exists():
		numFolio = folio[0].numFolio
	numFolioInt = int(numFolio)+1
	numFolio = "%03d" % (numFolioInt,)
	ident= request.session["proveedorTaller"]
	numFolio = "RMH-"+ident+"-"+numFolio
	numFolio = numFolio.encode('utf-8')
	#print numFolio
	for data in json_object:
		datos = data["data"]
		splitData = datos.split("|")
		apoyo = splitData[0]
		elemento = splitData[1]
		idMaterial = splitData[2]
		cantidadMaterial= splitData[3]
		pesoMaterial = splitData[4]
		longitud = splitData[5]
		tipo =splitData[6]
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
									numFolio = numFolioInt,
									estatusTipo =tipo
									)
		ird = InventarioRemisionDetalle.objects\
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
	mailHtml(request, numFolioInt)
	#print array
	return JsonResponse(array)

def elementoMaterial(request):
	array = {}
	mensaje = {}
	data = []
	material = request.POST.get('material', 0)
	if material > 0:
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
											'factor__pi').filter(id=material).order_by("numero")
	else:
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
										'factor__pi').filter().order_by("numero")
	##print elemento.query
	for e in elemento:
		diametro = e['diametro']
		pva = e['factor__pva']
		factorPulgada = e['factor__factorPulgada']
		pi = e['factor__pi']
		diametroMetro = diametro / 1000
		factorCalculado = ((pi * diametroMetro * diametroMetro) / 4) * pva
		#print diametroMetro
		factorCalculadoDecimal = "%.3f" % factorCalculado
		#print factorCalculadoDecimal 
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
	remisionDetalles = InventarioRemisionDetalle.objects\
						.values(
								'material_id',
								'material__nombre'
								)\
						.annotate(pesoMaterial = Sum('peso'))\
						.annotate(cantidadMaterial = Sum('cantidad'))\
						.filter(peso__gt = 0, remision__tallerAsignado_id = request.session["idTaller"], estatus=1)\
						.order_by('material_id')
	##print remisionDetalles.query
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
	htmlMail = request.POST.get('htmlMail', 0)
	reposicion = request.POST.get('reposicion', 0)
	respuesta = request.POST.get('json')
	jsonDataInfo = json.loads(respuesta)
	numFolio = 0
	array = {}
	mensaje = {}
	data = []
	totalAsignado = 0
	totalAsignadoResta = 0
	inventarioPeso = 0
	cantidadRestar = 0
	cantidadSobrante = 0
	var = 0
	inventarioId = 0
	irdpeso = 0
	folio = Salida.objects.all().filter(estatusEtapa = 1, tallerAsignado_id = request.session["idTaller"]).order_by("-numFolio")[:1]
	if folio.exists():
		numFolio = folio[0].numFolio
	numFolioInt = int(numFolio)+1
	numFolio = "%03d" % (numFolioInt,)
	ident= request.session["proveedorTaller"]
	numFolio = "SMH-"+ident+"-"+numFolio
	numFolio = numFolio.encode('utf-8')
	
	for jsonData in jsonDataInfo:
		material = jsonData["material"]
		cantidadReal = jsonData["cantidadReal"]
		cantidadAsignada = jsonData["cantidadAsignada"]
		totalAsignado = cantidadAsignada
		remisionDetallesTotales = InventarioRemisionDetalle.objects\
							.values(
									'material_id',
									'material__nombre'
									)\
							.annotate(pesoMaterial = Sum('peso'))\
							.annotate(cantidadMaterial = Sum('cantidad'))\
							.filter(material_id = material, remision__tallerAsignado_id = request.session["idTaller"],estatus=1).order_by("material_id")
		for remisionDetallesTotal in remisionDetallesTotales:
			if Decimal(remisionDetallesTotal["pesoMaterial"]) >= Decimal(totalAsignado):
				inventarioRemisionDetalles = InventarioRemisionDetalle.objects.all()\
												.filter(
														material_id = material,
														estatusTotalizado = 1,
														estatus=1,
														remision__tallerAsignado_id = request.session["idTaller"])\
												.order_by("id").order_by("material_id")
				for inventarioRemisionDetalle in inventarioRemisionDetalles:
					inventarioId = inventarioRemisionDetalle.id
					irdpeso = inventarioRemisionDetalle.peso
					peso=Decimal(totalAsignado)
					if Decimal(irdpeso) <= Decimal(totalAsignado):
						
						totalAsignado = Decimal(totalAsignado) - Decimal(irdpeso)
						descuento = DescuentoSalida.objects\
												.create(
														pesoSalida = peso,
														pesoRemision = irdpeso,
														resta = totalAsignado,
														inventarioRemisionDetalle_id =inventarioId
														)
						
						
						InventarioRemisionDetalle.objects.filter(id=inventarioId).update(peso=0, estatusTotalizado = 0)
						continue

					if Decimal(irdpeso) > Decimal(totalAsignado) and Decimal(totalAsignado) != 0:
						cantidadRestar = Decimal(irdpeso) - Decimal(totalAsignado)
						descuento = DescuentoSalida.objects\
												.create(
														pesoSalida = totalAsignado,
														pesoRemision = irdpeso,
														resta = cantidadRestar,
														inventarioRemisionDetalle_id =inventarioId
														)
						if cantidadRestar >= 0:
							totalAsignado = 0;
												
						InventarioRemisionDetalle.objects.filter(id=inventarioId).update(peso=cantidadRestar)
			else:
				mensaje = {"estatus":"ok", "mensaje":"No puede exceder el peso existente"}
				array = mensaje
				return JsonResponse(array)
		salida = Salida.objects\
						.create(
								apoyo_id = apoyo,
								elemento_id = elemento,
								material_id = material,
								frente_id = frente,
								estatusReposicion=reposicion,
								cantidadReal = cantidadReal,
								cantidadAsignada = cantidadAsignada,
								estatusEtapa = 1,
								folio = numFolio,
								numFolio = numFolioInt,
								tallerAsignado_id = request.session["idTaller"]
								)
		bitacora = Bitacora.objects.create(accion="Inserción", id_afectado=salida.pk, observacion="El id guardado es de la salida", estatus=1, modulo_id=2, user_id=request.user.id)
		DescuentoSalida.objects.filter(estatusSalida=0).update(salida_id=salida.pk, estatusSalida=1)
		inventarioSalida = InventarioSalida.objects\
						.create(
								apoyo_id = apoyo,
								elemento_id = elemento,
								material_id = material,
								frente_id = frente,
								cantidadReal = cantidadReal,
								cantidadAsignada = cantidadAsignada,
								estatusEtapa = 1,
								folio = numFolio,
								numFolio = numFolioInt,
								tallerAsignado_id = request.session["idTaller"]
								)


	mensaje = {"estatus":"ok", "mensaje":"Salida de Material Exitosa. Folio: "+numFolio, "folio":numFolio}
	array = mensaje
	mailHtmlSH(request, numFolioInt)
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
	folio = request.POST.get('folio', 1)
	cantidadReal = 0
	salidas = InventarioSalida.objects \
						.values(
								'material_id',
								'material__nombre',
								'material__diametro',
								'apoyo__id',
								'apoyo__numero',
								'elemento__id',
								'elemento__nombre'
								)\
						.annotate(cantidadAsignada = Sum('cantidadAsignada')) \
						.filter(numFolio = folio, frente_id = request.session["idFrente"], cantidadAsignada__gt=0, estatus=1) \
						.order_by('material_id')
	for salida in salidas:
		resultado = {
						"id":salida["material_id"],
						"materialNombre":salida["material__nombre"],
						"materialDiametro":salida["material__diametro"],
						"cantidadAsignada":salida["cantidadAsignada"],
						"apoyoId":salida["apoyo__id"],
						"apoyoNumero":salida["apoyo__numero"],
						"elementoId":salida["elemento__id"],
						"elementoNombre":salida["elemento__nombre"]
					}
		data.append(resultado)

	array["data"]=data
	return JsonResponse(array)

def entradaArmadoSave(request):
	remision = request.POST.get('remision', 0)
	apoyo = request.POST.get('apoyo', 0)
	elemento = request.POST.get('elemento', 0)
	funcion = request.POST.get('funcion', 0)
	folioSalida = request.POST.get('folio', 0)
	folioText= request.POST.get('folioText', 0)
	htmlMail = request.POST.get('htmlMail', 0)
	htmlMailFaltante = request.POST.get('htmlMailFaltante', 0)
	respuesta = request.POST.get('json')
	jsonDataInfo = json.loads(respuesta)
	respuestaFaltante = request.POST.get('jsonFaltante')
	jsonDataInfoFaltante = json.loads(respuestaFaltante)
	numFolio = 0
	array = {}
	mensaje = {}
	data = []
	cursor = connection.cursor()
	folio = Entrada.objects.all().filter(estatusEtapa = 1, frente_id = request.session["idFrente"]).order_by("-numFolio")[:1]
	if folio.exists():
		numFolio = folio[0].numFolio
	numFolioInt = int(numFolio)+1
	numFolio = "%03d" % (numFolioInt,)
	ident= request.session["ideF"]
	numFolio = "EMA-"+ident+"-"+numFolio
	numFolio = numFolio.encode('utf-8')
	
	for jsonData in jsonDataInfo:
		material = jsonData["material"]
		cantidadReal = jsonData["cantidadReal"]
		cantidadAsignada = jsonData["cantidadAsignada"]
		bandera = jsonData["bandera"]
		totalAsignado = cantidadAsignada
		inventarioSalidas = InventarioSalida.objects.all()\
										.filter(material_id = material, estatusTotalizado = 1, frente_id = request.session["idFrente"], estatus=1)
		for inventarioSalida in inventarioSalidas:
			inventarioId = inventarioSalida.id
			irdpeso = inventarioSalida.cantidadAsignada

			if Decimal(irdpeso) <= Decimal(totalAsignado):
				totalAsignado = Decimal(totalAsignado) - Decimal(irdpeso)
				InventarioSalida.objects.filter(id=inventarioId, estatus=1).update(cantidadAsignada=0, estatusTotalizado = 0)
				continue

			if Decimal(irdpeso) > Decimal(totalAsignado):
				cantidadRestar = Decimal(irdpeso) - Decimal(totalAsignado)
				InventarioSalida.objects.filter(id=inventarioId, estatus=1).update(cantidadAsignada=cantidadRestar)

		entrada = Entrada.objects\
						.create(
								remision = remision,
								elemento_id = elemento,
								apoyo_id = apoyo,
								material_id = material,
								funcion_id = funcion,
								folioSalida= folioText,
								cantidadReal = cantidadReal,
								cantidadAsignada = cantidadAsignada,
								folio = numFolio,
								numFolio = numFolioInt,
								frente_id = request.session["idFrente"]
								)
		bitacora = Bitacora.objects.create(accion="Inserción", id_afectado=entrada.pk, observacion="El id guardado es de la entrada en frente de trabajo", estatus=1, modulo_id=3, user_id=request.user.id)
	for jsonDataFaltante in jsonDataInfoFaltante:
		materialF = jsonDataFaltante["material"]
		cantidadRealF = jsonDataFaltante["cantidadReal"]
		cantidadAsignadaF = jsonDataFaltante["cantidadAsignada"]
		nomenclatura = jsonDataFaltante["nomenclatura"]
		longitud = jsonDataFaltante["longitud"]
		piezas = jsonDataFaltante["piezas"]
		calculado = jsonDataFaltante["calculadoReal"]
		bandera = jsonDataFaltante["bandera"]
		entradaFaltante = Entrada.objects\
						.create(
								remision = remision,
								elemento_id = elemento,
								apoyo_id = apoyo,
								material_id = materialF,
								funcion_id = funcion,
								folioSalida =folioText,
								cantidadReal = cantidadRealF,
								cantidadAsignada = cantidadAsignadaF,
								folio = numFolio,
								numFolio = numFolioInt,
								frente_id = request.session["idFrente"]
								)
		try:
			cursor.execute("UPDATE control_acero_inventariosalida\
								SET cantidadAsignada = 0,\
									estatusTotalizado = 0\
								WHERE numFolio = %s\
								AND material_id = %s", [folioSalida,materialF]);
		finally:
			print "Se actualizo"

		if bandera == 1:
			entradaDetalle = EntradaDetalle.objects\
							.create(
									nomenclatura = nomenclatura,
									longitud = longitud,
									piezas = piezas,
									calculado = calculado,
									entrada_id = entradaFaltante.id
									)

	mensaje = {"estatus":"ok", "mensaje":"Entrada de Material Exitosa. Folio: "+numFolio, "folio":numFolio}
	array = mensaje
	
	mailHtmlEA(request,numFolioInt)
	return JsonResponse(array)

def inventarioFisicoSave(request):
	array = {}
	mensaje = {}
	data = []
	numFolio = 0
	flag = 0
	folioEntrada = request.POST.get('folioEntrada')
	pesoEntrada = request.POST.get('pesoEntrada')
	folioSalida = request.POST.get('folioSalida')
	pesoSalida = request.POST.get('pesoSalida')
	totalexistencia = request.POST.get('totalexistencia')
	estatus = request.POST.get('estatus')
	idInvF=0
	observacion = request.POST.get('jsonObservaciones')
	real =request.POST.get('jsonReal')

	conteo = 1
	estatus = 1
	conteoInt = 0
	numFolioInt = 0
	#folio---
	folio = InventarioFisico.objects.all().filter(tallerAsignado_id = request.session["idTaller"]).order_by("-numFolio").order_by("-id")[:1]
	p = request.session["proveedorTaller"]	
	if folio.exists():
		numFolio = folio[0].numFolio
		conteo = folio[0].numConteo
		estatus = folio[0].estatusRegistro
	if estatus == 0 and conteo <= 2:
		conteo = int(conteo) + 1
		numFolioInt = int(numFolio)
	else:
		conteo = 1
		numFolioInt = int(numFolio)+1
	conteoInt = str(conteo)
	numFolio = "%03d" % (numFolioInt,)
	numFolio = "LIF-"+p+"-"+numFolio+"-"+conteoInt
	numFolio = numFolio.encode('utf-8')
	

	inventarioFisico = InventarioFisico.objects\
		.create(
				noEntradas = folioEntrada,
				totalEntradas = pesoEntrada,
				noSalidas = folioSalida,
				totalSalidas = pesoSalida,
				totalExistencias = totalexistencia,
				folio = numFolio,
				numFolio = numFolioInt,
				tallerAsignado_id = request.session["idTaller"],
				numConteo=conteo
				)
	bitacora = Bitacora.objects.create(accion="Inserción", id_afectado=inventarioFisico.pk, observacion="El id guardado es del inventario fisico", estatus=1, modulo_id=4, user_id=request.user.id)
	idFolioFisico=inventarioFisico.pk;
	json_observaciones = json.loads(observacion)
		
	for r in json_observaciones:
		
		material = r["id"]
		peso = r["peso"]
		longitud = r["longitud"]
		piezas = r["piezas"]
		referencia = r["observacion"]
		tipo = r["tipo"]
		if peso!=0:
			inventarioFisicoC = InventarioFisicoDetalleCompleto.objects\
										.create(
												material_id = material,
												peso = peso,
												longitud = longitud,
												piezas = piezas,
												referencia = referencia,
												estatusTipoV = tipo
												)
	inventariocompleto= InventarioFisicoDetalleCompleto.objects\
							.values("material__id",
									"material__nombre")\
							.annotate(pesomaterial = Sum("peso"))\
							.filter(estatusDetalle=0)\
							.order_by("material__id")

	json_reales = json.loads(real)
	flag=0;

	for real in json_reales:
		#print real
		flag=0
		idR = real["id"]
		pesoR = real["pesosistema"]
		
		
		for ic in inventariocompleto:
			idM= ic["material__id"]
			pesoM = ic["pesomaterial"]
			nombre = ic["material__nombre"]
			
			
			if idM == idR:
				
				diferencia=float(pesoM)-float(pesoR) 
				
				inventarioDetalle = InventarioFisicoDetalle.objects\
									.create(
										pesoExistencia = pesoR,
										pesoFisico = pesoM,
										diferencia = diferencia,
										material_id= idR,
										inventarioFisico_id = inventarioFisico.pk,
									)
				InventarioFisicoDetalleCompleto.objects.filter(estatusDetalle = 0).update(InventarioFisicoDetalle_id = inventarioDetalle.pk, estatusDetalle = 1)
				resultado = {
						"id":idM,
						"nombre":nombre,
						"existencia":pesoR,
						"fisico":pesoM,
						"diferencia":diferencia
						}
				data.append(resultado)
				flag=1
			
		if flag==0:
			
			diferencia=0-float(pesoR)
			material = Material.objects.values("nombre").filter(id=idR);	
			for m in material:
				nombre=m["nombre"]
			
			inventarioD = InventarioFisicoDetalle.objects\
									.create(
										pesoExistencia = pesoR,
										pesoFisico = 0,
										diferencia = diferencia,
										material_id= idR,
										inventarioFisico_id = inventarioFisico.pk,
									)
				#InventarioFisicoDetalleCompleto.objects.filter(material_id = idR).update(InventarioFisicoDetalle_id = inventarioD.pk, estatusDetalle = 1)
			resultado = {
						"id":idR,
						"nombre":nombre,
						"existencia":pesoR,
						"fisico":0,
						"diferencia":diferencia
						}
			data.append(resultado)
		
	#print "***++"
	#print conteo
	margen = 0
	error = 0
	idIF = 0
	estatusCierre = 0
	porcentaje= Taller.objects.values(
											"id",
											"funcion__porcentajeMaximo")\
											.filter(id=request.session["idTaller"])

	porcentajeMaximo= porcentaje[0]["funcion__porcentajeMaximo"]	
	print porcentajeMaximo		


	if conteo == 2:
		detalle = InventarioFisicoDetalle.objects.values(
														"id",
														"pesoExistencia",
														"pesoFisico",
														"diferencia",
														"inventarioFisico_id",
														"material_id",
														"material__nombre",
													)\
												.filter(inventarioFisico__estatusRegistro=0)\
												.order_by("inventarioFisico_id")

		
		##print detalle		
		for d in detalle:
			#print d["inventarioFisico_id"]
			#print d["pesoExistencia"]
			#print d["pesoFisico"]
			idIF=d["inventarioFisico_id"]
			fisico = int(d["pesoFisico"])
			margen = int(d["pesoExistencia"]) * porcentajeMaximo
			#print margen
			margenNeg = int(d["pesoExistencia"]) - margen
			
			margenPos = int(d["pesoExistencia"]) + margen
			print margenPos
			print margenNeg
			if  margenNeg <= fisico and fisico <= margenPos:
				print "si entra en el margen "
			else: 
				print "NO entra en el margen "
				error = 1
		if error == 0 :
			#print "cierre automatico"
			RemisionDetalle.objects.filter(estatusInventario=0).update(estatusInventario=1, folioInventario=idIF)
			InventarioRemisionDetalle.objects.filter(estatusInventario=0).update(estatusInventario=1,folioInventario=idIF)
			Salida.objects.filter(estatusInventario=0).update(estatusInventario=1,folioInventario=idIF)
			InventarioSalida.objects.filter(estatusInventario=0).update(estatusInventario=1,folioInventario=idIF)

			InventarioFisico.objects.filter(estatusRegistro=0).update(estatusRegistro=1, estatusCierre=1)#COLOCAR--- PARA GUARDAR REGISTRO DE MOVIMIENTO POR Inventario
			estatusCierre = 1

	if conteo == 3:
		detalle = InventarioFisicoDetalle.objects.values(
														"id",
														"pesoExistencia",
														"pesoFisico",
														"diferencia",
														"inventarioFisico_id",
														"material_id",
														"material__nombre"
													)\
												.filter(inventarioFisico__estatusRegistro=0, inventarioFisico_id = inventarioFisico.pk)\
												.order_by("inventarioFisico_id")


					
		##print detalle		
		for d in detalle:
			#print d["inventarioFisico_id"]
			#print d["pesoExistencia"]
			#print d["pesoFisico"]
			idIF=d["inventarioFisico_id"]
			fisico = int(d["pesoFisico"])
			margen = int(d["pesoExistencia"]) * porcentajeMaximo
			print margen
			margenNeg = int(d["pesoExistencia"]) - margen
			
			margenPos = int(d["pesoExistencia"]) + margen
			print margenPos
			print margenNeg
			if  margenNeg <= fisico and fisico <= margenPos:
				print "si entra en el margen "
			else: 
				print "NO entra en el margen "
				error = 1
		if error == 0 :
			#print "cierre automatico"
			RemisionDetalle.objects.filter(estatusInventario=0).update(estatusInventario=1, folioInventario=idIF)
			InventarioRemisionDetalle.objects.filter(estatusInventario=0).update(estatusInventario=1,folioInventario=idIF)
			Salida.objects.filter(estatusInventario=0).update(estatusInventario=1,folioInventario=idIF)
			InventarioSalida.objects.filter(estatusInventario=0).update(estatusInventario=1,folioInventario=idIF)

			InventarioFisico.objects.filter(estatusRegistro=0).update(estatusRegistro=1)#COLOCAR--- PARA GUARDAR REGISTRO DE MOVIMIENTO POR Inventario
			estatusCierre = 1
		else:
			#print "3er inventario"
			idInvF=inventarioFisico.pk

	mensaje = {"estatus":"ok", "mensaje":"Entrada de Material Exitosa. Folio: "+numFolio, "folio":numFolio, "estatusCierre": estatusCierre, "inventarioAjuste": idInvF}
	array = mensaje
	array["data"]=data
	mailHtmlIF(request,idFolioFisico)
	return JsonResponse(array)

def foliosMostrar(request):
	modulo = request.POST.get('modulo', 0)
	numFolio = 0
	array = {}
	mensaje = {}
	data = []
	today = datetime.now()
	dateFormat = today.strftime("%d/%m/%Y")

	if int(modulo) == 1:
		folio = RemisionDetalle.objects.all().filter(remision__tallerAsignado_id = request.session["idTaller"]).order_by("-numFolio")[:1]
		p = request.session["proveedorTaller"]
		if folio.exists():
			numFolio = folio[0].numFolio
		numFolioInt = int(numFolio)+1
		numFolio = "%03d" % (numFolioInt,)
		numFolio = "RMH-"+p+"-"+numFolio
		#print request.session["proveedorTaller"]
		#print request.session['idfuncion']
	if int(modulo) == 2:
		folio = Salida.objects.all().filter(estatusEtapa = 1, tallerAsignado_id = request.session["idTaller"]).order_by("-numFolio")[:1]
		p = request.session["proveedorTaller"]
		if folio.exists():
			numFolio = folio[0].numFolio
		numFolioInt = int(numFolio)+1
		numFolio = "%03d" % (numFolioInt,)
		numFolio = "SMH-"+p+"-"+numFolio
	if int(modulo) == 3:
		folio = Entrada.objects.all().filter(estatusEtapa = 1, frente_id = request.session["idFrente"]).order_by("-numFolio")[:1]
		p=request.session["ideF"]
		if folio.exists():
			numFolio = folio[0].numFolio
		numFolioInt = int(numFolio)+1
		numFolio = "%03d" % (numFolioInt,)
		numFolio = "EMA-"+p+"-"+numFolio
	if int(modulo) == 4:
		conteo = 1
		estatus = 1
		conteoInt = 0
		numFolioInt = 1
		folio = InventarioFisico.objects.all().filter(tallerAsignado_id = request.session["idTaller"]).order_by("-numFolio").order_by("-id")[:1]
		p = request.session["proveedorTaller"]	
		##print folio.query
		if folio.exists():
			numFolio = folio[0].numFolio
			conteo = folio[0].numConteo
			estatus = folio[0].estatusRegistro
			#print conteo

		if estatus == 0 and conteo <=2:
			conteo = int(conteo) + 1
			numFolioInt = int(numFolio)
			#print "aqui"
		else:
			conteo = 1
			numFolioInt = int(numFolio)+1
		conteoInt = str(conteo)
		#print conteo
		numFolio = "%03d" % (numFolioInt,)
		numFolio = "LIF-"+p+"-"+numFolio+"-"+conteoInt
	if int(modulo) == 5:
		#print modulo
		folio = InventarioFisicoDetalleCierre.objects.all().filter(tallerAsignado_id = request.session["idTaller"]).order_by("-numFolio")[:1]
		p = request.session["proveedorTaller"]
		if folio.exists():
			numFolio = folio[0].numFolio
		numFolioInt = int(numFolio)+1
		numFolio = "%03d" % (numFolioInt,)
		numFolio = "IFA-"+p+"-"+numFolio

	mensaje = {"estatus":"ok", "folio":numFolio, "date":dateFormat}
	#mensaje = {"estatus":"ok", "folio":numFolio}
	#print mensaje
	array = mensaje
	return JsonResponse(array)

def foliosSalidaHabilitado(request):
	array = {}
	mensaje = {}
	data = []
	salidaFolios = InventarioSalida.objects.values('folio', 'numFolio', 'apoyo__numero', 'elemento__nombre').distinct().filter(frente_id=request.session['idFrente'])
	for salidaFolio in salidaFolios:
		validacionAsignado = InventarioSalida.objects.filter(numFolio=salidaFolio["numFolio"]).aggregate(Sum('cantidadAsignada'))
		validacionAsign = validacionAsignado["cantidadAsignada__sum"]
		if Decimal(validacionAsign) > 0:
			resultado = {
							"numFolio":salidaFolio["numFolio"],
							"folio":salidaFolio["folio"],
							"apoyo":salidaFolio["apoyo__numero"],
							"elemento":salidaFolio["elemento__nombre"]
						}
			data.append(resultado)
	array["data"]=data
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
def perfilView(request):
	current_user = request.user
	user_id = current_user.id
	talleres = Taller.objects.all().filter(user__id = user_id).order_by("nombre")
	frentes = Frente.objects.all().filter(user__id = user_id).order_by("nombre")
	return render_to_response('control_acero/perfil.html', RequestContext(request, {"talleres": talleres, "frentes": frentes}))

@login_required(login_url='/control_acero/usuario/login/')
def principalView(request):
	if request.method == "POST":
		perfil = request.POST.get('perfil', 0)
		taller = request.POST.get('taller', 0)
		frente = request.POST.get('frente', 0)
		if int(perfil) == 1:
			if int(taller) == 0:
				template_name = '/control_acero/perfil'
			 	messages.error(request, 'Debes Elegir un Perfil Taller de Habilitado')
			 	return HttpResponseRedirect(template_name)
		if int(perfil) == 2:
			if int(frente) == 0:
				template_name = '/control_acero/perfil'
			 	messages.error(request, 'Debes Elegir un Frente de Trabajo')
			 	return HttpResponseRedirect(template_name)
		getTallerAsignado(request, taller)
		getFrenteAsignado(request, frente)
	template = 'control_acero/principal.html'
	return render(request, template)

@login_required(login_url='/control_acero/usuario/login/')
def recepcionMaterialView(request):
	template = 'control_acero/material/recepcion_material_view.html'
	return render(request, template)

@login_required(login_url='/control_acero/usuario/login/')
def salidaHabilitadoView(request):
	template = 'control_acero/material/salida_habilitado_view.html'
	return render(request, template)
@login_required(login_url='/control_acero/usuario/login/')
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
	##print etapa.query
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
	##print elementoRelacion.query
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
	##print etapa.query
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
	#print etapa
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


def comboFuncionGeneral(request):
	array = {}
	mensaje = {}
	data = []

	funciones = Funcion.objects.all()\
								.filter(
										estatus = 1
										)\
								.order_by("tipo")
	for funcion in funciones:
		resultado = {
						"id":funcion.id,
						"tipo":funcion.tipo,
						"proveedor":funcion.proveedor
					}
		data.append(resultado)
	array["data"]=data
	return JsonResponse(array)

def comboTaller(request):
	array = {}
	mensaje = {}
	data = []

	f = request.POST.get('funcion', 0)
	
	talleres = Taller.objects.all()\
								.filter(
										funcion_id = f,
										funcion__tipo=2,
										estatus = 1
										)\
								.order_by("funcion_id")
	##print talleres.query
	for taller in talleres:
		resultado = {
						"id":taller.id,
						"nombre":taller.nombre
					}
		data.append(resultado)
	array["data"]=data
	return JsonResponse(array)

def comboTallerG(request):
	array = {}
	mensaje = {}
	data = []

	talleres = Taller.objects.all()\
								.filter(
										estatus = 1
										)\
								.order_by("funcion_id")
	##print talleres.query
	for taller in talleres:
		resultado = {
						"id":taller.id,
						"nombre":taller.nombre
					}
		data.append(resultado)
	array["data"]=data
	return JsonResponse(array)	

@login_required(login_url='/control_acero/usuario/login/')	
def reporteView(request):
	template = 'control_acero/reportes/reporte.html'
	return render(request, template)

def reporteConsulta(request):
	array = {}
	mensaje = {}
	data = []
	dataEn = []
	totales = []
	totalesS = []

	idFuncion = request.POST.get('funcion', 0)
	idTaller = request.POST.get('taller', 0)
	idFrente = request.POST.get('frente', 18)
	tipo =request.POST.get('tipo',3)
	excel = request.POST.get('excel',0)
	inventario = request.POST.get('inventario',0)

	fechaInicial = request.POST.get('fechai', '17/05/2016')
	fechaFinal = request.POST.get('fechaf', '14/06/2016')
	fechaInicialFormat = datetime.strptime(fechaInicial+" 00:00:00", '%d/%m/%Y %H:%M:%S')
	fechaFinalFormat = datetime.strptime(fechaFinal+" 23:59:59", '%d/%m/%Y %H:%M:%S')

	if idFuncion!='0' and idTaller=='0' and idFrente=='0' and tipo=='2' and inventario=='1':
		#print "Inventario Fisico"
		datos= InventarioFisico.objects.values(
												'id',
												'folio',
												'fechaRegistro',
												'tallerAsignado__nombre',
												'tallerAsignado__funcion__proveedor',
												'inventariofisicodetalle__pesoExistencia',
												'inventariofisicodetalle__pesoFisico',
												'inventariofisicodetalle__diferencia',
												'inventariofisicodetalle__material__nombre'
												).filter(tallerAsignado__funcion__id=idFuncion,
														fechaRegistro__gte=fechaInicialFormat,
														fechaRegistro__lte=fechaFinalFormat,
														estatus=1)\
												.order_by("folio")
		for x in datos:
			fecha = x['fechaRegistro'].strftime("%d/%m/%Y")
			resultado = {
				"value":0,
				"excel":0,
				"id":x['id'],
				"folio":x['folio'],
				"proveedor":x['tallerAsignado__funcion__proveedor'],
				"fechaR":fecha,
				"taller":x['tallerAsignado__nombre'],
				"existencia":x['inventariofisicodetalle__pesoExistencia'],
				"fisico":x['inventariofisicodetalle__pesoFisico'],
				"diferencia":x['inventariofisicodetalle__diferencia'],
				"material":x['inventariofisicodetalle__material__nombre']
			}

			data.append(resultado)
		array["data"]=data
		if int(excel) == 1:
			#print "Inventario Excel"
			filename = excelReportesEntrada(request,array)
			return JsonResponse({"filename": filename})

		return JsonResponse(array)


	if idFuncion!='0' and idTaller=='0' and idFrente=='0' and tipo=='1' and inventario=='0':

		#print "Fabricante"

		total = RemisionDetalle.objects.values(	'material__id',
												'material__nombre'		
												).annotate(pesoMaterial = Sum('peso'))\
												.filter(remision__funcion__id =idFuncion,
														fechaRegistro__gte=fechaInicialFormat,
														fechaRegistro__lte=fechaFinalFormat,
														estatus=1)\
												.order_by("material__id")

		##print total.query
		for x in total:
			resultado = {
					"id":x['material__id'],
					"nombre":x['material__nombre'],
					"peso":x['pesoMaterial']
			}											
			totales.append(resultado)
		datos = Remision.objects.values(
												'id',
												'idOrden',
												'pesoNeto',
												'fechaRemision',
												'fechaActualizacion',
												'remision',
												'tallerAsignado__nombre',
												'funcion__proveedor',
												'remisiondetalle__cantidad',
												'remisiondetalle__peso',
												'remisiondetalle__folio',
												'remisiondetalle__numFolio',
												'remisiondetalle__longitud',
												'remisiondetalle__material__nombre')\
												.filter(fechaRegistro__gte=fechaInicialFormat,
																			fechaRegistro__lte=fechaFinalFormat,
																			funcion_id= idFuncion,
																			estatus=1).order_by("tallerAsignado__id")
		##print datos.query
		for e in datos:
			fechaR = e['fechaRemision'].strftime("%d/%m/%Y")
			fechaA = e['fechaActualizacion'].strftime("%d/%m/%Y")
			
			resultado = {   "value": 1,
							"excel":1,
								"id":e['id'],
								"orden":e['idOrden'],
								"pesoTotal":e['pesoNeto'],
								"peso":e['remisiondetalle__peso'],
								"fechaR":fechaR,
								"fechaA":fechaA,
								"taller":e['tallerAsignado__nombre'],
								"folio":e['remisiondetalle__folio'],
								"num":e['remisiondetalle__numFolio'],
								"remision":e['remision'],
								"proveedor":e['funcion__proveedor'],
								"piezas":e['remisiondetalle__cantidad'],
								"longitud":e['remisiondetalle__longitud'],
								"material":e['remisiondetalle__material__nombre']
							}

			data.append(resultado)
		array["data"]=data
		array["totales"]=totales
		if int(excel) == 1:
			#print "1"
			filename = excelReportesEntrada(request,array)
			return JsonResponse({"filename": filename})

		return JsonResponse(array)

	if idFuncion!='0' and idTaller!='0' and idFrente=='0' and tipo=='1' and inventario=='0':

		#print "Fabricante y Taller de Habilitado"
		
		total = RemisionDetalle.objects.values(	'material__id',
												'material__nombre'		
												).annotate(pesoMaterial = Sum('peso'))\
												.filter(remision__funcion__id =idFuncion,
														remision__tallerAsignado__id=idTaller,
														fechaRegistro__gte=fechaInicialFormat,
														fechaRegistro__lte=fechaFinalFormat,
														estatus=1)\
												.order_by("material__id")

		#print total.query
		for x in total:
			resultado = {
					"id":x['material__id'],
					"nombre":x['material__nombre'],
					"peso":x['pesoMaterial']
			}											
			totales.append(resultado)
		datos = Remision.objects.values(
												'id',
												'idOrden',
												'pesoNeto',
												'fechaRemision',
												'fechaActualizacion',
												'remision',
												'tallerAsignado__nombre',
												'funcion__proveedor',
												'remisiondetalle__cantidad',
												'remisiondetalle__peso',
												'remisiondetalle__folio',
												'remisiondetalle__numFolio',
												'remisiondetalle__longitud',
												'remisiondetalle__material__nombre')\
												.filter(fechaRegistro__gte=fechaInicialFormat,
																			fechaRegistro__lte=fechaFinalFormat,
																			funcion_id= idFuncion,
																			tallerAsignado__id=idTaller,
																			estatus=1).order_by("tallerAsignado__id")
		##print datos.query
		for e in datos:
			fechaR = e['fechaRemision'].strftime("%d/%m/%Y")
			fechaA = e['fechaActualizacion'].strftime("%d/%m/%Y")	
			resultado = {   "value": 1,
								"excel":2,
								"id":e['id'],
								"orden":e['idOrden'],
								"pesoTotal":e['pesoNeto'],
								"peso":e['remisiondetalle__peso'],
								"fechaR":fechaR,
								"fechaA":fechaA,
								"taller":e['tallerAsignado__nombre'],
								"folio":e['remisiondetalle__folio'],
								"num":e['remisiondetalle__numFolio'],
								"remision":e['remision'],
								"proveedor":e['funcion__proveedor'],
								"piezas":e['remisiondetalle__cantidad'],
								"longitud":e['remisiondetalle__longitud'],
								"material":e['remisiondetalle__material__nombre']
							}

			data.append(resultado)
		array["data"]=data
		array["totales"]=totales
		if int(excel) == 1:
			#print "2"
			filename = excelReportesEntrada(request,array)
			return JsonResponse({"filename": filename})

		return JsonResponse(array)

	elif idFrente=='0' and idTaller=='0' and idFuncion!='0' and tipo=='3' and inventario=='0':
		#print "elif Armador"
		total = Entrada.objects.values(			
												'material__id',
												'material__nombre',
												'entradadetalle__calculado',
												'cantidadReal',	
												'cantidadAsignada'	
												).filter(funcion__id =idFuncion,
														fechaRegistro__gte=fechaInicialFormat,
														fechaRegistro__lte=fechaFinalFormat,
														estatus=1)\
												.order_by("material__id")



		##print total.query
		for x in total:
			
			resultado = {
					"value":1,
					"id":x['material__id'],
					"nombre":x['material__nombre'],
					"faltante":x['entradadetalle__calculado'],
					"real":x['cantidadReal'],
					"cantidad":x['cantidadAsignada']
			}											
			totales.append(resultado)


		armador = Entrada.objects.values(
											'id',
											'cantidadAsignada',
											'funcion__proveedor',
											'material__nombre',
											'apoyo__numero',
											'cantidadReal',
											'fechaRegistro',
											'elemento__nombre',
											'folio',
											'material__id',
											'numFolio',
											'frente__id',
											'frente__nombre',
											'entradadetalle__nomenclatura',
											'entradadetalle__longitud',
											'entradadetalle__piezas',
											'entradadetalle__entrada_id',
											'entradadetalle__calculado',
											'remision').filter( funcion__id =idFuncion,
																fechaRegistro__gte=fechaInicialFormat,
																fechaRegistro__lte=fechaFinalFormat,
																estatus=1).order_by("folio")
		##print armador.query
		for e in armador:
			fecha = e['fechaRegistro'].strftime("%d/%m/%Y")
			resultado = {	"value": 2,
							"excel":3,
							"id":e['id'],
							"cantidad":e['cantidadAsignada'],
							"proveedor":e['funcion__proveedor'],
							"apoyo":e['apoyo__numero'],
							"folio":e['folio'],
							"fechaR":fecha,
							"nFolio":e['numFolio'],
							"idFrente":e['frente__id'],
							"idMaterial":e['material__id'],
							"frente":e['frente__nombre'],
							"nomenclatura":e['entradadetalle__nomenclatura'],
							"longitud":e['entradadetalle__longitud'],
							"piezas":e['entradadetalle__piezas'],
							"idED":e['entradadetalle__entrada_id'],
							"calculado":e['entradadetalle__calculado'],
							"remision":e['remision'],
							"material":e['material__nombre'],
							"cantidadReal":e['cantidadReal'],
							"elemento":e['elemento__nombre']
						}
			data.append(resultado)

		array["data"]=data
		array["totales"]=totales
		if int(excel) == 1:
			#print "Armador"
			filename = excelReportesEntrada(request,array)
			return JsonResponse({"filename": filename})
		##print array
		return JsonResponse(array)

	elif idFrente!='0' and idTaller=='0' and idFuncion=='0' and inventario=='0' :
		print "elif Frente de Trabajo"

		total = Entrada.objects.values(			
												'material__id',
												'material__nombre',
												'entradadetalle__calculado',
												'cantidadReal',
												'cantidadAsignada'	
												).filter(frente_id=idFrente,
														fechaRegistro__gte=fechaInicialFormat,
														fechaRegistro__lte=fechaFinalFormat,
														estatus=1)\
												.order_by("material__id")


		##print total.query
		for x in total:
			
			resultado = {
					"value":1,
					"id":x['material__id'],
					"nombre":x['material__nombre'],
					"cantidad":x['cantidadAsignada'],
					"faltante":x['entradadetalle__calculado'],
					"real":x['cantidadReal']
			}											
			totales.append(resultado)

		armador = Entrada.objects.values(
											'id',
											'cantidadAsignada',
											'funcion__proveedor',
											'material__nombre',
											'apoyo__numero',
											'cantidadReal',
											'elemento__nombre',
											'fechaRegistro',
											'folio',
											'material__id',
											'numFolio',
											'remision',
											'frente__id',
											'frente__nombre',
											'entradadetalle__entrada_id',
											'entradadetalle__nomenclatura',
											'entradadetalle__longitud',
											'entradadetalle__piezas',
											'entradadetalle__calculado'
											).filter(	frente_id=idFrente,
																fechaRegistro__gte=fechaInicialFormat,
																fechaRegistro__lte=fechaFinalFormat,
																estatus=1).order_by("folio")
		##print armador.query
		for e in armador:
			fecha = e['fechaRegistro'].strftime("%d/%m/%Y")
			resultado = {	"value": 2,
							"excel":4,
							"id":e['id'],
							"cantidad":e['cantidadAsignada'],
							"proveedor":e['funcion__proveedor'],
							"apoyo":e['apoyo__numero'],
							"fechaR":fecha,
							"folio":e['folio'],
							"nFolio":e['numFolio'],
							"idFrente":e['frente__id'],
							"idMaterial":e['material__id'],
							"frente":e['frente__nombre'],
							"idED":e['entradadetalle__entrada_id'],
							"calculado":e['entradadetalle__calculado'],
							"remision":e['remision'],
							"material":e['material__nombre'],
							"cantidadReal":e['cantidadReal'],
							"elemento":e['elemento__nombre'],
							"nomenclatura":e['entradadetalle__nomenclatura'],
							"longitud":e['entradadetalle__longitud'],
							"piezas":e['entradadetalle__piezas']
						}
			data.append(resultado)

		array["data"]=data
		array["totales"]=totales
		#excelReportes(request,array)
		if int(excel) == 1:
			#print "Frente de Trabajo"
			filename = excelReportesEntrada(request,array)
			return JsonResponse({"filename": filename})
		return JsonResponse(array)

	elif idFrente!='0' and idTaller=='0' and idFuncion!='0' and tipo=='3' and inventario=='0':
		#print "Frente de Trabajo y Armador"

		total = Entrada.objects.values(			
												'material__id',
												'material__nombre',
												'entradadetalle__calculado',
												'cantidadReal',
												'cantidadAsignada'	
												).filter(funcion__id =idFuncion,
														frente_id=idFrente,
														fechaRegistro__gte=fechaInicialFormat,
														fechaRegistro__lte=fechaFinalFormat,
														estatus=1)\
												.order_by("material__id")


		##print total.query
		for x in total:
			
			resultado = {
					"value":1,
					"id":x['material__id'],
					"nombre":x['material__nombre'],
					"cantidad":x['cantidadAsignada'],
					"faltante":x['entradadetalle__calculado'],
					"real":x['cantidadReal']
			}											
			totales.append(resultado)

		armador = Entrada.objects.values(
											'id',
											'cantidadAsignada',
											'funcion__proveedor',
											'material__nombre',
											'apoyo__numero',
											'cantidadReal',
											'fechaRegistro',
											'elemento__nombre',
											'folio',
											'material__id',
											'numFolio',
											'frente__id',
											'frente__nombre',
											'entradadetalle__nomenclatura',
											'entradadetalle__longitud',
											'entradadetalle__piezas',
											'entradadetalle__entrada_id',
											'entradadetalle__calculado',
											'remision').filter(	funcion__id =idFuncion,
																frente_id=idFrente,
																fechaRegistro__gte=fechaInicialFormat,
																fechaRegistro__lte=fechaFinalFormat,
																estatus=1).order_by("folio")
		##print armador.query
		for e in armador:
			fecha = e['fechaRegistro'].strftime("%d/%m/%Y")
			resultado = {	"value": 2,
							"excel":3,
							"id":e['id'],
							"cantidad":e['cantidadAsignada'],
							"proveedor":e['funcion__proveedor'],
							"apoyo":e['apoyo__numero'],
							"fechaR":fecha,
							"folio":e['folio'],
							"nFolio":e['numFolio'],
							"idFrente":e['frente__id'],
							"idMaterial":e['material__id'],
							"frente":e['frente__nombre'],
							"idED":e['entradadetalle__entrada_id'],
							"calculado":e['entradadetalle__calculado'],
							"remision":e['remision'],
							"material":e['material__nombre'],
							"cantidadReal":e['cantidadReal'],
							"elemento":e['elemento__nombre'],
							"nomenclatura":e['entradadetalle__nomenclatura'],
							"longitud":e['entradadetalle__longitud'],
							"piezas":e['entradadetalle__piezas']
						}
			data.append(resultado)

		array["data"]=data
		array["totales"]=totales
		if int(excel) == 1:
			#print "Frente de Trabajo y Armado"
			filename = excelReportesEntrada(request,array)
			return JsonResponse({"filename": filename})
		return JsonResponse(array)

	elif idTaller!='0' and idFrente=='0' and idFuncion=='0' and inventario=='0':
		#print "Taller del Habilitador"
		total = Remision.objects.values(	'remisiondetalle__material__id',
												'remisiondetalle__material__nombre'		
												).annotate(pesoMaterial = Sum('remisiondetalle__peso'))\
												.filter(tallerAsignado__id= idTaller,
														fechaRegistro__gte=fechaInicialFormat,
														fechaRegistro__lte=fechaFinalFormat,
														estatus=1)\
												.order_by("remisiondetalle__material__id")

		##print total.query
		for x in total:
			resultado = {
					"id":x['remisiondetalle__material__id'],
					"nombre":x['remisiondetalle__material__nombre'],
					"peso":x['pesoMaterial']
			}											
			totales.append(resultado)

		entrada = Remision.objects.values(
												'id',
												'idOrden',
												'pesoNeto',
												'fechaRemision',
												'fechaActualizacion',
												'remision',
												'tallerAsignado__nombre',
												'funcion__proveedor',
												'remisiondetalle__cantidad',
												'remisiondetalle__peso',
												'remisiondetalle__folio',
												'remisiondetalle__numFolio',
												'remisiondetalle__longitud',
												'remisiondetalle__material__nombre').filter(fechaRegistro__gte=fechaInicialFormat,
																			fechaRegistro__lte=fechaFinalFormat,
																			tallerAsignado__id= idTaller,
																			estatus=1).order_by("remisiondetalle__numFolio")											
		
		for e in entrada:
			fechaR = e['fechaRemision'].strftime("%d/%m/%Y")
			fechaA = e['fechaActualizacion'].strftime("%d/%m/%Y")	
			resultado = {   "value": 4,
								"excel":5,
								"id":e['id'],
								"orden":e['idOrden'],
								"pesoTotal":e['pesoNeto'],
								"peso":e['remisiondetalle__peso'],
								"fechaR":fechaR,
								"fechaA":fechaA,
								"taller":e['tallerAsignado__nombre'],
								"folio":e['remisiondetalle__folio'],
								"num":e['remisiondetalle__numFolio'],
								"remision":e['remision'],
								"proveedor":e['funcion__proveedor'],
								"piezas":e['remisiondetalle__cantidad'],
								"longitud":e['remisiondetalle__longitud'],
								"material":e['remisiondetalle__material__nombre']
			}
			dataEn.append(resultado)


		total = Salida.objects.values(	'material__id',
										'material__nombre'		
												).annotate(pesoMaterial = Sum('cantidadAsignada'))\
												.filter(tallerAsignado__id= idTaller,
														fechaRegistro__gte=fechaInicialFormat,
														fechaRegistro__lte=fechaFinalFormat,
														estatus=1)\
												.order_by("material__id")

		##print total.query
		for x in total:
			resultado = {
					"id":x['material__id'],
					"nombre":x['material__nombre'],
					"peso":x['pesoMaterial']
			}											
			totalesS.append(resultado)

		habilitadores= Salida.objects.values(
												'id',
												'cantidadAsignada',
												'fechaRegistro',
												'folio',
												'tallerAsignado__nombre',
												'tallerAsignado__funcion__proveedor',
												'apoyo__numero',
												'frente__nombre',
												'material__nombre',
												'cantidadReal',
												'elemento__nombre').filter(tallerAsignado_id=idTaller,
																			fechaRegistro__gte=fechaInicialFormat,
																			fechaRegistro__lte=fechaFinalFormat,
																			estatus=1)


		for e in habilitadores:
			fechaR = e['fechaRegistro'].strftime("%d/%m/%Y")
			resultado={	"value": 3,
						"excel":5,
						"id":e['id'],
						"cantidad":e['cantidadAsignada'],
						"fechaR":fechaR,
						"folio":e['folio'],
						"taller":e['tallerAsignado__nombre'],
						"proveedor":e['tallerAsignado__funcion__proveedor'],
						"apoyo":e['apoyo__numero'],
						"frente":e['frente__nombre'],
						"material":e['material__nombre'],
						"cantidadReal":e['cantidadReal'],
						"elemento":e['elemento__nombre']

			}

			data.append(resultado)

		array["entrada"]=dataEn
		array["totales"]=totales
		array["data"]=data
		array["totalesS"]=totalesS
		
		if int(excel) == 1:
			#print "5"
			filename = excelReportes(request,array)
			return JsonResponse({"filename": filename})
		return JsonResponse(array)

	elif idFuncion!='0' and idFrente=='0' and tipo=='2' and idTaller=='0' and inventario=='0':
		#print "Proveedor Habilitado"

		total = Remision.objects.values(	'remisiondetalle__material__id',
												'remisiondetalle__material__nombre'		
												).annotate(pesoMaterial = Sum('remisiondetalle__peso'))\
												.filter(tallerAsignado__funcion__id= idFuncion,
														fechaRegistro__gte=fechaInicialFormat,
														fechaRegistro__lte=fechaFinalFormat,
														estatus=1)\
												.order_by("remisiondetalle__material__id")

		##print total.query
		for x in total:
			resultado = {
					"id":x['remisiondetalle__material__id'],
					"nombre":x['remisiondetalle__material__nombre'],
					"peso":x['pesoMaterial']
			}											
			totales.append(resultado)

		entrada = Remision.objects.values(
												'id',
												'idOrden',
												'pesoNeto',
												'fechaRemision',
												'fechaActualizacion',
												'remision',
												'tallerAsignado__nombre',
												'funcion__proveedor',
												'remisiondetalle__cantidad',
												'remisiondetalle__peso',
												'remisiondetalle__folio',
												'remisiondetalle__numFolio',
												'remisiondetalle__longitud',
												'remisiondetalle__material__nombre').filter(fechaRegistro__gte=fechaInicialFormat,
																			fechaRegistro__lte=fechaFinalFormat,
																			tallerAsignado__funcion__id= idFuncion,
																			estatus=1).order_by("tallerAsignado__id")											
		
		for e in entrada:
			fechaR = e['fechaRemision'].strftime("%d/%m/%Y")
			fechaA = e['fechaActualizacion'].strftime("%d/%m/%Y")	
			resultado = {   "value": 4,
								"excel":6,
								"id":e['id'],
								"orden":e['idOrden'],
								"pesoTotal":e['pesoNeto'],
								"peso":e['remisiondetalle__peso'],
								"fechaR":fechaR,
								"fechaA":fechaA,
								"taller":e['tallerAsignado__nombre'],
								"folio":e['remisiondetalle__folio'],
								"num":e['remisiondetalle__numFolio'],
								"remision":e['remision'],
								"proveedor":e['funcion__proveedor'],
								"piezas":e['remisiondetalle__cantidad'],
								"longitud":e['remisiondetalle__longitud'],
								"material":e['remisiondetalle__material__nombre']
			}
			dataEn.append(resultado)

		total = Salida.objects.values(	'material__id',
										'material__nombre'		
												).annotate(pesoMaterial = Sum('cantidadAsignada'))\
												.filter(tallerAsignado__funcion__id=idFuncion,
														fechaRegistro__gte=fechaInicialFormat,
														fechaRegistro__lte=fechaFinalFormat,
														estatus=1)\
												.order_by("material__id")

		##print total.query
		for x in total:
			resultado = {
					"id":x['material__id'],
					"nombre":x['material__nombre'],
					"peso":x['pesoMaterial']
			}											
			totalesS.append(resultado)

		salida= Salida.objects.values(
												'id',
												'cantidadAsignada',
												'fechaRegistro',
												'folio',
												'tallerAsignado__nombre',
												'tallerAsignado__funcion__proveedor',
												'apoyo__numero',
												'frente__nombre',
												'material__nombre',
												'cantidadReal',
												'elemento__nombre').filter(tallerAsignado__funcion__id=idFuncion,
																			fechaRegistro__gte=fechaInicialFormat,
																			fechaRegistro__lte=fechaFinalFormat,
																			estatus=1).order_by("tallerAsignado__id")


		for s in salida:
			fechaR = s['fechaRegistro'].strftime("%d/%m/%Y")
			resultado={	"value": 4,
						"excel":6,
						"id":s['id'],
						"cantidad":s['cantidadAsignada'],
						"fechaR":fechaR,
						"folio":s['folio'],
						"taller":s['tallerAsignado__nombre'],
						"proveedor":s['tallerAsignado__funcion__proveedor'],
						"apoyo":s['apoyo__numero'],
						"frente":s['frente__nombre'],
						"material":s['material__nombre'],
						"cantidadReal":s['cantidadReal'],
						"elemento":s['elemento__nombre']

			}

			data.append(resultado)

		array["entrada"]=dataEn
		array["totales"]=totales
		array["data"]=data
		array["totalesS"]=totalesS
		if int(excel) == 1:
			#print "6"
			filename = excelReportes(request,array)
			return JsonResponse({"filename": filename})
		return JsonResponse(array)

	elif idFuncion!='0' and idTaller!='0' and idFrente=='0' and tipo=='2' and inventario=='0':
		#print "Proveedor Habilitado y Taller"

		total = Remision.objects.values(	'remisiondetalle__material__id',
												'remisiondetalle__material__nombre'		
												).annotate(pesoMaterial = Sum('remisiondetalle__peso'))\
												.filter(tallerAsignado__funcion__id= idFuncion,
														tallerAsignado__id= idTaller,
														fechaRegistro__gte=fechaInicialFormat,
														fechaRegistro__lte=fechaFinalFormat,
														estatus=1)\
												.order_by("remisiondetalle__material__id")

		##print total.query
		for x in total:
			resultado = {
					"id":x['remisiondetalle__material__id'],
					"nombre":x['remisiondetalle__material__nombre'],
					"peso":x['pesoMaterial']
			}											
			totales.append(resultado)

		entrada = Remision.objects.values(
												'id',
												'idOrden',
												'pesoNeto',
												'fechaRemision',
												'fechaActualizacion',
												'remision',
												'tallerAsignado__nombre',
												'funcion__proveedor',
												'remisiondetalle__cantidad',
												'remisiondetalle__peso',
												'remisiondetalle__folio',
												'remisiondetalle__numFolio',
												'remisiondetalle__longitud',
												'remisiondetalle__material__nombre').filter(fechaRegistro__gte=fechaInicialFormat,
																			fechaRegistro__lte=fechaFinalFormat,
																			tallerAsignado__id= idTaller,
																			tallerAsignado__funcion__id= idFuncion,
																			estatus=1).order_by("tallerAsignado__id")											
		
		for e in entrada:
			fechaR = e['fechaRemision'].strftime("%d/%m/%Y")
			fechaA = e['fechaActualizacion'].strftime("%d/%m/%Y")	
			resultado = {   "value": 4,
								"excel":6,
								"id":e['id'],
								"orden":e['idOrden'],
								"pesoTotal":e['pesoNeto'],
								"peso":e['remisiondetalle__peso'],
								"fechaR":fechaR,
								"fechaA":fechaA,
								"taller":e['tallerAsignado__nombre'],
								"folio":e['remisiondetalle__folio'],
								"num":e['remisiondetalle__numFolio'],
								"remision":e['remision'],
								"proveedor":e['funcion__proveedor'],
								"piezas":e['remisiondetalle__cantidad'],
								"longitud":e['remisiondetalle__longitud'],
								"material":e['remisiondetalle__material__nombre']
			}
			dataEn.append(resultado)

		total = Salida.objects.values(	'material__id',
										'material__nombre'		
												).annotate(pesoMaterial = Sum('cantidadAsignada'))\
												.filter(tallerAsignado__funcion__id=idFuncion,
														tallerAsignado__id= idTaller,
														fechaRegistro__gte=fechaInicialFormat,
														fechaRegistro__lte=fechaFinalFormat,
														estatus=1)\
												.order_by("material__id")

		##print total.query
		for x in total:
			resultado = {
					"id":x['material__id'],
					"nombre":x['material__nombre'],
					"peso":x['pesoMaterial']
			}											
			totalesS.append(resultado)

		salida= Salida.objects.values(
												'id',
												'cantidadAsignada',
												'fechaRegistro',
												'folio',
												'tallerAsignado__nombre',
												'tallerAsignado__funcion__proveedor',
												'apoyo__numero',
												'frente__nombre',
												'material__nombre',
												'cantidadReal',
												'elemento__nombre').filter(tallerAsignado__funcion__id=idFuncion,
																			tallerAsignado__id= idTaller,
																			fechaRegistro__gte=fechaInicialFormat,
																			fechaRegistro__lte=fechaFinalFormat,
																			estatus=1).order_by("tallerAsignado__id")


		for s in salida:
			fechaR = s['fechaRegistro'].strftime("%d/%m/%Y")
			resultado={	"value": 4,
						"excel":6,
						"id":s['id'],
						"cantidad":s['cantidadAsignada'],
						"fechaR":fechaR,
						"folio":s['folio'],
						"taller":s['tallerAsignado__nombre'],
						"proveedor":s['tallerAsignado__funcion__proveedor'],
						"apoyo":s['apoyo__numero'],
						"frente":s['frente__nombre'],
						"material":s['material__nombre'],
						"cantidadReal":s['cantidadReal'],
						"elemento":s['elemento__nombre']

			}

			data.append(resultado)

		array["entrada"]=dataEn
		array["totales"]=totales
		array["data"]=data
		array["totalesS"]=totalesS
		if int(excel) == 1:
			#print "6"
			filename = excelReportes(request,array)
			return JsonResponse({"filename": filename})
		return JsonResponse(array)

	elif idTaller!='0' and idFrente!='0' and idFuncion=='0' and inventario=='0':
		#print "Taller de habilitado y frente de trabajo"
		
		total = Salida.objects.values(	'material__id',
										'material__nombre'		
												).annotate(pesoMaterial = Sum('cantidadAsignada'))\
												.filter(tallerAsignado__id= idTaller,
														frente_id = idFrente,
														fechaRegistro__gte=fechaInicialFormat,
														fechaRegistro__lte=fechaFinalFormat,
														estatus=1)\
												.order_by("material__id")

		##print total.query
		for x in total:
			resultado = {
					"id":x['material__id'],
					"nombre":x['material__nombre'],
					"peso":x['pesoMaterial']
			}											
			totalesS.append(resultado)

		habilitadores= Salida.objects.values(
												'id',
												'cantidadAsignada',
												'fechaRegistro',
												'folio',
												'tallerAsignado__nombre',
												'tallerAsignado__funcion__proveedor',
												'apoyo__numero',
												'frente__nombre',
												'material__nombre',
												'cantidadReal',
												'elemento__nombre').filter(tallerAsignado_id=idTaller,
																			frente_id = idFrente,
																			fechaRegistro__gte=fechaInicialFormat,
																			fechaRegistro__lte=fechaFinalFormat,
																			estatus=1)


		for e in habilitadores:
			fechaR = e['fechaRegistro'].strftime("%d/%m/%Y")
			resultado={	"value": 3,
						"excel":7,
						"id":e['id'],
						"cantidad":e['cantidadAsignada'],
						"fechaR":fechaR,
						"folio":e['folio'],
						"taller":e['tallerAsignado__nombre'],
						"proveedor":e['tallerAsignado__funcion__proveedor'],
						"apoyo":e['apoyo__numero'],
						"frente":e['frente__nombre'],
						"material":e['material__nombre'],
						"cantidadReal":e['cantidadReal'],
						"elemento":e['elemento__nombre']

			}

			data.append(resultado)

		array["entrada"]=dataEn
		array["totales"]=totales
		array["data"]=data
		array["totalesS"]=totalesS
		
		#excelReportes(request,array)
		return JsonResponse(array)
	# else:
	# 	mensaje = {"estatus":"error", "mensaje":"Consulta invalida."}
	# 	array = mensaje
	# 	return JsonResponse(array)

@login_required(login_url='/control_acero/usuario/login/')
def inventarioFisicoView(request):
	i=1
	inventarioFisicoAnterior = InventarioFisico.objects.all().filter(tallerAsignado_id=request.session["idTaller"], estatusRegistro = 0)
	# folio = InventarioFisico.objects.all().filter(tallerAsignado_id = request.session["idTaller"]).order_by("-numFolio")[:1]
	# id = folio[0].numFolio
	# if folio.exists():
	# 	i=folio[0].numConteo
	template = 'control_acero/inventario/inventarioFisico.html'
	return render(request, template, {"inventarioFisicoAnterior":inventarioFisicoAnterior})

def elementoBusquedaView(request):
	array = {}
	mensaje = {}
	data = []
	idElemento = request.POST.get('elemento', 1)


	d = Elemento.objects.values("id",
								"material__nombre",
								"material__longitud",
								"imagen").filter(id=idElemento)
	
	for f in d:
			resultado = { "id":f["id"],
						"material":f["material__nombre"],
						"long": f["material__longitud"],
						"imagenElem" : f["imagen"]
						}
			data.append(resultado)

	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def materialCombo(request):
	array = {}
	mensaje = {}
	data = []
	material = Material.objects.all()
	for e in material:
			resultado = {"idMaterial":e.id,"nombre":e.nombre}
			data.append(resultado)

	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def materialBusquedaView(request):
	array = {}
	mensaje = {}
	data = []
	idMaterial = request.POST.get('material', 1)


	d = Material.objects.values("id",
								"nombre",
								"imagen").filter(id=idMaterial)
	##print d.query
	for f in d:
			resultado = {"id":f["id"],
						"nombre": f["nombre"],
						"imagen":f["imagen"]
						}
			data.append(resultado)

	array = mensaje
	array["data"]=data
	return JsonResponse(array)


@login_required(login_url='/control_acero/usuario/login/')
def frenteComboBusquedaViews(request):
	array = {}
	mensaje = {}
	data = []
	idFrente= request.POST.get('frente',1)
	frente = Frente.objects.filter(id= idFrente)
	for e in frente:
			resultado = {"idfrente":e.id,"nombre":e.nombre,"identificacion":e.identificacion, "ubicacion":e.ubicacion}
			data.append(resultado)

	array = mensaje
	array["data"]=data
	return JsonResponse(array)

def inventarioSave(request):
	array = {}
	mensaje = {}
	
	respuesta = request.POST.get('json')
	json_object = json.loads(respuesta)
	for data in json_object:
		datos = data["data"]
		splitData = datos.split("|")
		idMaterial = splitData[0]
		longitud = splitData[1]
		piezas = splitData[2]
		atado= splitData[3]
		nomenclatura = splitData[4]
		elemento = splitData[5]
		
		if nomenclatura == 'null':
			inv = InventarioFisico.objects\
								.create(
										cantidadPiezas=piezas,
										longitud=longitud,
										atado=atado,
										material_id=idMaterial								
										)
		if atado == 'null':
			inv = InventarioFisico.objects\
								.create(
										cantidadPiezas=piezas,
										longitud=longitud,
										nomenclatura=nomenclatura,
										material_id=idMaterial,
										elemento_id=elemento								
										)
	mensaje = {"estatus":"ok", "mensaje":"Recepción del Material Exitoso."}
	array = mensaje
	

	return JsonResponse(array)

def inventarioFisicoCierreSave(request):
	array = {}
	mensaje = {}
	respuesta = request.POST.get('json')
	fechaRemision= '14/06/2016'
	json_object = json.loads(respuesta)
	inventarioremisiondetalle__estatusInventario = 0
	cantidad=0
	
	for data in json_object:
		idC= data["id"]
		
	RemisionDetalle.objects.filter(estatusInventario=0,estatus=1).update(estatusInventario=1,folioInventario=idC)
	InventarioRemisionDetalle.objects.filter(estatusInventario=0, estatus=1).update(estatusInventario=1,folioInventario=idC)
	Salida.objects.filter(estatusInventario=0, estatus=1).update(estatusInventario=1,folioInventario=idC)
	InventarioSalida.objects.filter(estatusInventario=0, estatus=1).update(estatusInventario=1,folioInventario=idC)
	numFolio=0
	folio = InventarioFisicoDetalleCierre.objects.all().filter(tallerAsignado_id = request.session["idTaller"]).order_by("-numFolio")[:1]
	if folio.exists():
			numFolio = folio[0].numFolio
	numFolioInt = int(numFolio)+1
	numFolio = "%03d" % (numFolioInt,)
	ident= request.session["proveedorTaller"]
	numFolio = "IFA-"+ident+"-"+numFolio
	numFolio = numFolio.encode('utf-8')
	
	for data in json_object:

		#print data
		idCierre = data["id"]
		material = data["material"]
		existencia = data["existencia"]
		fisico = data["fisico"]
		diferencia = data["diferencia"]
		print diferencia
		ifd = InventarioFisicoDetalle.objects.get(pk=idCierre)
		idInventario = ifd.inventarioFisico_id
		#print diferencia
		cantidadEntrada = data["cantidadEntrada"]
		if cantidadEntrada:
			cantidadEntrada
			auxEntrada = int(cantidadEntrada) + int(diferencia)
			p = Remision.objects\
				.create(pesoNeto=auxEntrada,
						fechaRemision=datetime.strptime(fechaRemision, '%d/%m/%Y'),
						estatus=1,
						ajuste_id=idInventario,
						tallerAsignado_id=request.session['idTaller']
						)
			pd = RemisionDetalle.objects\
							.create(
									remision_id=p.pk,
									material_id=material,
									apoyo_id=1,
									elemento_id=1,
									numFolio=0,
									peso=auxEntrada,
									longitud=12
									)
			ird = InventarioRemisionDetalle.objects\
							.create(
									remision_id=p.pk,
									apoyo_id=1,
									elemento_id=1,
									numFolio=0,
									material_id=material,
									peso=auxEntrada,
									longitud=12
									)
		else:
			cantidadEntrada = 0
		observacionEntrada = data["observacionEntrada"]
		cantidadSalida = data["cantidadSalida"]
		#print cantidadSalida
		if cantidadSalida:
			cantidadReal = InventarioRemisionDetalle.objects\
						.values(
								'material_id',
								'material__nombre'
								)\
						.annotate(pesoMaterial = Sum('peso'))\
						.annotate(cantidadMaterial = Sum('cantidad'))\
						.filter(peso__gt = 0, remision__tallerAsignado_id = request.session["idTaller"], material_id = material)\
						.order_by('material_id')

			cantidad = cantidadReal[0]['pesoMaterial']
			#print "------"
			#print material
			#print cantidadReal[0]['pesoMaterial']
			cantidadAsignada = int(cantidadSalida)+ int(diferencia)
			totalAsignado = cantidadAsignada
			print totalAsignado
			remisionDetallesTotales = InventarioRemisionDetalle.objects\
							.values(
									'material_id',
									'material__nombre'
									)\
							.annotate(pesoMaterial = Sum('peso'))\
							.annotate(cantidadMaterial = Sum('cantidad'))\
							.filter(material_id = material, remision__tallerAsignado_id = request.session["idTaller"])
			for remisionDetallesTotal in remisionDetallesTotales:
				if Decimal(remisionDetallesTotal["pesoMaterial"]) >= Decimal(totalAsignado):
					inventarioRemisionDetalles = InventarioRemisionDetalle.objects.all()\
													.filter(
															material_id = material,
															estatusTotalizado = 1,
															remision__tallerAsignado_id = request.session["idTaller"])\
													.order_by("id")
					for inventarioRemisionDetalle in inventarioRemisionDetalles:
						inventarioId = inventarioRemisionDetalle.id
						irdpeso = inventarioRemisionDetalle.peso
						peso=Decimal(totalAsignado)
						if Decimal(irdpeso) <= Decimal(totalAsignado):
							totalAsignado = Decimal(totalAsignado) - Decimal(irdpeso)
							descuento = DescuentoSalida.objects\
												.create(
														pesoSalida = peso,
														pesoRemision = irdpeso,
														resta = totalAsignado,
														inventarioRemisionDetalle_id =inventarioId
														)
							InventarioRemisionDetalle.objects.filter(id=inventarioId).update(peso=0, estatusTotalizado = 0)
							continue

						if Decimal(irdpeso) > Decimal(totalAsignado) and Decimal(totalAsignado) != 0:
							cantidadRestar = Decimal(irdpeso) - Decimal(totalAsignado)
							descuento = DescuentoSalida.objects\
												.create(
														pesoSalida = totalAsignado,
														pesoRemision = irdpeso,
														resta = cantidadRestar,
														inventarioRemisionDetalle_id =inventarioId
														)
							if cantidadRestar >= 0:
								totalAsignado = 0;
							InventarioRemisionDetalle.objects.filter(id=inventarioId).update(peso=cantidadRestar)
			#print"**********"
			#print material
			#print cantidadAsignada

			salida = Salida.objects\
							.create(
									tipoEstatus = 2,
									material_id = material,
									cantidadReal = cantidad,
									ajuste_id=idInventario,
									cantidadAsignada = cantidadAsignada,
									estatusEtapa = 1,
									numFolio=0,
									tallerAsignado_id = request.session["idTaller"]
									)
			DescuentoSalida.objects.filter(estatusSalida=0).update(salida_id=salida.pk, estatusSalida=1)
			inventarioSalida = InventarioSalida.objects\
							.create(
									material_id = material,
									cantidadReal = cantidad,
									cantidadAsignada = cantidadAsignada,
									numFolio=0,
									estatusEtapa = 1,
									tallerAsignado_id = request.session["idTaller"]
									)
		else:
			cantidadSalida = 0

		observacionSalida = data["observacionSalida"]
		
		ifdc = InventarioFisicoDetalleCierre.objects\
				.create(
						pesoExistencia = existencia,
						pesoFisico = fisico,
						diferencia = diferencia,
						cantidadEntrada = cantidadEntrada,
						observacionEntrada = observacionEntrada,
						cantidadSalida = cantidadSalida,
						observacionSalida = observacionSalida,
						tipoExistencia = ifd.tipoExistencia,
						inventarioFisico_id = ifd.inventarioFisico_id,
						material_id = material,
						numFolio = numFolioInt, 
						folio = numFolio,
						tallerAsignado_id = request.session["idTaller"]
					)
	InventarioFisico.objects.filter(estatusRegistro=0).update(estatusRegistro=1)#COLOCAR--- PARA GUARDAR REGISTRO DE MOVIMIENTO POR Inventario
	bitacora = Bitacora.objects.create(accion="Cierre", id_afectado=idInventario, observacion="El id guardado es de inventario cierre", estatus=1, modulo_id=5, user_id=request.user.id)
	mensaje = {"estatus":"ok", "mensaje":"El inventario se ha modificado y cerrado Correctamente.  Folio: "+numFolio, "folio":numFolio}
	array = mensaje
	#mailHtmlIFA(request,ifdc.pk)
	return JsonResponse(array)

def inventarioRemision(request):
	cursor = connection.cursor()
	array = {}
	arrayVal1 = []
	arrayVal2 = []
	arrayVal3 = []
	dataRemision = []
	dataRemisionInventario = []
	dataRemisionInventarioSum = []
	dataSalida = []
	dataSalidaInventario = []
	dataInventario = []
	remisiones = Remision.objects.values(
										"remisiondetalle__id",
										"remisiondetalle__material__nombre",
										"remisiondetalle__peso",
										"remisiondetalle__longitud",
										"remisiondetalle__numFolio"
										)\
					.filter(remisiondetalle__estatusInventario = 0, tallerAsignado_id = request.session['idTaller'],estatus=1).distinct()
	for remision in remisiones:
			resultado = {
							"id":remision["remisiondetalle__id"],
							"material":remision["remisiondetalle__material__nombre"],
							"peso":remision["remisiondetalle__peso"],
							"longitud":remision["remisiondetalle__longitud"],
							"numFolio":remision["remisiondetalle__numFolio"]
						}
			dataRemision.append(resultado)
	remisionesInventario = Remision.objects.values(
										"inventarioremisiondetalle__id",
										"inventarioremisiondetalle__material__nombre",
										"inventarioremisiondetalle__peso",
										"inventarioremisiondetalle__longitud"
										)\
					.filter(inventarioremisiondetalle__estatusInventario = 0, tallerAsignado_id = request.session['idTaller'],estatus=1).distinct()
	for remisionInventario in remisionesInventario:
			resultado = {
							"id":remisionInventario["inventarioremisiondetalle__id"],
							"material":remisionInventario["inventarioremisiondetalle__material__nombre"],
							"peso":remisionInventario["inventarioremisiondetalle__peso"],
							"longitud":remisionInventario["inventarioremisiondetalle__longitud"]
						}
			dataRemisionInventario.append(resultado)
	try:
		cursor.execute("SELECT control_acero_inventarioremisiondetalle.material_id, control_acero_material.nombre, SUM(control_acero_inventarioremisiondetalle.peso) AS pesoMaterial\
													FROM control_acero_remision\
													LEFT OUTER JOIN control_acero_inventarioremisiondetalle ON ( control_acero_remision.id = control_acero_inventarioremisiondetalle.remision_id )\
													LEFT OUTER JOIN control_acero_material ON ( control_acero_inventarioremisiondetalle.material_id = control_acero_material.id )\
													WHERE control_acero_remision.tallerAsignado_id = %s\
													AND control_acero_inventarioremisiondetalle.estatusTotalizado = 1\
													AND control_acero_inventarioremisiondetalle.estatus = 1\
													AND control_acero_remision.estatus = 1\
													GROUP BY control_acero_inventarioremisiondetalle.material_id, control_acero_material.nombre\
													ORDER BY control_acero_inventarioremisiondetalle.material_id ASC", [request.session['idTaller']]);
		remisionesInventarioSum = cursor.fetchall()
	finally:
		cursor.close()
	salidas = Salida.objects.values(
										"id",
										"cantidadReal",
										"cantidadAsignada",
										"numFolio"
										)\
					.filter(estatusInventario = 0, tallerAsignado_id = request.session['idTaller'],estatus =1)
	for salida in salidas:
			resultado = {
						"id":salida["id"],
						"cantidadReal":salida["cantidadReal"],
						"cantidadAsignada":salida["cantidadAsignada"],
						"numFolio":salida["numFolio"]
						}
			dataSalida.append(resultado)
	salidasInventario = InventarioSalida.objects.values(
										"id",
										"cantidadReal",
										"cantidadAsignada"
										)\
					.filter(estatusInventario = 0, tallerAsignado_id = request.session['idTaller'],estatus =1)
	for salidaInventario in salidasInventario:
			resultado = {
						"id":salidaInventario["id"],
						"cantidadReal":salidaInventario["cantidadReal"],
						"cantidadAsignada":salidaInventario["cantidadAsignada"]
						}
			dataSalidaInventario.append(resultado)
	# lastInventarioFisico = InventarioFisico.objects.order_by('-id')[:1]
	# if lastInventarioFisico.count() >= 1:
	# 	inventariosFisico = InventarioFisico.objects.values(
	# 										"inventariofisicodetallecierre__material_id",
	# 										"inventariofisicodetallecierre__material__nombre",
	# 										"inventariofisicodetallecierre__pesoExistencia"
	# 										)\
	# 					.filter(pk=lastInventarioFisico[0].id, tallerAsignado_id = request.session['idTaller'])
	# else:
	# 	inventariosFisico = InventarioFisico.objects.values(
	# 										"inventariofisicodetallecierre__material_id",
	# 										"inventariofisicodetallecierre__material__nombre",
	# 										"inventariofisicodetallecierre__pesoExistencia"
	# 										)\
	# 					.filter(tallerAsignado_id = request.session['idTaller'])
	# for inventarioFisico in inventariosFisico:
	# 		resultado = {
	# 					"material":inventarioFisico["inventariofisicodetallecierre__material_id"],
	# 					"restante":inventarioFisico["inventariofisicodetallecierre__pesoExistencia"],
	# 					}
	# 		dataInventario.append(resultado)
	# if inventariosFisico.exists():
	# 	for inventarioFisico in inventariosFisico:
	# 		material1 = inventarioFisico["inventariofisicodetallecierre__material_id"]
	# 		arrayVal1.append(material1);
	# 		fisicoActual = inventarioFisico["inventariofisicodetallecierre__pesoExistencia"]
	# 		for remisionInventarioSum in remisionesInventarioSum:
	# 			material2 = remisionInventarioSum[0]
	# 			arrayVal2.append(material2);
	# 			if material1 == material2:
	# 				resultado = {
	# 							"materialId":remisionInventarioSum[0],
	# 							"material":remisionInventarioSum[1],
	# 							"peso":remisionInventarioSum[2],
	# 							"fisicoActual":fisicoActual,
	# 							}
	# 				dataRemisionInventarioSum.append(resultado)
	# 				#print "ok1"
	# 			##print arrayVal1
	# 			arrayVal3 = (list(set(arrayVal1).difference(arrayVal2)))

	# 	if len(arrayVal3) > 0:
	# 		for val3 in arrayVal3:
	# 			for inventarioFisico in inventariosFisico:
	# 				materialF = inventarioFisico["inventariofisicodetallecierre__material_id"]
	# 				if val3 == materialF:
	# 					resultado = {
	# 								"materialId":materialF,
	# 								"material":inventarioFisico["inventariofisicodetallecierre__material__nombre"],
	# 								"peso":0,
	# 								"fisicoActual":inventarioFisico["inventariofisicodetallecierre__pesoExistencia"],
	# 								}
	# 					dataRemisionInventarioSum.append(resultado)
	# 					#print "ok2"
	# else:
	for remisionInventarioSum in remisionesInventarioSum:
			resultado = {
						"materialId":remisionInventarioSum[0],
						"material":remisionInventarioSum[1],
						"peso":remisionInventarioSum[2],
						"fisicoActual":0
					}
			dataRemisionInventarioSum.append(resultado)
			#print "ok3"

	#print dataRemisionInventarioSum
	array["remisiones"]=dataRemision
	array["remisionesInventario"]=dataRemisionInventario
	array["remisionesInventarioSum"]=dataRemisionInventarioSum
	array["salidas"]=dataSalida
	array["salidasInventario"]=dataSalidaInventario
	return JsonResponse(array)

@login_required(login_url='/control_acero/usuario/login/')	
def apoyoBusquedaView(request):
	array = {}
	mensaje = {}
	data = []
	idApoyo = request.POST.get('Apoyo', 1)

	d = Apoyo.objects.values("id", 
								"numero",
								"elemento__nombre",
								"elemento__id",
								"elemento__imagen").filter(id=idApoyo)
	##print d.query


	for f in d:
			resultado = {"idApoyo":f["id"],
						"nombre": f["numero"],
						"elemento":f["elemento__nombre"],
						"idE":f["elemento__id"],
						"imagen":f["elemento__imagen"]
						}
			data.append(resultado)
    
	array = mensaje
	array["data"]=data

	return JsonResponse(array)


def mailHtmlHeader(request):
	##print logo
	# <img src="%s" alt="Logo" />
	html = """\
			<html>
				<head>
				</head>
				<body>
					<br />
					<table rules="all" style="border-color: #666;" cellpadding="10">
						<thead>
							<tr style='background: #66cc00;'>
								<th><strong> Usuario </strong></th>
								<th><strong> Nombre </strong></th>
								<th><strong> Email </strong></th>
							</tr>
						</thead>
						<tbody>
							<tr>
								<td>%s</td>
								<td>%s %s</td>
								<td>%s</td>
							</tr>
						</tbody>
					</table>
			""" %\
			(	
				
				request.user.username,
				request.user.first_name,
				request.user.last_name,
				request.user.email,
			)
	return html;

def mailHtmlFooter():
	html = """\
			</body>
			</html>
			"""
	return html;

def mailHtml(request, folio):
	# Mail Recepcion Material
	remisiones = Remision.objects.values(
											"idOrden",
											"remision",
											"fechaRemision",
											"fechaRegistro",
											"funcion_id",
											"funcion__proveedor",
											"pesoNeto",
											"pesoBruto",
											"pesoTara",
											"observacion",
											"remisiondetalle__material__nombre",
											"remisiondetalle__peso",
											"remisiondetalle__longitud",
											"remisiondetalle__cantidad",
											"remisiondetalle__folio"
										)\
										.filter(
											remisiondetalle__numFolio = folio,
											tallerAsignado_id = request.session['idTaller']
										)\
										.distinct()
	tablaDetalle = ''
	tablaDetalle += """\
					
					<table rules="all" style="border-color: #666;" cellpadding="10">
						<thead>
							<tr style='background: #66cc00;'>
								<th>Material</th>
								<th>Piezas</th>
								<th>Peso Recibido Kg</th>
								<th>Longitud</th>
							</tr>
						</thead>
						<tbody>\
						"""

	for rem in remisiones:
		tablaDetalle += """\
							<tr>
								<td>%s</td>
								<td>%d</td>
								<td>%d</td>
								<td>%d</td>
							</tr>
						"""%\
						(
							rem["remisiondetalle__material__nombre"],
							rem["remisiondetalle__cantidad"],
							rem["remisiondetalle__peso"],
							rem["remisiondetalle__longitud"]
						)

	tablaDetalle += """\
						</tbody>
					</table>
					<br />\
					"""

	folioStr = remisiones[0]["remisiondetalle__folio"]
	proveedor = remisiones[0]["funcion__proveedor"]
	orden = remisiones[0]["idOrden"]
	remision = remisiones[0]["remision"]
	fechaRemision = remisiones[0]["fechaRemision"]
	fechaRegistro = remisiones[0]["fechaRegistro"]
	pesoNeto= remisiones[0]["pesoNeto"]
	pesoBruto= remisiones[0]["pesoBruto"]
	pesoTara= remisiones[0]["pesoTara"]
	observacion=remisiones[0]["observacion"]

	envioEmails = User.objects.all().filter(taller__id = request.session['idTaller'])
	header = "RECEPCIÓN DEL MATERIAL"
	body = ""
	body += mailHtmlHeader(request)
	body += """
			<br />
			<table rules="all" style="border-color: #666;" cellpadding="10">
				<thead>
					<tr style='background:#66cc00;'>
						<th><strong> Folio </strong></th>
						<th><strong> Fabricante </strong></th>
						<th><strong> Orden </strong></th>
						<th><strong> Remisi&oacute;n </strong></th>
						<th><strong> Fecha Remisi&oacute;n </strong></th>
						<th><strong> Fecha Creaci&oacute;n </strong></th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<td><strong>%s</strong></td>
						<td>%s</td>
						<td>%s</td>
						<td>%s</td>
						<td>%s</td>
						<td>%s</td>
					</tr>
				</tbody>
			</table>
			<br />
			""" %\
			(
				folioStr,
				proveedor,
				orden,
				remision,
				fechaRemision.strftime("%d/%m/%Y"),
				fechaRegistro.strftime("%d/%m/%Y %H:%M:%S")
			)
	body += tablaDetalle
	body += """
			<br />
			<h4>Peso Neto: %d  Kg </h4>
			<h4>Peso Tara: %d  Kg </h4>
			<h4>Peso Bruto: %d  Kg </h4>
			""" %\
			(
				pesoNeto,
				pesoTara,
				pesoBruto
				)
	body += mailHtmlFooter()

	for envioEmail in envioEmails:
		mail(header, body, envioEmail.email)

	return True

def mailHtmlSH(request, folio):
	# Mail Salida Habilitado
	#salidaHabilitadoSave
	res=0;
	auxF='';
	salida = Salida.objects.values(			"folio",
											"cantidadAsignada",
											"fechaRegistro",
											"apoyo__numero",
											"frente__id",
											"frente__nombre",
											"material__nombre",
											"elemento__nombre",
											"tallerAsignado__nombre",
											"cantidadReal",
											"estatusReposicion"
										)\
										.filter(
											numFolio = folio,
											tallerAsignado_id = request.session['idTaller']
										)\
										.distinct()\
										.order_by("material__id")
	tablaDetalle = ''
	tablaDetalle += """\
					
					<table rules="all" style="border-color: #666;" cellpadding="10">
						<thead>
							<tr style='background: #66cc00;'>
								<th>Material</th>
								<th>Peso de Salida de Habilitado en Kg</th>
								<th>Peso Restante en Almac&eacute;n Kg</th>
							</tr>
						</thead>
						<tbody>\
						"""

	for rem in salida:
		res=rem["cantidadReal"]-rem["cantidadAsignada"]

		tablaDetalle += """\
							<tr>
								<td>%s</td>
								<td>%d</td>
								<td>%d</td>
							</tr>
						"""%\
						(
							rem["material__nombre"],
							rem["cantidadAsignada"],
							res
						)

	tablaDetalle += """\
						</tbody>
					</table>
					<br />\
					"""

	tablaDetalleF = ''
	tablaDetalleF += """\
					
					<table rules="all" style="border-color: #666;" cellpadding="10">
						<thead>
							<tr style='background: #66cc00;'>
								<th>Material</th>
								<th>Peso Recibido Kg</th>
							</tr>
						</thead>
						<tbody>\
						"""

	for rem in salida:
		tablaDetalleF += """\
							<tr>
								<td>%s</td>
								<td>%d</td>
							</tr>
						"""%\
						(
							rem["material__nombre"],
							rem["cantidadAsignada"]
						)

	tablaDetalleF += """\
						</tbody>
					</table>
					<br />\
					"""

	folioStr = salida[0]["folio"]
	taller = salida[0]["tallerAsignado__nombre"]
	frente = salida[0]["frente__nombre"]
	apoyo = salida[0]["apoyo__numero"]
	elemento = salida[0]["elemento__nombre"] 
	fechaRegistro = salida[0]["fechaRegistro"]
	reposicion = salida[0]["estatusReposicion"]
	reposicion = int(reposicion)
	if reposicion == 1:
		auxF='SI'
	if reposicion == 2:
		auxF='NO'
	print "**"
	print reposicion
	print auxF
	talleresEmail = User.objects.all().filter(taller__id = request.session['idTaller'])

	frentesEmail = User.objects.all().filter(frente__id = salida[0]["frente__id"])

	header = "SALIDA DE MATERIAL HABILITADO"
	body = ""
	body2 = ""
	aux = "" 
	
	body += mailHtmlHeader(request)
	body += """
			<h4>Reporte a Habilitadores</h4>

			"""
	
	aux += """
			<br />
			<table rules="all" style="border-color: #666;" cellpadding="10">
				<thead>
					<tr style='background: #66cc00;'>
						<th><strong> Folio </strong></th>
						<th><strong> Taller </strong></th>
						<th><strong> Frente Enviado</strong></th>
						<th><strong> Apoyo </strong></th>
						<th><strong> Elemento </strong></th>
						<th><strong> Fecha Creaci&oacute;n </strong></th>
						<th><strong> Reposici&oacute;n de Material Faltante</strong> </th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<td><strong>%s</strong></td>
						<td>%s</td>
						<td>%s</td>
						<td>%s</td>
						<td>%s</td>
						<td>%s</td>
						<td>%s</td>
					</tr>
				</tbody>
			</table>
			<br />
			""" %\
			(
				folioStr,
				taller,
				frente,
				apoyo,
				elemento,
				fechaRegistro.strftime("%d/%m/%Y %H:%M:%S"),
				auxF
			)
	body2 += mailHtmlHeader(request)
	body2 += """
			<h4>Proxima Entrega en Frente de Trabajo</h4>

			"""
	body2 += aux
	body +=aux

	body += tablaDetalle
	body += mailHtmlFooter()


	body2 +=tablaDetalleF
	body2 +=mailHtmlFooter()

	
	for envio in frentesEmail:
		mail(header, body2, envio.email)
	
	
	for envioEmail in talleresEmail:
		mail(header, body, envioEmail.email)
	return True	

def mailHtmlEA(request, folio):
	# Mail entradaArmadoSave
	res=0
	flag=0
	entrada = Entrada.objects.values(	   "folio",
											"cantidadAsignada",
											"remision",
											"funcion__proveedor",
											"fechaRegistro",
											"apoyo__numero",
											"frente__id",
											"frente__nombre",
											"material__nombre",
											"elemento__nombre",
											"cantidadReal",
											"entradadetalle__entrada_id",
											"entradadetalle__nomenclatura",
											"entradadetalle__longitud",
											"entradadetalle__piezas",
											"entradadetalle__calculado"
										)\
										.filter(
											numFolio = folio,
											frente_id = request.session['idFrente']
										)\
										.distinct()\
										.order_by("material__id")
	
	tablaDetalle = ''
	tabla = ''
	tablaDetalleFaltante =''
	tablaDetalle += """\
					
					<table rules="all" style="border-color: #666;" cellpadding="10">
						<thead>
							<tr style='background: #66cc00;'>
								<th>Material</th>
								<th>Peso de Recibido en Kg</th>
							</tr>
						</thead>
						<tbody>\
						"""
	

	tablaDetalleFaltante += """\
					<br />
					<table rules="all" style="border-color: #666;" cellpadding="10">
						<thead>
							<tr style='background: #66cc00;'>
								<th>Material</th>
								<th>Nomenclatura</th>
								<th>Num. Piezas</th>
								<th>Longitud Mts</th>
								<th>Peso Faltante en Kg</th>
							</tr>
						</thead>
						<tbody>\
						"""

	for rem in entrada:
		cantReal= rem["cantidadReal"]
		cantReal= rem["cantidadReal"]
		nombre = rem["material__nombre"]
		if rem["entradadetalle__nomenclatura"]!=None:
			res= res + rem["cantidadAsignada"]
			tablaDetalleFaltante += """\
										<tr>
											<td>%s</td>
											<td>%s</td>
											<td>%d</td>
											<td>%d</td>
											<td>%d</td>
										</tr>
									"""%\
									(
										rem["material__nombre"],
										rem["entradadetalle__nomenclatura"],
										rem["entradadetalle__longitud"],
										rem["entradadetalle__piezas"],
										rem["cantidadAsignada"]
										
									)


		else:
			#res= res + rem["cantidadAsignada"]
			

			tablaDetalle += """\
									<tr>
										<td>%s</td>
										<td>%d</td>
									</tr>
								"""%\
								(
									rem["material__nombre"],
									rem["cantidadAsignada"]
									
								)


	#print "***********"
	#print res
	#print cantReal
	cantReal=cantReal-res
	#print cantReal

	tabla += """\
					<tr>
						<td>%s</td>
						<td>%d</td>
					</tr>
			"""%\
			(
				nombre,
				cantReal
				)
	tablaDetalle += tabla

	tablaDetalle += """\
						</tbody>
					</table>
					<br />\
					"""
	tablaDetalleFaltante += """\
						</tbody>
					</table>
					<br />\
					"""

	
	folioStr = entrada[0]["folio"]
	proveedor = entrada[0]["funcion__proveedor"]
	remision = entrada[0]["remision"]
	frente = entrada[0]["frente__nombre"]
	apoyo = entrada[0]["apoyo__numero"]
	elemento = entrada[0]["elemento__nombre"] 
	fechaRegistro = entrada[0]["fechaRegistro"]

	frenteEmail = User.objects.all().filter(frente__id = request.session['idFrente'])

	
	header = "RECEPCION EN FRENTE DE TRABAJO"
	body = ""

	body += mailHtmlHeader(request)
	body += """
			<br />
			<table rules="all" style="border-color: #666;" cellpadding="10">
				<thead>
					<tr style='background: #66cc00;'>
						<th><strong> Folio </strong></th>
						<th><strong> Remisi&oacute;n </strong></th>
						<th><strong> Recepci&oacute;n en el Frente </strong></th>
						<th><strong> Armador Asignado </strong></th>
						<th><strong> Apoyo </strong></th>
						<th><strong> Elemento </strong></th>
						<th><strong> Fecha Creaci&oacute;n </strong></th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<td><strong>%s</strong></td>
						<td>%s</td>
						<td>%s</td>
						<td>%s</td>
						<td>%s</td>
						<td>%s</td>
						<td>%s</td>
					</tr>
				</tbody>
			</table>
			<br />
			""" %\
			(
				folioStr,
				remision,
				frente,
				proveedor,				
				apoyo,
				elemento,
				fechaRegistro.strftime("%d/%m/%Y %H:%M:%S")
			)
	
	body += tablaDetalle
	body += tablaDetalleFaltante
	body += mailHtmlFooter()

	for envioEmail in frenteEmail:
		mail(header, body, envioEmail.email)
	return True	

def mailHtmlIF(request, folio):
	# Mail Inventariofisico
	#print "IF****"
	#print folio
	cierre = ''
	idfolio= int(folio)
	inventario = InventarioFisico.objects.values(
											"folio",
											"fechaRegistro",
											"tallerAsignado__nombre",
											"estatusRegistro",
											"inventariofisicodetalle__pesoExistencia",
											"inventariofisicodetalle__pesoFisico",
											"inventariofisicodetalle__diferencia",
											"inventariofisicodetalle__material__nombre"
										)\
										.filter(
											id = idfolio,
											tallerAsignado_id = request.session['idTaller']
										)\
										.distinct()\
										.order_by("inventariofisicodetalle__material__id")
	tablaDetalle = ''
	tablaDetalle += """\
					
					<table rules="all" style="border-color: #666;" cellpadding="10">
						<thead>
							<tr style='background: #66cc00;'>
								<th>Material</th>
								<th>Peso existencia en el sistema</th>
								<th>Peso existencias f&iacute;sicas</th>
								<th>Diferencia</th>
							</tr>
						</thead>
						<tbody>\
						"""

	for rem in inventario:

		tablaDetalle += """\
							<tr>
								<td>%s</td>
								<td>%d</td>
								<td>%d</td>
								<td>%d</td>
							</tr>
						"""%\
						(
							rem["inventariofisicodetalle__material__nombre"],
							rem["inventariofisicodetalle__pesoExistencia"],
							rem["inventariofisicodetalle__pesoFisico"],
							rem["inventariofisicodetalle__diferencia"]
						)

	tablaDetalle += """\
						</tbody>
					</table>
					<br />\
					"""

	folioStr = inventario[0]["folio"]
	taller = inventario[0]["tallerAsignado__nombre"]
	fechaRegistro = inventario[0]["fechaRegistro"]
	if inventario[0]["estatusRegistro"]==1:
			cierre = 'Cierre automatico - Inventario correcto'

	envioEmails = User.objects.all().filter(taller__id = request.session['idTaller'])
	header = "INVENTARIO FISICO"
	body = ""
	body += mailHtmlHeader(request)
	body += """
			<br />
			<table rules="all" style="border-color: #666;" cellpadding="10">
				<thead>
					<tr style='background:#66cc00;'>
						<th><strong> Folio </strong></th>
						<th><strong> Taller de Habilitado </strong></th>
						<th><strong> Fecha Creaci&oacute;n </strong></th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<td><strong>%s</strong></td>
						<td>%s</td>
						<td>%s</td>
					</tr>
				</tbody>
			</table>
			<br />
			""" %\
			(
				folioStr,
				taller,
				fechaRegistro.strftime("%d/%m/%Y %H:%M:%S")
			)
	body += """
			<br />
			<h2> <strong> %s </strong>  </h2>
			<br />
			""" %\
			(
				cierre
				)
	body += tablaDetalle
	body += mailHtmlFooter()

	for envioEmail in envioEmails:
		mail(header, body, envioEmail.email)

	return True

def mailHtmlIFA(request, folio):
	# Mail InventariofisicoAjuste
	#print "IFA****"
	#print folio
	idfolio= int(folio)
	inventario = InventarioFisico.objects.values(
											"folio",
											"fechaRegistro",
											"tallerAsignado__nombre",
											"inventariofisicodetalle__pesoExistencia",
											"inventariofisicodetalle__pesoFisico",
											"inventariofisicodetalle__diferencia",
											"inventariofisicodetalle__material__nombre"
										)\
										.filter(
											id = idfolio,
											tallerAsignado_id = request.session['idTaller']
										)\
										.distinct()\
										.order_by("inventariofisicodetalle__material__id")
	tablaDetalle = ''
	tablaDetalle += """\
					
					<table rules="all" style="border-color: #666;" cellpadding="10">
						<thead>
							<tr style='background: #66cc00;'>
								<th>Material</th>
								<th>Peso existencia en el sistema</th>
								<th>Peso existencias f&iacute;sicas</th>
								<th>Diferencia</th>
							</tr>
						</thead>
						<tbody>\
						"""

	for rem in inventario:
		tablaDetalle += """\
							<tr>
								<td>%s</td>
								<td>%d</td>
								<td>%d</td>
								<td>%d</td>
							</tr>
						"""%\
						(
							rem["inventariofisicodetalle__material__nombre"],
							rem["inventariofisicodetalle__pesoExistencia"],
							rem["inventariofisicodetalle__pesoFisico"],
							rem["inventariofisicodetalle__diferencia"]
						)

	tablaDetalle += """\
						</tbody>
					</table>
					<br />\
					"""

	folioStr = inventario[0]["folio"]
	taller = inventario[0]["tallerAsignado__nombre"]
	fechaRegistro = inventario[0]["fechaRegistro"]

	envioEmails = User.objects.all().filter(taller__id = request.session['idTaller'])
	header = "INVENTARIO FISICO"
	body = ""
	body += mailHtmlHeader(request)
	body += """
			<br />
			<table rules="all" style="border-color: #666;" cellpadding="10">
				<thead>
					<tr style='background:#66cc00;'>
						<th><strong> Folio </strong></th>
						<th><strong> Taller de Habilitado </strong></th>
						<th><strong> Fecha Creaci&oacute;n </strong></th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<td><strong>%s</strong></td>
						<td>%s</td>
						<td>%s</td>
					</tr>
				</tbody>
			</table>
			<br />
			""" %\
			(
				folioStr,
				taller,
				fechaRegistro.strftime("%d/%m/%Y %H:%M:%S")
			)
	body += tablaDetalle
	body += mailHtmlFooter()

	for envioEmail in envioEmails:
		mail(header, body, envioEmail.email)

	return True


def mail(header, body, to):
	try:
		send_mail(header, body, 'control-acero@grupohi.mx',
		    [to], html_message=body, fail_silently=False)
	except:
		return True;

def excelReportes(request, array):
	x=0;
	y=0;
	random = uuid.uuid4().hex[:6].lower()
	filename = "Suministro_%s" % random
	ext = ".xlsx"
	path = "control_acero/static/excel/"
	workbook = xlsxwriter.Workbook(filename+ext)
	worksheet = workbook.add_worksheet()
	bold14 = workbook.add_format({'bold': True, 'font_size': 12, 'align': 'center'})
	worksheet.set_column('A:J', 25)
	#worksheet.set_column('B:B', 25)
	
	merge_format = workbook.add_format({
	    'bold': 1,
	    'border': 1,
	    'font_size': 18,
	    'align': 'center',
	    'valign': 'vcenter'})

	titulo_format = workbook.add_format({
	    'bold': True,
	    'border': 3,
	    'font_size': 25,
	    'align': 'center',
	    'valign': 'vcenter',
	    'fg_color': 'green'})

	if array["entrada"][0]["excel"] == 6: #Proveedor Habilitado
		
		worksheet.merge_range('A1:J1', 'Tren InterUrbano Mexico Toluca', titulo_format)
		worksheet.merge_range('A2:J2', array["data"][0]["proveedor"], merge_format)
		worksheet.merge_range('A3:J3', 'Registros de Entrada de Fabricantes de Acero', merge_format)
		##print array["entrada"][0]["proveedor"]
		worksheet.write('A4', 'Folio', bold14)
		worksheet.write('B4', 'Fabricante de Acero', bold14)
		worksheet.write('C4', 'Taller de Habilitado', bold14)
		worksheet.write('D4', 'Num. de Orden', bold14)
		worksheet.write('E4', 'Remision', bold14)
		worksheet.write('F4', 'Varilla', bold14)
		worksheet.write('G4', 'Piezas', bold14)
		worksheet.write('H4', 'Longitud Mts', bold14)
		worksheet.write('I4', 'Fecha de Remision', bold14)
		worksheet.write('J4', 'Peso Recibido en Kg', bold14)
		row = 4
		col = 0
		for res in array["entrada"]:
			
			
			worksheet.write(row, col, res["folio"])
			worksheet.write(row, col + 1, res["proveedor"])
			worksheet.write(row, col + 2, res["taller"])
			worksheet.write(row, col + 3, res["orden"])
			worksheet.write(row, col + 4, res["remision"])
			worksheet.write(row, col + 5, res["material"])
			worksheet.write(row, col + 6, int(res["piezas"]))
			worksheet.write(row, col + 7, res["longitud"])
			worksheet.write(row, col + 8, res["fechaR"])
			worksheet.write(row, col + 9, res["peso"])
			row += 1

		row+=3
		worksheet.merge_range('A'+str(row)+':H'+str(row),'Registros de Salida de Acero Habilitado', merge_format)
		row+=1
		worksheet.write('A'+str(row), 'Folio', bold14)
		worksheet.write('B'+str(row), 'Taller de Habilitado', bold14)
		worksheet.write('C'+str(row), 'Fecha de Envio', bold14)
		worksheet.write('D'+str(row), 'Frente', bold14)
		worksheet.write('E'+str(row), 'Apoyo', bold14)
		worksheet.write('F'+str(row), 'Elemento', bold14)
		worksheet.write('G'+str(row), 'Varilla', bold14)
		worksheet.write('H'+str(row), 'Peso de Habilitado en Kg', bold14)

		for salida in array["data"]:

			worksheet.write(row, col, salida["folio"])
			worksheet.write(row, col + 1, salida["taller"])
			worksheet.write(row, col + 2, salida["fechaR"])
			worksheet.write(row, col + 3, salida["frente"])
			worksheet.write(row, col + 4, salida["apoyo"])
			worksheet.write(row, col + 5, salida["elemento"])
			worksheet.write(row, col + 6, salida["material"])
			worksheet.write(row, col + 7, salida["cantidad"])
			row += 1

		row+=3
		worksheet.merge_range('A'+str(row)+':B'+str(row),'Pesos Totales por Varilla', merge_format)
		worksheet.merge_range('E'+str(row)+':F'+str(row),'Pesos Totales de Varilla Habilitada', merge_format)
		row+=1
		worksheet.write('A'+str(row), 'Varilla', bold14)
		worksheet.write('B'+str(row), 'Peso Total en Kg', bold14)
		worksheet.write('E'+str(row), 'Varilla', bold14)
		worksheet.write('F'+str(row), 'Peso Total en Kg', bold14)
		z=0
		for total in array["totales"]:
			worksheet.write(row, col, total["nombre"])
			x+=total["peso"]
			worksheet.write(row, col + 1, total["peso"])
			row+=1
			z+=1
		row= row-z
		for  tot in array["totalesS"]:
			
			worksheet.write(row, col + 4, tot["nombre"])
			y+=tot["peso"]
			worksheet.write(row, col + 5, tot["peso"])	
			row+=1
		row+=2
		#worksheet.set_column('A:J', 20)
		worksheet.write(row, col, 'Peso Total de Acero',bold14)
		worksheet.write(row, col + 1, x)
		worksheet.write(row, col + 2, 'Kg',bold14)

		worksheet.write(row, col + 4, 'Peso Total de Habilitado', bold14)
		worksheet.write(row, col + 5, y)
		worksheet.write(row, col + 6, 'Kg',bold14)


	if array["entrada"][0]["excel"] == 5: #Taller del Habilitador
		
		worksheet.merge_range('A1:J1', 'Tren InterUrbano Mexico Toluca', titulo_format)
		worksheet.merge_range('A2:J2', array["data"][0]["taller"], merge_format)
		##print array["entrada"][0]["proveedor"]
		worksheet.merge_range('A3:J3', 'Registros de Entrada de Fabricantes de Acero', merge_format)
		worksheet.write('A4', 'Folio', bold14)
		worksheet.write('B4', 'Fabricante de Acero', bold14)
		worksheet.write('C4', 'Taller de Habilitado', bold14)
		worksheet.write('D4', 'Num. de Orden', bold14)
		worksheet.write('E4', 'Remision', bold14)
		worksheet.write('F4', 'Varilla', bold14)
		worksheet.write('G4', 'Piezas', bold14)
		worksheet.write('H4', 'Longitud Mts', bold14)
		worksheet.write('I4', 'Fecha de Remision', bold14)
		worksheet.write('J4', 'Peso Recibido en Kg', bold14)
		row = 4
		col = 0
		for res in array["entrada"]:
			
			
			worksheet.write(row, col, res["folio"])
			worksheet.write(row, col + 1, res["proveedor"])
			worksheet.write(row, col + 2, res["taller"])
			worksheet.write(row, col + 3, res["orden"])
			worksheet.write(row, col + 4, res["remision"])
			worksheet.write(row, col + 5, res["material"])
			worksheet.write(row, col + 6, int(res["piezas"]))
			worksheet.write(row, col + 7, res["longitud"])
			worksheet.write(row, col + 8, res["fechaR"])
			worksheet.write(row, col + 9, res["peso"])
			row += 1

		row+=3
		worksheet.merge_range('A'+str(row)+':H'+str(row),'Registros de Salida de Acero Habilitado', merge_format)
		row+=1
		worksheet.write('A'+str(row), 'Folio', bold14)
		worksheet.write('B'+str(row), 'Taller de Habilitado', bold14)
		worksheet.write('C'+str(row), 'Fecha de Envio', bold14)
		worksheet.write('D'+str(row), 'Frente', bold14)
		worksheet.write('E'+str(row), 'Apoyo', bold14)
		worksheet.write('F'+str(row), 'Elemento', bold14)
		worksheet.write('G'+str(row), 'Varilla', bold14)
		worksheet.write('H'+str(row), 'Peso de Habilitado en Kg', bold14)

		for salida in array["data"]:

			worksheet.write(row, col, salida["folio"])
			worksheet.write(row, col + 1, salida["taller"])
			worksheet.write(row, col + 2, salida["fechaR"])
			worksheet.write(row, col + 3, salida["frente"])
			worksheet.write(row, col + 4, salida["apoyo"])
			worksheet.write(row, col + 5, salida["elemento"])
			worksheet.write(row, col + 6, salida["material"])
			worksheet.write(row, col + 7, salida["cantidad"])
			row += 1

		row+=3
		worksheet.merge_range('A'+str(row)+':B'+str(row),'Pesos Totales por Varilla', merge_format)
		worksheet.merge_range('E'+str(row)+':F'+str(row),'Pesos Totales de Varilla Habilitada', merge_format)
		row+=1
		worksheet.write('A'+str(row), 'Varilla', bold14)
		worksheet.write('B'+str(row), 'Peso Total en Kg', bold14)
		worksheet.write('E'+str(row), 'Varilla', bold14)
		worksheet.write('F'+str(row), 'Peso Total en Kg', bold14)
		z=0
		for total in array["totales"]:
			worksheet.write(row, col, total["nombre"])
			x+=total["peso"]
			worksheet.write(row, col + 1, total["peso"])
			row+=1
			z+=1
		row= row-z
		for  tot in array["totalesS"]:
			
			worksheet.write(row, col + 4, tot["nombre"])
			y+=tot["peso"]
			worksheet.write(row, col + 5, tot["peso"])	
			row+=1
		row+=2+z/2
		#worksheet.set_column('A:J', 20)

		worksheet.write(row, col, 'Peso Total de Acero en Kg',bold14)
		worksheet.write(row, col + 1, x)

		worksheet.write(row, col + 4, 'Peso Total de Habilitado en Kg', bold14)
		worksheet.write(row, col + 5, y)
	workbook.close()
	return filename

def excelReportesEntrada(request,array):
	x=0;
	faltante=0;
	real=0;
	random = uuid.uuid4().hex[:6].lower()
	filename = "Suministro_%s" % random
	ext = ".xlsx"
	path = "control_acero/static/excel/"
	workbook = xlsxwriter.Workbook(filename+ext)
	worksheet = workbook.add_worksheet()
	bold14 = workbook.add_format({'bold': True, 'font_size': 12, 'align': 'center'})
	worksheet.set_column('A:I', 20)
	#worksheet.set_column('B:B', 25)
	
	merge_format = workbook.add_format({
	    'bold': 1,
	    'border': 1,
	    'font_size': 18,
	    'align': 'center',
	    'valign': 'vcenter'})

	titulo_format = workbook.add_format({
	    'bold': True,
	    'border': 3,
	    'font_size': 25,
	    'align': 'center',
	    'valign': 'vcenter',
	    'fg_color': 'green'})

	if array["data"][0]["excel"] == 0: #Inventario Fisico
		#print "reporte inventario"
		worksheet.merge_range('A1:G1', 'Tren InterUrbano Mexico Toluca', titulo_format)
		worksheet.merge_range('A2:G2', array["data"][0]["proveedor"], merge_format)
		worksheet.merge_range('A3:G3', 'Inventarios Fisicos', merge_format)

		worksheet.write('A4', 'Folio', bold14)
		worksheet.write('B4', 'Taller', bold14)
		worksheet.write('C4', 'Fecha de Registro', bold14)
		worksheet.write('D4', 'Material', bold14)
		worksheet.write('E4', 'Peso en Sistema', bold14)
		worksheet.write('F4', 'Peso Fisico Ingresado', bold14)
		worksheet.write('G4', 'Diferencia', bold14)
		row = 4
		col = 0

		for res in array["data"]:
		
			worksheet.write(row, col, res["folio"])
			worksheet.write(row, col + 1, res["taller"])
			worksheet.write(row, col + 2, res["fechaR"])
			worksheet.write(row, col + 3, res["material"])
			worksheet.write(row, col + 4, res["existencia"])
			worksheet.write(row, col + 5, res["fisico"])
			worksheet.write(row, col + 6, res["diferencia"])
			row += 1

			

	if array["data"][0]["excel"] == 1: #fabricante de acero
		worksheet.merge_range('A1:I1', 'Tren InterUrbano Mexico Toluca', titulo_format)
		worksheet.merge_range('A2:I2', array["data"][0]["proveedor"], merge_format)
		worksheet.merge_range('A3:I3', 'Registros de Entrada de Fabricantes de Acero', merge_format)

		worksheet.write('A4', 'Folio', bold14)
		worksheet.write('B4', 'Taller de Habilitado', bold14)
		worksheet.write('C4', 'Num. de Orden', bold14)
		worksheet.write('D4', 'Remision', bold14)
		worksheet.write('E4', 'Varilla', bold14)
		worksheet.write('F4', 'Piezas', bold14)
		worksheet.write('G4', 'Longitud Mts', bold14)
		worksheet.write('H4', 'Fecha de Remision', bold14)
		worksheet.write('I4', 'Peso Recibido en Kg', bold14)
		row = 4
		col = 0

		for res in array["data"]:
			##print res
			#worksheet.write('A1', res["proveedor"], bold14)
			worksheet.write(row, col, res["folio"])
			worksheet.write(row, col + 1, res["taller"])
			worksheet.write(row, col + 2, res["orden"])
			worksheet.write(row, col + 3, res["remision"])
			worksheet.write(row, col + 4, res["material"])
			worksheet.write(row, col + 5, int(res["piezas"]))
			worksheet.write(row, col + 6, res["longitud"])
			worksheet.write(row, col + 7, res["fechaR"])
			worksheet.write(row, col + 8, res["peso"])
			row += 1

		
		row+=3
		worksheet.merge_range('A'+str(row)+':B'+str(row),'Pesos Totales por Varilla', merge_format)
		row+=1
		worksheet.write('A'+str(row), 'Varilla', bold14)
		worksheet.write('B'+str(row), 'Peso Total en Kg', bold14)
		

		for total in array["totales"]:
			worksheet.write(row, col, total["nombre"])
			x += total["peso"]
			worksheet.write(row, col + 1, total["peso"])
			row +=1
		row += 2
		
		worksheet.write(row, col, 'Peso Total de Acero')
		worksheet.write(row, col + 1, x)
		worksheet.write(row, col + 2, 'Kg')

	elif array["data"][0]["excel"] == 2:  #Fabricante de acero y Taller de Habilitado

		worksheet.merge_range('A1:H1', 'Tren InterUrbano Mexico Toluca', titulo_format)
		worksheet.merge_range('A2:H2', array["data"][0]["proveedor"]+' - '+array["data"][0]["taller"], merge_format)
		worksheet.merge_range('A3:H3', 'Registros de Entrada de Fabricantes de Acero', merge_format)
		worksheet.write('A4', 'Folio', bold14)
		worksheet.write('B4', 'Num. de Orden', bold14)
		worksheet.write('C4', 'Remision', bold14)
		worksheet.write('D4', 'Varilla', bold14)
		worksheet.write('E4', 'Piezas', bold14)
		worksheet.write('F4', 'Longitud Mts', bold14)
		worksheet.write('G4', 'Fecha de Remision', bold14)
		worksheet.write('H4', 'Peso Recibido en Kg', bold14)
		row = 4
		col = 0

		for res in array["data"]:
			
			worksheet.write(row, col, res["folio"])
			worksheet.write(row, col + 1, res["orden"])
			worksheet.write(row, col + 2, res["remision"])
			worksheet.write(row, col + 3, res["material"])
			worksheet.write(row, col + 4, int(res["piezas"]))
			worksheet.write(row, col + 5, res["longitud"])
			worksheet.write(row, col + 6, res["fechaR"])
			worksheet.write(row, col + 7, res["peso"])
			row += 1

		
		row+=3
		worksheet.merge_range('A'+str(row)+':B'+str(row),'Pesos Totales por Varilla', merge_format)
		row+=1
		worksheet.write('A'+str(row), 'Varilla', bold14)
		worksheet.write('B'+str(row), 'Peso Total en Kg', bold14)
		

		for total in array["totales"]:
			worksheet.write(row, col, total["nombre"])
			x += total["peso"]
			worksheet.write(row, col + 1, total["peso"])
			row += 1;
		row += 2
		
		worksheet.write(row, col, 'Peso Total de Acero', bold14)
		worksheet.write(row, col + 1, x)
		worksheet.write(row, col + 2, 'Kg', bold14)


	elif array["data"][0]["excel"] == 3: #elif Armador

		worksheet.merge_range('A1:H1', 'Tren InterUrbano Mexico Toluca', titulo_format)
		worksheet.merge_range('A2:H2', array["data"][0]["proveedor"], merge_format)
		worksheet.merge_range('A3:H3', 'Recepcion completa', merge_format)
		worksheet.write('A4', 'Folio', bold14)
		worksheet.write('B4', 'Remision', bold14)
		worksheet.write('C4', 'Frente', bold14)
		worksheet.write('D4', 'Apoyo', bold14)
		worksheet.write('E4', 'Elemento', bold14)
		worksheet.write('F4', 'Material', bold14)
		worksheet.write('G4', 'Fecha de Remision', bold14)
		worksheet.write('H4', 'Peso Recibido en Kg', bold14)
		row = 4
		col = 0
		aux=0
		cant=0;
		fal=0
		real=0
		i=0
		flag=0
		idMaterial =0;
		
		for res in array["data"]:
			if res["cantidad"]== res["cantidadReal"]:
				worksheet.write(row, col, res["folio"])
				worksheet.write(row, col + 1, res["remision"])
				worksheet.write(row, col + 2, res["frente"])
				worksheet.write(row, col + 3, res["apoyo"])
				worksheet.write(row, col + 4, res["elemento"])
				worksheet.write(row, col + 5, res["material"])
				worksheet.write(row, col + 6, res["fechaR"])
				worksheet.write(row, col + 7, res["cantidad"])
				cant= cant + res["cantidad"]
			else:
				row= row-1
			row += 1	
		row+=3
		worksheet.merge_range('A'+str(row)+':H'+str(row),'Pesos Faltantes', merge_format)
		row+=1
		worksheet.write('A'+str(row), 'Folio', bold14)
		worksheet.write('B'+str(row), 'Apoyo', bold14)
		worksheet.write('C'+str(row), 'Elemento', bold14)
		worksheet.write('D'+str(row), 'Material', bold14)
		worksheet.write('E'+str(row), 'Nomenclatura', bold14)
		worksheet.write('F'+str(row), 'Longitud', bold14)
		worksheet.write('G'+str(row), 'Piezas', bold14)
		worksheet.write('H'+str(row), 'Peso Faltante en Kg', bold14)
		
		for res in array["data"]:
			if res["cantidad"]!= res["cantidadReal"]:
				worksheet.write(row, col, res["folio"])
				worksheet.write(row, col + 1, res["apoyo"])
				worksheet.write(row, col + 2, res["elemento"])
				worksheet.write(row, col + 3, res["material"])
				worksheet.write(row, col + 4, res["nomenclatura"])
				worksheet.write(row, col + 5, res["longitud"])
				worksheet.write(row, col + 6, res["piezas"])
				worksheet.write(row, col + 7, int(res["cantidad"]))
				
				fal= fal + int(res["cantidad"])
				#print "*******"
				#print flag
				#worksheet.write(row, col + 9, int(res["cantidadReal"]))
				if flag == res["cantidadReal"]:
					if i==0:
						#worksheet.write(row, col + 8, int(flag))
						real= real + int(flag)
					i+=1
					
				else:
					i=0

				flag=int(res["cantidadReal"])
					#real= real+ int(res["cantidadReal"])
					
					

			else:
				row=row-1

			row += 1
		row += 3
		worksheet.merge_range('A'+str(row)+':B'+str(row),'Resumen de Pesos Totales', merge_format)
		row += 1
		worksheet.write('A'+str(row), 'Peso Recibido en Kg', bold14)
		worksheet.write('B'+str(row), 'Peso Faltante en Kg', bold14)
		#print "****"
		#print real

		real=cant + (real-fal)
		worksheet.write(row, col, real)
		worksheet.write(row, col + 1, fal)

		
	elif array["data"][0]["excel"] == 4: #elif Frente de Trabajo

		worksheet.merge_range('A1:H1', 'Tren InterUrbano Mexico Toluca', titulo_format)
		worksheet.merge_range('A2:H2', array["data"][0]["frente"], merge_format)
		worksheet.merge_range('A3:H3', 'Recepcion completa', merge_format)
		worksheet.write('A4', 'Folio', bold14)
		worksheet.write('B4', 'Remision', bold14)
		worksheet.write('C4', 'Frente', bold14)
		worksheet.write('D4', 'Apoyo', bold14)
		worksheet.write('E4', 'Elemento', bold14)
		worksheet.write('F4', 'Material', bold14)
		worksheet.write('G4', 'Fecha de Registro', bold14)
		worksheet.write('H4', 'Peso Recibido en Kg', bold14)
		row = 4
		col = 0
		aux=0
		cant=0;
		fal=0
		flag=0
		real=0
		idMaterial =0;
		
		for res in array["data"]:
			if res["cantidad"]== res["cantidadReal"]:
				worksheet.write(row, col, res["folio"])
				worksheet.write(row, col + 1, res["remision"])
				worksheet.write(row, col + 2, res["frente"])
				worksheet.write(row, col + 3, res["apoyo"])
				worksheet.write(row, col + 4, res["elemento"])
				worksheet.write(row, col + 5, res["material"])
				worksheet.write(row, col + 6, res["fechaR"])
				worksheet.write(row, col + 7, res["cantidad"])
				cant= cant + res["cantidad"]
			else:
				row= row-1
			row += 1	
		
		row += 2
		worksheet.merge_range('A'+str(row)+':H'+str(row),'Pesos Faltantes', merge_format)
		row+=1
		worksheet.write('A'+str(row), 'Folio', bold14)
		worksheet.write('B'+str(row), 'Apoyo', bold14)
		worksheet.write('C'+str(row), 'Elemento', bold14)
		worksheet.write('D'+str(row), 'Material', bold14)
		worksheet.write('E'+str(row), 'Nomenclatura', bold14)
		worksheet.write('F'+str(row), 'Longitud', bold14)
		worksheet.write('G'+str(row), 'Piezas', bold14)
		worksheet.write('H'+str(row), 'Peso Faltante en Kg', bold14)
		
		for res in array["data"]:
			if res["cantidad"]!= res["cantidadReal"]:
				worksheet.write(row, col, res["folio"])
				worksheet.write(row, col + 1, res["apoyo"])
				worksheet.write(row, col + 2, res["elemento"])
				worksheet.write(row, col + 3, res["material"])
				worksheet.write(row, col + 4, res["nomenclatura"])
				worksheet.write(row, col + 5, res["longitud"])
				worksheet.write(row, col + 6, res["piezas"])
				worksheet.write(row, col + 7, int(res["cantidad"]))
				fal= fal + int(res["cantidad"])

				#worksheet.write(row, col + 9, int(res["cantidadReal"]))
				if flag == res["cantidadReal"]:
					if i==0:
						#worksheet.write(row, col + 8, int(flag))
						real= real + int(flag)
					i+=1
					
				else:
					i=0

				flag=int(res["cantidadReal"])
					#real= real+ int(res["cantidadReal"])
					
			else:
				row=row-1
			row += 1	
		row += 3
		
		worksheet.merge_range('A'+str(row)+':B'+str(row),'Resumen de Pesos Totales', merge_format)
		row += 1
		worksheet.write('A'+str(row), 'Peso Recibido en Kg', bold14)
		worksheet.write('B'+str(row), 'Peso Faltante en Kg', bold14)
		row+=1
		real=cant + (real-fal)
		worksheet.write(row, col, real)
		worksheet.write(row, col + 1, fal)

	workbook.close()
	return filename

def descargaExcel(request, filename):
	path = "control_acero/static/excel/"
	ext = ".xlsx"
	excel = open(filename + ext, "rb")
	output = StringIO.StringIO(excel.read())
	out_content = output.getvalue()
	output.close()
	response = HttpResponse(out_content,content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
	response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % filename
	return response

@login_required(login_url='/control_acero/usuario/login/') 
def eliminarView(request):
	template = 'control_acero/eliminar/eliminacionFolio.html'
	return render(request, template)

def buscarFolio(request):
	array = {}
	mensaje = {}
	data = []
	folio = request.POST.get('folio', 0)
	e = request.POST.get('estatus', 0)
	e = int(e)
	cad=folio[:3]
	idDesc=0
	idSal=0
	estado=0
	taller=request.session['idTaller']
	frente=request.session['idFrente']
	print taller
	print frente

	if taller!=0 and cad == 'RMH':
		print "recepcion de material"
		r = RemisionDetalle.objects.values("id", 
								   			"remision_id",
											"folio", 
											"remision__idOrden",
											"remision__remision",
											"remision__pesoNeto",
											"remision__tallerAsignado__nombre",
											"remision__funcion__proveedor",
											"material__nombre",
											"peso",
											"cantidad",
											"longitud")\
											.filter(folio=folio, estatus=1, estatusInventario=0, remision__tallerAsignado_id = request.session['idTaller'] ).distinct()

		
		print "****"
		
		print len(r)
		if len(r) == 0:
			mensaje = {"mensaje":"No se encontro el folio buscado o ya fué eliminado."}
			array["mensaje"] = mensaje
			array["data"]=data
			return JsonResponse(array)
		else:	
			d = DescuentoSalida.objects.values("id",
											"salida_id",
											"estatus").filter(inventarioRemisionDetalle__remision__id = r[0]["remision_id"])					
			
			#print d.query
			

			if len(d) != 0 and d[0]["estatus"] == 1:
				estado=d[0]["estatus"]
				idDesc=d[0]["id"]
				idSal=d[0]["salida_id"]
				
				mensaje = {"mensaje":"No se puede eliminar este folio, el material de este folio ya fué habilitado"}
				array["mensaje"] = mensaje
				array["data"]=data
				return JsonResponse(array)
				
			else:
				
				
				for f in r:
					resultado = {
							"modulo":1,
							"id":f["id"],
							"folio":f["folio"],
							"remid": f["remision_id"],
							"idOrden":f["remision__idOrden"],
							"remision":f["remision__remision"],
							"pesoNeto":f["remision__pesoNeto"],
							"funcion":f["remision__funcion__proveedor"],
							"material":f["material__nombre"],
							"peso":f["peso"],
							"cantidad":f["cantidad"],
							"longitud":f["longitud"],
							"taller":f["remision__tallerAsignado__nombre"],
							}
					data.append(resultado)	

				print e
				if e == 1:
					print "elimina"
					Remision.objects.filter( id = r[0]["remision_id"]).update(estatus=0)
					RemisionDetalle.objects.filter(folio = r[0]["folio"]).update(estatus=0)
					InventarioRemisionDetalle.objects.filter(folio=folio).update(estatus=0)
					bitacora = Bitacora.objects.create(accion="Eliminación de Folio Recepcion Taller", id_afectado=r[0]["remision_id"], observacion="Cambio de estatus en folio remision", estatus=1, modulo_id=6, user_id=request.user.id)
	
	if taller!= 0 and cad == 'SMH':
		print "Salida de material"

		salida=Salida.objects.values("id",
										"cantidadAsignada",
										"folio",
										"apoyo__numero",
										"frente__nombre",
										"material__nombre",
										"elemento__nombre",
										"tallerAsignado__nombre"
										)\
								.filter(folio=folio,
										estatus=1, estatusInventario=0, tallerAsignado_id = request.session['idTaller']).distinct()
		for s in salida:
			resultado={
					"modulo":2,
					"id":s["id"],
					"cantidadAsignada":s["cantidadAsignada"],
					"folio":s["folio"],
					"apoyo":s["apoyo__numero"],
					"frente":s["frente__nombre"],
					"material":s["material__nombre"],
					"elemento":s["elemento__nombre"],
					"taller":s["tallerAsignado__nombre"]
			}
			data.append(resultado)

		if e == 1:
			print "elimina"
			for s in salida:
				descuente=DescuentoSalida.objects.values(
															"id",
															"inventarioRemisionDetalle_id",
															"salida_id",
															"pesoSalida",
															"pesoRemision",
															"inventarioRemisionDetalle__material__nombre",
															"inventarioRemisionDetalle__peso"
														)\
														.filter(estatus=1, salida_id=s["id"])

				for des in descuente:
					print des
					pesoReal=int(des["inventarioRemisionDetalle__peso"])+int(des["pesoSalida"])
					InventarioRemisionDetalle.objects.filter(id=des["inventarioRemisionDetalle_id"]).update(peso=pesoReal, estatusTotalizado = 1)
					DescuentoSalida.objects.filter(id=des["id"]).update(estatus=0)
					Salida.objects.filter(id=des["salida_id"]).update(estatus=0)
					InventarioSalida.objects.filter(folio=folio).update(estatus=0)
					bitacora = Bitacora.objects.create(accion="Eliminación de Folio Salida Taller", id_afectado=des["salida_id"], observacion="Cambio de estatus en folio salida", estatus=1, modulo_id=7, user_id=request.user.id)											
	
	if frente!=0 and cad == 'EMA':
		print "Recepcion en Frente de trabajo"

		entrada=Entrada.objects.values( 
										"id",
										"folio",
										"folioSalida",
										"material__id",
										"material__nombre",
										"funcion__proveedor",
										"frente__nombre",
										"elemento__nombre",
										"apoyo__numero",
										"remision",
										"cantidadReal"
										)\
										.filter(folio=folio, estatus=1, frente_id = request.session['idFrente'])\
										.annotate(cantidadAsignada = Sum('cantidadAsignada'))\
										.order_by("material__id")\
										.distinct()

		for ent in entrada:
			resultado={
				"modulo":3,
				"id":ent["id"],
				"folio":ent["folio"],
				"folioSalida":ent["folioSalida"],
				"material":ent["material__nombre"],
				"proveedor":ent["funcion__proveedor"],
				"frente":ent["frente__nombre"],
				"elemento":ent["elemento__nombre"],
				"apoyo":ent["apoyo__numero"],
				"remision":ent["remision"],
				"cantidad":ent["cantidadAsignada"],
				"cantidadR":ent["cantidadReal"]
			}
			data.append(resultado)

		print e
		if e == 1:
			print "elimina"
			Entrada.objects.filter(folio=folio).update(estatus=0)
			EntradaDetalle.objects.filter(entrada__folio =folio).update(estatus=0)
			for ex in entrada:
				print "cambio de recepcion pendiente"
				InventarioSalida.objects.filter(folio=ex["folioSalida"],material_id=ex["material__id"]).update(estatusTotalizado=1, cantidadAsignada=ex["cantidadReal"])
			bitacora = Bitacora.objects.create(accion="Eliminación de Folio Recepción en Frente", id_afectado=entrada[0]["id"], observacion="Cambio de estatus en folio entrada", estatus=1, modulo_id=8, user_id=request.user.id)
	
	else:
		mensaje = {"mensaje":"Folio Incorrecto"}
		
	array["mensaje"] = mensaje
	array["data"]=data
	return JsonResponse(array)
