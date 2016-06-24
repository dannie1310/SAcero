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
from django.contrib.auth.models import User, Permission, Group
from django.template import RequestContext
from django.contrib.staticfiles.templatetags.staticfiles import static
import xlsxwriter
import StringIO

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
	print dateFormat
	#mensaje = {"estatus":"ok", "folio":numFolio, "date":dateFormat}
	mensaje = {"date":dateFormat}
	array = mensaje
	return JsonResponse(array)

def getTallerAsignado(request, taller):
	taller = Taller.objects.filter(id = taller).order_by()
	if taller.exists():
		request.session['idTaller'] = taller[0].id
		request.session['nombreTaller'] = taller[0].nombre
		request.session['proveedorTaller'] = taller[0].proveedor
		request.session['ubicacionTaller'] = taller[0].ubicacion
		request.session['responsableTaller'] = taller[0].responsable
	else:
		request.session['idTaller'] = 0
		request.session['nombreTaller'] = 0
		request.session['proveedorTaller'] = 0
		request.session['ubicacionTaller'] = 0
		request.session['responsableTaller'] = 0

def getFrenteAsignado(request, frente):
	frente = Frente.objects.filter(id = frente).order_by()
	if frente.exists():
		request.session['idFrente'] = frente[0].id
		request.session['nombreFrente'] = frente[0].nombre
		request.session['identificacionFrente'] = frente[0].identificacion
		request.session['ubicacionFrente'] = frente[0].ubicacion
	else:
		request.session['idFrente'] = 0
		request.session['nombreFrente'] = 0
		request.session['identificacionFrente'] = 0
		request.session['ubicacionFrente'] = 0

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

def usuariosEditView(request, pk):
	usuario = get_object_or_404(User, pk=pk)
	if request.method == "POST":
		# for key in request.POST:
		#     print(key)
		#     value = request.POST[key]
		#     print(value)
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
	return render(request,'control_acero/catalogos/elementos/elementos.html', {"elementos": elementos})

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
	return render(request,'control_acero/catalogos/despieces/despiece.html', {"despieces": despieces})

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
	return render(request,'control_acero/catalogos/materiales/material.html', {"materiales": materiales})

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
	return render(request,'control_acero/catalogos/frentes/frente.html', {"frentes": frentes})

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

def funcionesNewView(request):
	if request.method == "POST":
		form = FuncionForm(request.POST)
		print form
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
	return render(request,'control_acero/catalogos/talleres/taller.html', {"talleres": talleres})

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

def inventario(request):
	inventario_list = InventarioFisico.objects.filter(estatus=1)
	paginator = Paginator(inventario_list, 10)
	page = request.GET.get('page')
	try:
		inventario = paginator.page(page)
	except PageNotAnInteger:
		inventario = paginator.page(1)
	except EmptyPage:
		inventario = paginator.page(paginator.num_pages)
	return render(request,'control_acero/inventario/inventario.html', {"inventario": inventario})

def inventarioFisicoEditView(request, pk):
	inventario = get_object_or_404(InventarioFisico, pk=pk)
	inventarioDetalle = InventarioFisicoDetalle.objects.filter(inventarioFisico_id=inventario.id);
	template = 'control_acero/inventario/inventarioFisicoEdit.html'
	#inventario = InventarioFisico.objects.filter(id=pk, estatus=1)
	return render(request, template, {"inventario": inventario, "detalles": inventarioDetalle})
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
						estatus=1,
						tallerAsignado_id=request.session['idTaller']
						)
	folio = RemisionDetalle.objects.all().filter(remision__tallerAsignado_id=request.session["idTaller"]).order_by("-numFolio")[:1]
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
											'factor__pi').filter(id=material)
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
	remisionDetalles = InventarioRemisionDetalle.objects\
						.values(
								'material_id',
								'material__nombre'
								)\
						.annotate(pesoMaterial = Sum('peso'))\
						.annotate(cantidadMaterial = Sum('cantidad'))\
						.filter(peso__gt = 0, remision__tallerAsignado_id = request.session["idTaller"])\
						.order_by('material_id')
	print remisionDetalles.query
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
	numFolio = "%04d" % (numFolioInt,)
	numFolio = "SMH-"+numFolio
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
							.filter(material_id = material, remision__tallerAsignado_id = request.session["idTaller"])
		for remisionDetallesTotal in remisionDetallesTotales:
			if Decimal(remisionDetallesTotal["pesoMaterial"]) >= Decimal(totalAsignado):
				inventarioRemisionDetalles = InventarioRemisionDetalle.objects.all()\
												.filter(material_id = material, estatusTotalizado = 1, remision__tallerAsignado_id = request.session["idTaller"])
				for inventarioRemisionDetalle in inventarioRemisionDetalles:
					inventarioId = inventarioRemisionDetalle.id
					irdpeso = inventarioRemisionDetalle.peso
					if Decimal(irdpeso) <= Decimal(totalAsignado):
						totalAsignado = Decimal(totalAsignado) - Decimal(irdpeso)
						InventarioRemisionDetalle.objects.filter(id=inventarioId).update(peso=0, estatusTotalizado = 0)
						continue

					if Decimal(irdpeso) > Decimal(totalAsignado):
						cantidadRestar = Decimal(irdpeso) - Decimal(totalAsignado)
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
								cantidadReal = cantidadReal,
								cantidadAsignada = cantidadAsignada,
								estatusEtapa = 1,
								folio = numFolio,
								numFolio = numFolioInt,
								tallerAsignado_id = request.session["idTaller"]
								)
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
						.filter(numFolio = folio, frente_id = request.session["idFrente"]) \
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
	folio = Entrada.objects.all().filter(estatusEtapa = 1, frente_id = request.session["idFrente"]).order_by("-numFolio")[:1]
	if folio.exists():
		numFolio = folio[0].numFolio
	numFolioInt = int(numFolio)+1
	numFolio = "%04d" % (numFolioInt,)
	numFolio = "EMA-"+numFolio
	for jsonData in jsonDataInfo:
		material = jsonData["material"]
		cantidadReal = jsonData["cantidadReal"]
		cantidadAsignada = jsonData["cantidadAsignada"]
		bandera = jsonData["bandera"]
		totalAsignado = cantidadAsignada
		inventarioSalidas = InventarioSalida.objects.all()\
										.filter(material_id = material, estatusTotalizado = 1, frente_id = request.session["idFrente"])
		for inventarioSalida in inventarioSalidas:
			inventarioId = inventarioSalida.id
			irdpeso = inventarioSalida.cantidadAsignada

			if Decimal(irdpeso) <= Decimal(totalAsignado):
				totalAsignado = Decimal(totalAsignado) - Decimal(irdpeso)
				InventarioSalida.objects.filter(id=inventarioId).update(cantidadAsignada=0, estatusTotalizado = 0)
				continue

			if Decimal(irdpeso) > Decimal(totalAsignado):
				cantidadRestar = Decimal(irdpeso) - Decimal(totalAsignado)
				InventarioSalida.objects.filter(id=inventarioId).update(cantidadAsignada=cantidadRestar)

		entrada = Entrada.objects\
						.create(
								remision = remision,
								elemento_id = elemento,
								apoyo_id = apoyo,
								material_id = material,
								funcion_id = funcion,
								cantidadReal = cantidadReal,
								cantidadAsignada = cantidadAsignada,
								folio = numFolio,
								numFolio = numFolioInt,
								frente_id = request.session["idFrente"]
								)
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
								cantidadReal = cantidadRealF,
								cantidadAsignada = cantidadAsignadaF,
								folio = numFolio,
								numFolio = numFolioInt,
								frente_id = request.session["idFrente"]
								)
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
	respuesta = request.POST.get('json')
	respuestaRemisiones = request.POST.get('jsonRemisiones')
	respuestaRemisionesInventario = request.POST.get('jsonRemisionesInventario')
	respuestaRemisionesSalidas= request.POST.get('jsonSalidas')

	folio = InventarioFisico.objects.all().filter(tallerAsignado_id = request.session["idTaller"]).order_by("-numFolio")[:1]
	if folio.exists():
		numFolio = folio[0].numFolio
	numFolioInt = int(numFolio)+1
	numFolio = "%04d" % (numFolioInt,)
	numFolio = "LIF-"+numFolio
	inventarioFisico = InventarioFisico.objects\
		.create(
				folio = numFolio,
				numFolio = numFolioInt,
				tallerAsignado_id = request.session["idTaller"]
				)
	json_object = json.loads(respuesta)
	for data in json_object:
		material = data["materialId"]
		pesoExistencia = data["existencias"]
		pesoFisico = data["existenciaFisica"]
		diferencia = data["diferencia"]
		tipo = data["bandera"]
		inventarioFisicoD = InventarioFisicoDetalle.objects\
							.create(
									inventarioFisico_id = inventarioFisico.pk,
									material_id = material,
									pesoExistencia = pesoExistencia,
									pesoFisico = pesoFisico,
									diferencia = diferencia,
									tipoExistencia = tipo,
									)
	json_remisiones = json.loads(respuestaRemisiones)
	for data1 in json_remisiones:
		RemisionDetalle.objects.filter(id=data1).update(estatusInventario=1, folioInventario = numFolioInt)

	json_remisionesInventario = json.loads(respuestaRemisionesInventario)
	for data2 in json_remisionesInventario:
		InventarioRemisionDetalle.objects.filter(id=data2).update(estatusInventario=1, folioInventario = numFolioInt)

	json_salidas = json.loads(respuestaRemisionesSalidas)
	for data3 in json_salidas:
		Salida.objects.filter(id=data3).update(estatusInventario=1, folioInventario = numFolioInt)

	mensaje = {"estatus":"ok", "mensaje":"Entrada de Material Exitosa. Folio: "+numFolio, "folio":numFolio}
	array = mensaje
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
		if folio.exists():
			numFolio = folio[0].numFolio
		numFolioInt = int(numFolio)+1
		numFolio = "%04d" % (numFolioInt,)
		numFolio = "RMH-"+numFolio
	if int(modulo) == 2:
		folio = Salida.objects.all().filter(estatusEtapa = 1, tallerAsignado_id = request.session["idTaller"]).order_by("-numFolio")[:1]
		if folio.exists():
			numFolio = folio[0].numFolio
		numFolioInt = int(numFolio)+1
		numFolio = "%04d" % (numFolioInt,)
		numFolio = "SMH-"+numFolio
	if int(modulo) == 3:
		folio = Entrada.objects.all().filter(estatusEtapa = 1, frente_id = request.session["idFrente"]).order_by("-numFolio")[:1]
		if folio.exists():
			numFolio = folio[0].numFolio
		numFolioInt = int(numFolio)+1
		numFolio = "%04d" % (numFolioInt,)
		numFolio = "EMA-"+numFolio
	if int(modulo) == 4:
		folio = InventarioFisico.objects.all().filter(tallerAsignado_id = request.session["idTaller"]).order_by("-numFolio")[:1]
		if folio.exists():
			numFolio = folio[0].numFolio
		numFolioInt = int(numFolio)+1
		numFolio = "%04d" % (numFolioInt,)
		numFolio = "LIF-"+numFolio

	mensaje = {"estatus":"ok", "folio":numFolio, "date":dateFormat}
	#mensaje = {"estatus":"ok", "folio":numFolio}
	array = mensaje
	return JsonResponse(array)

def foliosSalidaHabilitado(request):
	array = {}
	mensaje = {}
	data = []
	salidaFolios = InventarioSalida.objects.values('folio', 'numFolio', 'apoyo__numero', 'elemento__nombre').distinct().filter(frente_id=request.session['idFrente'])
	for salidaFolio in salidaFolios:
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

#@permission_required('control_acero.add_apoyo')
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

def reporteView(request):
	template = 'control_acero/reportes/reporte.html'
	return render(request, template)

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
	print f
	talleres = Taller.objects.all()\
								.filter(
										funcion_id = f,
										funcion__tipo=2,
										estatus = 1
										)\
								.order_by("funcion_id")
	#print talleres.query
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
	#print talleres.query
	for taller in talleres:
		resultado = {
						"id":taller.id,
						"nombre":taller.nombre
					}
		data.append(resultado)
	array["data"]=data
	return JsonResponse(array)		

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

	fechaInicial = request.POST.get('fechai', '17/05/2016')
	fechaFinal = request.POST.get('fechaf', '14/06/2016')
	fechaInicialFormat = datetime.strptime(fechaInicial+" 00:00:00", '%d/%m/%Y %H:%M:%S')
	fechaFinalFormat = datetime.strptime(fechaFinal+" 23:59:59", '%d/%m/%Y %H:%M:%S')

	print "----------"
	print idFuncion
	print tipo
	print idTaller
	print idFrente
	print fechaInicial
	print fechaFinal

	if idFuncion!='0' and idTaller=='0' and idFrente=='0' and tipo=='1':

		print "Fabricante"

		total = RemisionDetalle.objects.values(	'material__id',
												'material__nombre'		
												).annotate(pesoMaterial = Sum('peso'))\
												.filter(remision__funcion__id =idFuncion,
														fechaRegistro__gte=fechaInicialFormat,
														fechaRegistro__lte=fechaFinalFormat,
														estatus=1)\
												.order_by("material__id")

		print total.query
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
		#print datos.query
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
		excelReportesEntrada(request,array)
		#print array
		return JsonResponse(array)

	if idFuncion!='0' and idTaller!='0' and idFrente=='0' and tipo=='1':

		print "Fabricante y Taller de Habilitado"
		
		total = RemisionDetalle.objects.values(	'material__id',
												'material__nombre'		
												).annotate(pesoMaterial = Sum('peso'))\
												.filter(remision__funcion__id =idFuncion,
														remision__tallerAsignado__id=idTaller,
														fechaRegistro__gte=fechaInicialFormat,
														fechaRegistro__lte=fechaFinalFormat,
														estatus=1)\
												.order_by("material__id")

		print total.query
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
		#print datos.query
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
		excelReportesEntrada(request,array)
		return JsonResponse(array)

	elif idFrente=='0' and idTaller=='0' and idFuncion!='0' and tipo=='3':
		print "elif Armador"
		total = Entrada.objects.values(			
												'material__id',
												'material__nombre',
												'entradadetalle__calculado',
												'cantidadReal'		
												).annotate(pesoMaterial = Sum('cantidadAsignada'))\
												.filter(funcion__id =idFuncion,
														fechaRegistro__gte=fechaInicialFormat,
														fechaRegistro__lte=fechaFinalFormat,
														estatus=1)\
												.order_by("material__id")


		#print total.query
		for x in total:
			
			resultado = {
					"value":1,
					"id":x['material__id'],
					"nombre":x['material__nombre'],
					"peso":x['pesoMaterial'],
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
											'folio',
											'material__id',
											'numFolio',
											'frente__id',
											'frente__nombre',
											'entradadetalle__entrada_id',
											'entradadetalle__calculado',
											'remision').filter( funcion__id =idFuncion,
																fechaRegistro__gte=fechaInicialFormat,
																fechaRegistro__lte=fechaFinalFormat,
																estatus=1).order_by("folio")
		#print armador.query
		for e in armador:
			
			resultado = {	"value": 2,
							"excel":3,
							"id":e['id'],
							"cantidad":e['cantidadAsignada'],
							"proveedor":e['funcion__proveedor'],
							"apoyo":e['apoyo__numero'],
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
							"elemento":e['elemento__nombre']
						}
			data.append(resultado)

		array["data"]=data
		array["totales"]=totales
		#excelReportes(request,array)
		#print array
		return JsonResponse(array)

	elif idFrente!='0' and idTaller=='0' and idFuncion=='0' :
		print "elif Frente de Trabajo"

		total = Entrada.objects.values(			
												'material__id',
												'material__nombre',
												'entradadetalle__calculado',
												'cantidadReal'		
												).annotate(pesoMaterial = Sum('cantidadAsignada'))\
												.filter(frente_id=idFrente,
														fechaRegistro__gte=fechaInicialFormat,
														fechaRegistro__lte=fechaFinalFormat,
														estatus=1)\
												.order_by("material__id")


		print total.query
		for x in total:
			
			resultado = {
					"value":1,
					"id":x['material__id'],
					"nombre":x['material__nombre'],
					"peso":x['pesoMaterial'],
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
											'folio',
											'material__id',
											'numFolio',
											'frente__id',
											'frente__nombre',
											'entradadetalle__entrada_id',
											'entradadetalle__calculado',
											'remision').filter(	frente_id=idFrente,
																fechaRegistro__gte=fechaInicialFormat,
																fechaRegistro__lte=fechaFinalFormat,
																estatus=1).order_by("folio")
		#print armador.query
		for e in armador:
			
			resultado = {	"value": 2,
							"excel":4,
							"id":e['id'],
							"cantidad":e['cantidadAsignada'],
							"proveedor":e['funcion__proveedor'],
							"apoyo":e['apoyo__numero'],
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
							"elemento":e['elemento__nombre']
						}
			data.append(resultado)

		array["data"]=data
		array["totales"]=totales
		#excelReportes(request,array)
		return JsonResponse(array)

	elif idFrente!='0' and idTaller=='0' and idFuncion!='0' and tipo=='3':
		print "Frente de Trabajo y Armador"

		total = Entrada.objects.values(			
												'material__id',
												'material__nombre',
												'entradadetalle__calculado',
												'cantidadReal'		
												).annotate(pesoMaterial = Sum('cantidadAsignada'))\
												.filter(funcion__id =idFuncion,
														frente_id=idFrente,
														fechaRegistro__gte=fechaInicialFormat,
														fechaRegistro__lte=fechaFinalFormat,
														estatus=1)\
												.order_by("material__id")


		print total.query
		for x in total:
			
			resultado = {
					"value":1,
					"id":x['material__id'],
					"nombre":x['material__nombre'],
					"peso":x['pesoMaterial'],
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
											'folio',
											'material__id',
											'numFolio',
											'frente__id',
											'frente__nombre',
											'entradadetalle__entrada_id',
											'entradadetalle__calculado',
											'remision').filter(	funcion__id =idFuncion,
																frente_id=idFrente,
																fechaRegistro__gte=fechaInicialFormat,
																fechaRegistro__lte=fechaFinalFormat,
																estatus=1).order_by("folio")
		#print armador.query
		for e in armador:
			
			resultado = {	"value": 2,
							"excel":8,
							"id":e['id'],
							"cantidad":e['cantidadAsignada'],
							"proveedor":e['funcion__proveedor'],
							"apoyo":e['apoyo__numero'],
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
							"elemento":e['elemento__nombre']
						}
			data.append(resultado)

		array["data"]=data
		array["totales"]=totales
		#excelReportes(request,array)
		return JsonResponse(array)

	elif idTaller!='0' and idFrente=='0' and idFuncion=='0':
		print "Taller del Habilitador"
		total = Remision.objects.values(	'remisiondetalle__material__id',
												'remisiondetalle__material__nombre'		
												).annotate(pesoMaterial = Sum('remisiondetalle__peso'))\
												.filter(tallerAsignado__id= idTaller,
														fechaRegistro__gte=fechaInicialFormat,
														fechaRegistro__lte=fechaFinalFormat,
														estatus=1)\
												.order_by("remisiondetalle__material__id")

		#print total.query
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

		#print total.query
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
		excelReportes(request,array)
		#print array
		return JsonResponse(array)

	elif idFuncion!='0' and idFrente=='0' and tipo=='2':
		print "Proveedor Habilitado"

		total = Remision.objects.values(	'remisiondetalle__material__id',
												'remisiondetalle__material__nombre'		
												).annotate(pesoMaterial = Sum('remisiondetalle__peso'))\
												.filter(tallerAsignado__funcion__id= idFuncion,
														fechaRegistro__gte=fechaInicialFormat,
														fechaRegistro__lte=fechaFinalFormat,
														estatus=1)\
												.order_by("remisiondetalle__material__id")

		#print total.query
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

		#print total.query
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
		excelReportes(request,array)
		return JsonResponse(array)

	elif idTaller!='0' and idFrente!='0' and idFuncion=='0':
		print "Taller de habilitado y frente de trabajo"
		
		total = Salida.objects.values(	'material__id',
										'material__nombre'		
												).annotate(pesoMaterial = Sum('cantidadAsignada'))\
												.filter(tallerAsignado__id= idTaller,
														frente_id = idFrente,
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
	


def inventarioFisicoView(request):
	template = 'control_acero/inventario/inventarioFisico.html'

	return render(request, template)

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
	#print d.query
	for f in d:
			resultado = {"id":f["id"],
						"nombre": f["nombre"],
						"imagen":f["imagen"]
						}
			data.append(resultado)

	array = mensaje
	array["data"]=data
	return JsonResponse(array)



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

def inventarioRemision(request):
	cursor = connection.cursor()
	array = {}
	dataRemision = []
	dataRemisionInventario = []
	dataRemisionInventarioSum = []
	dataSalida = []
	dataSalidaInventario = []
	remisiones = Remision.objects.values(
										"remisiondetalle__id",
										"remisiondetalle__material__nombre",
										"remisiondetalle__peso",
										"remisiondetalle__longitud",
										"remisiondetalle__numFolio"
										)\
					.filter(remisiondetalle__estatusInventario = 0, tallerAsignado_id = request.session['idTaller']).distinct()
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
					.filter(inventarioremisiondetalle__estatusInventario = 0, tallerAsignado_id = request.session['idTaller']).distinct()
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
													AND control_acero_inventarioremisiondetalle.estatusInventario = 0\
													GROUP BY control_acero_inventarioremisiondetalle.material_id, control_acero_material.nombre\
													ORDER BY control_acero_inventarioremisiondetalle.material_id ASC", [request.session['idTaller']]);
		remisionesInventarioSum = cursor.fetchall()
		for remisionInventarioSum in remisionesInventarioSum:
			resultado = {
							"materialId":remisionInventarioSum[0],
							"material":remisionInventarioSum[1],
							"peso":remisionInventarioSum[2]
						}
			dataRemisionInventarioSum.append(resultado)
	finally:
		cursor.close()
	salidas = Salida.objects.values(
										"id",
										"cantidadReal",
										"cantidadAsignada",
										"numFolio"
										)\
					.filter(estatusInventario = 0, tallerAsignado_id = request.session['idTaller'])
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
					.filter(estatusInventario = 0, tallerAsignado_id = request.session['idTaller'])
	for salidaInventario in salidasInventario:
			resultado = {
						"id":salidaInventario["id"],
						"cantidadReal":salidaInventario["cantidadReal"],
						"cantidadAsignada":salidaInventario["cantidadAsignada"]
						}
			dataSalidaInventario.append(resultado)
	array["remisiones"]=dataRemision
	array["remisionesInventario"]=dataRemisionInventario
	array["remisionesInventarioSum"]=dataRemisionInventarioSum
	array["salidas"]=dataSalida
	array["salidasInventario"]=dataSalidaInventario
	return JsonResponse(array)

def inventarioRemisionEdit(request):
	array = {}
	dataRemision = []
	dataRemisionInventario = []
	dataSalida = []
	dataSalidaInventario = []
	folio= request.POST.get('folio',1)
	remisiones = Remision.objects.values(
										"remisiondetalle__id",
										"remisiondetalle__material__nombre",
										"remisiondetalle__peso",
										"remisiondetalle__longitud",
										"remisiondetalle__numFolio"
										)\
					.filter(remisiondetalle__folioInventario = folio, tallerAsignado_id = request.session['idTaller']).distinct()
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
					.filter(inventarioremisiondetalle__folioInventario = folio, tallerAsignado_id = request.session['idTaller']).distinct()
	for remisionInventario in remisionesInventario:
			resultado = {
							"id":remisionInventario["inventarioremisiondetalle__id"],
							"material":remisionInventario["inventarioremisiondetalle__material__nombre"],
							"peso":remisionInventario["inventarioremisiondetalle__peso"],
							"longitud":remisionInventario["inventarioremisiondetalle__longitud"]
						}
			dataRemisionInventario.append(resultado)
	salidas = Salida.objects.values(
										"id",
										"cantidadReal",
										"cantidadAsignada",
										"numFolio"
										)\
					.filter(folioInventario = folio, tallerAsignado_id = request.session['idTaller'])
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
					.filter(folioInventario = folio, tallerAsignado_id = request.session['idTaller'])
	for salidaInventario in salidasInventario:
			resultado = {
						"id":salidaInventario["id"],
						"cantidadReal":salidaInventario["cantidadReal"],
						"cantidadAsignada":salidaInventario["cantidadAsignada"]
						}
			dataSalidaInventario.append(resultado)
	array["remisiones"]=dataRemision
	array["remisionesInventario"]=dataRemisionInventario
	array["salidas"]=dataSalida
	array["salidasInventario"]=dataSalidaInventario
	return JsonResponse(array)
	
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
	#print d.query


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
	html = """\
			<html>
				<head>
				</head>
				<body>
					<table rules="all" style="border-color: #666;" cellpadding="10">
						<thead>
							<tr style='background: #eee;'>
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
							<tr style='background: #eee;'>
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
								<td>%s</td>
								<td>%s</td>
								<td>%s</td>
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

	envioEmails = User.objects.all().filter(taller__id = request.session['idTaller'])
	header = "RECEPCION DEL MATERIAL"
	body = ""
	body += mailHtmlHeader(request)
	body += """
			<br />
			<table rules="all" style="border-color: #666;" cellpadding="10">
				<thead>
					<tr style='background: #eee;'>
						<th><strong> Folio </strong></th>
						<th><strong> Fabricante </strong></th>
						<th><strong> Orden </strong></th>
						<th><strong> Remision </strong></th>
						<th><strong> Fecha Remision </strong></th>
						<th><strong> Fecha Creacion </strong></th>
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
	body += mailHtmlFooter()

	for envioEmail in envioEmails:
		mail(header, body, envioEmail.email)

	return True

def mailHtmlSH(request, folio):
	# Mail Salida Habilitado
	#salidaHabilitadoSave
	res=0;
	salida = Salida.objects.values(			"folio",
											"cantidadAsignada",
											"fechaRegistro",
											"apoyo__numero",
											"frente__id",
											"frente__nombre",
											"material__nombre",
											"elemento__nombre",
											"tallerAsignado__nombre",
											"cantidadReal"
										)\
										.filter(
											numFolio = folio,
											tallerAsignado_id = request.session['idTaller']
										)\
										.distinct()
	tablaDetalle = ''
	tablaDetalle += """\
					
					<table rules="all" style="border-color: #666;" cellpadding="10">
						<thead>
							<tr style='background: #eee;'>
								<th>Material</th>
								<th>Peso de Salida de Habilitado en Kg</th>
								<th>Peso Restante en Almacen Kg</th>
							</tr>
						</thead>
						<tbody>\
						"""

	for rem in salida:
		res=rem["cantidadReal"]-rem["cantidadAsignada"]

		tablaDetalle += """\
							<tr>
								<td>%s</td>
								<td>%s</td>
								<td>%s</td>
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
							<tr style='background: #eee;'>
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
								<td>%s</td>
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

	talleresEmail = User.objects.all().filter(taller__id = request.session['idTaller'])

	frentesEmail = User.objects.all().filter(frente__id = salida[0]["frente__id"])

	header = "SALIDA DE MATERIAL HABILITADO"
	body = ""
	body2 = ""
	body += mailHtmlHeader(request)
	body += """
			<br />
			<table rules="all" style="border-color: #666;" cellpadding="10">
				<thead>
					<tr style='background: #eee;'>
						<th><strong> Folio </strong></th>
						<th><strong> Taller </strong></th>
						<th><strong> Frente Enviado</strong></th>
						<th><strong> Apoyo </strong></th>
						<th><strong> Elemento </strong></th>
						<th><strong> Fecha Creacion </strong></th>
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
				taller,
				frente,
				apoyo,
				elemento,
				fechaRegistro.strftime("%d/%m/%Y %H:%M:%S")
			)
	body2 += body
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
	#salidaHabilitadoSave
	res=0;
	entrada = Entrada.objects.values(			"folio",
											"cantidadAsignada",
											"fechaRegistro",
											"apoyo__numero",
											"frente__id",
											"frente__nombre",
											"material__nombre",
											"elemento__nombre",
											"taller__nombre",
											"cantidadReal"
										)\
										.filter(
											numFolio = folio,
											frente_id = request.session['idFrente']
										)\
										.distinct()
	tablaDetalle = ''
	tablaDetalle += """\
					
					<table rules="all" style="border-color: #666;" cellpadding="10">
						<thead>
							<tr style='background: #eee;'>
								<th>Material</th>
								<th>Peso de Recibido en Kg</th>
							</tr>
						</thead>
						<tbody>\
						"""

	for rem in entrada:
		

		tablaDetalle += """\
							<tr>
								<td>%s</td>
								<td>%s</td>
							</tr>
						"""%\
						(
							rem["material__nombre"],
							rem["cantidadAsignada"]
							
						)

	tablaDetalle += """\
						</tbody>
					</table>
					<br />\
					"""

	
	folioStr = entrada[0]["folio"]
	taller = entrada[0]["taller__nombre"]
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
					<tr style='background: #eee;'>
						<th><strong> Folio </strong></th>
						<th><strong> Taller </strong></th>
						<th><strong> Frente Enviado</strong></th>
						<th><strong> Apoyo </strong></th>
						<th><strong> Elemento </strong></th>
						<th><strong> Fecha Creacion </strong></th>
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
				taller,
				frente,
				apoyo,
				elemento,
				fechaRegistro.strftime("%d/%m/%Y %H:%M:%S")
			)
	
	body += tablaDetalle
	body += mailHtmlFooter()

	for envioEmail in frenteEmail:
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
	workbook = xlsxwriter.Workbook('Suministro.xlsx')
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
		#print array["entrada"][0]["proveedor"]
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
		#print array["entrada"][0]["proveedor"]
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

def excelReportesEntrada(request,array):
	x=0;
	workbook = xlsxwriter.Workbook('Suministro.xlsx')
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
			#print res
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

	workbook.close()
# 	generateExcel(request)

# def generateExcel(request):
#     path = './hello.xlsx' # this should live elsewhere, definitely
#     if os.path.exists(path):
#     	print path
#         with open(path, "r") as excel:
#             data = excel.read()

#         response = HttpResponse(data,content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#         response['Content-Disposition'] = 'attachment; filename=hello.xlsx'
#         return response