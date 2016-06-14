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

# def loginUsuario(request):
# 	logout(request)
# 	username = password = ''
# 	if request.POST:
# 		username = request.POST['usuario']
# 		password = request.POST['clave']
#         userIGH = Usuario.objects.using('auth_db').filter(usuario=username, clave=md5.new(password).hexdigest()).first()
#         if userIGH:
#             try:
#                 user = User.objects.get(username=userIGH.usuario)
#             except User.DoesNotExist:
#                 user = User(username=userIGH.usuario, password=userIGH.clave, email=userIGH.correo, first_name=userIGH.nombre, last_name=userIGH.apaterno + ' ' + userIGH.amaterno)
#                 user.save()
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     url = '/control_acero/principal/'
#                     return HttpResponseRedirect(url)
# 	template_name = '/control_acero'
#  	messages.error(request, 'Usuario y/o Password invalidos')
#  	return HttpResponseRedirect(template_name)
 	
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
				current_user = request.user
				user_id = current_user.id
				getTallerAsignado(request, 0)
				url = '/control_acero/perfil/'
				return HttpResponseRedirect(url)
	template_name = '/control_acero'
 	messages.error(request, 'Usuario y/o Password invalidos')
 	return HttpResponseRedirect(template_name)

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

def getTallerAsignado(request, almacen):
	taller = Taller.objects.filter(id = almacen).order_by()
	# today = datetime.now()
	# date = today.strftime("%d/%m/%Y")
	if taller.exists():
		request.session['idTaller'] = taller[0].id
		request.session['nombreTaller'] = taller[0].nombre
		request.session['proveedorTaller'] = taller[0].proveedor
		request.session['ubicacionTaller'] = taller[0].ubicacion
		request.session['responsableTaller'] = taller[0].responsable
		# request.session['fecha'] = date
	else:
		request.session['idTaller'] = 0
		request.session['nombreTaller'] = 0
		request.session['proveedorTaller'] = 0
		request.session['ubicacionTaller'] = 0
		request.session['responsableTaller'] = 0

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
	del request.session['idTaller']
	del	request.session['nombreTaller']
	del	request.session['proveedorTaller']
	del	request.session['ubicacionTaller']
	del	request.session['responsableTaller']
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
	return render_to_response('control_acero/catalogos/apoyos/apoyo.html', {"apoyos": apoyos})

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
	return render_to_response('control_acero/catalogos/usuarios/usuario.html', {"usuarios": usuarios})

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
	return render_to_response('control_acero/catalogos/talleres/taller.html', {"talleres": talleres})

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
	envioEmails = User.objects.all().filter(taller__id = request.session['idTaller'])
	header = "RECEPCION DEL MATERIAL DEL FABRICANTE"
	body = ""
	body += """\
			<html>
			<head></head>
			<body>
				<table>
					<thead>
						<tr>
							<th> Usuario %s %s %s %s</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td>Se Creo el Folio: %s</td>
						</tr>
					</tbody>
				</table>
			</body>
			</html>
	""" %\
	(
		request.user.username,
		request.user.first_name,
		request.user.last_name,
		request.user.email,
		numFolio
	)
	for envioEmail in envioEmails:
		mail(header, body, envioEmail.email)

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
						.filter(remision__tallerAsignado_id = request.session["idTaller"])\
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
	envioEmails = User.objects.all().filter(taller__id = request.session['idTaller'])
	header = "SALIDA DEL HABILITADO"
	body = ""
	body += """\
			<html>
			<head></head>
			<body>
				<table>
					<thead>
						<tr>
							<th> Usuario %s %s %s %s</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td>Se Creo el Folio: %s</td>
						</tr>
					</tbody>
				</table>
			</body>
			</html>
	""" %\
	(
		request.user.username,
		request.user.first_name,
		request.user.last_name,
		request.user.email,
		numFolio
	)
	for envioEmail in envioEmails:
		mail(header, body, envioEmail.email)
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
	remisionDetalles = Salida.objects \
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
						.filter(numFolio = folio, tallerAsignado_id = request.session["idTaller"]) \
						.order_by('material_id')
	for remisionDetalle in remisionDetalles:
		resultado = {
						"id":remisionDetalle["material_id"],
						"materialNombre":remisionDetalle["material__nombre"],
						"materialDiametro":remisionDetalle["material__diametro"],
						"cantidadAsignada":remisionDetalle["cantidadAsignada"],
						"apoyoId":remisionDetalle["apoyo__id"],
						"apoyoNumero":remisionDetalle["apoyo__numero"],
						"elementoId":remisionDetalle["elemento__id"],
						"elementoNombre":remisionDetalle["elemento__nombre"]
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
	respuesta = request.POST.get('json')
	jsonDataInfo = json.loads(respuesta)
	respuestaFaltante = request.POST.get('jsonFaltante')
	jsonDataInfoFaltante = json.loads(respuestaFaltante)
	numFolio = 0
	array = {}
	mensaje = {}
	data = []
	folio = Entrada.objects.all().filter(estatusEtapa = 1, tallerAsignado_id = request.session["idTaller"]).order_by("-numFolio")[:1]
	if folio.exists():
		numFolio = folio[0].numFolio
	numFolioInt = int(numFolio)+1
	numFolio = "%04d" % (numFolioInt,)
	numFolio = "EMA-"+numFolio
	print jsonDataInfoFaltante
	for jsonData in jsonDataInfo:
		material = jsonData["material"]
		cantidadReal = jsonData["cantidadReal"]
		cantidadAsignada = jsonData["cantidadAsignada"]
		bandera = jsonData["bandera"]
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
								tallerAsignado_id = request.session["idTaller"]
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
								tallerAsignado_id = request.session["idTaller"]
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
	envioEmails = User.objects.all().filter(taller__id = request.session['idTaller'])
	header = "ARMADO RECEPCIÓN"
	body = ""
	body += """\
			<html>
			<head></head>
			<body>
				<table>
					<thead>
						<tr>
							<th> Usuario %s %s %s %s</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td>Se Creo el Folio: %s</td>
						</tr>
					</tbody>
				</table>
			</body>
			</html>
	""" %\
	(
		request.user.username,
		request.user.first_name,
		request.user.last_name,
		request.user.email,
		numFolio
	)
	for envioEmail in envioEmails:
		mail(header, body, envioEmail.email)
	return JsonResponse(array)


def foliosMostrar(request):
	modulo = request.POST.get('modulo', 0)
	numFolio = 0
	array = {}
	mensaje = {}
	data = []
	today = datetime.now()
	dateFormat = today.strftime("%d/%m/%Y")
	print "------"
	print dateFormat

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
		folio = Entrada.objects.all().filter(estatusEtapa = 1, tallerAsignado_id = request.session["idTaller"]).order_by("-numFolio")[:1]
		if folio.exists():
			numFolio = folio[0].numFolio
		numFolioInt = int(numFolio)+1
		numFolio = "%04d" % (numFolioInt,)
		numFolio = "EMA-"+numFolio

	mensaje = {"estatus":"ok", "folio":numFolio, "date":dateFormat}
	#mensaje = {"estatus":"ok", "folio":numFolio}
	array = mensaje
	return JsonResponse(array)

def foliosSalidaHabilitado(request):
	array = {}
	mensaje = {}
	data = []
	salidaFolios = InventarioSalida.objects.values('folio', 'numFolio', 'apoyo__numero', 'elemento__nombre').distinct()
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
	return render_to_response('control_acero/perfil.html', RequestContext(request, {"talleres": talleres}))

@login_required(login_url='/control_acero/usuario/login/')
def principalView(request):
	if request.method == "POST":
		almacen = request.POST["almacen"]
		if int(almacen) == 0:
			template_name = '/control_acero/perfil'
		 	messages.error(request, 'Debes Elegir un Perfil')
		 	return HttpResponseRedirect(template_name)
		getTallerAsignado(request, almacen)
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
	idFrente = request.POST.get('frente', 0)
	tipo =request.POST.get('tipo',0)

	fechaInicial = request.POST.get('fechai', '17/05/2016')
	fechaFinal = request.POST.get('fechaf', '12/06/2016')
	fechaInicialFormat = datetime.strptime(fechaInicial+" 00:00:00", '%d/%m/%Y %H:%M:%S')
	fechaFinalFormat = datetime.strptime(fechaFinal+" 23:59:59", '%d/%m/%Y %H:%M:%S')

	print "----------"
	print idFuncion
	print tipo
	print idTaller
	print idFrente
	print fechaInicial
	print fechaFinal

	if idTaller=='0' and idFrente=='0' and tipo=='1':

		print "aqui Fabricante"
		print idTaller
			##here!!! :D .annotate(pesoMaterial = Sum('peso'))\

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
				
			resultado = {   "value": 1,
								"id":e['id'],
								"orden":e['idOrden'],
								"pesoTotal":e['pesoNeto'],
								"peso":e['remisiondetalle__peso'],
								"fechaR":e['fechaRemision'],
								"fechaA":e['fechaActualizacion'],
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
		return JsonResponse(array)
			
	elif idFrente!='0' and idTaller=='0':
		print "elif Armado"
		armador = Entrada.objects.values(
											'id',
											'cantidadAsignada',
											'funcion__proveedor',
											'material__nombre',
											'apoyo__numero',
											'cantidadReal',
											'elemento__nombre',
											'folio',
											'tallerAsignado__nombre',
											'remision').filter(
																fechaRegistro__gte=fechaInicialFormat,
																fechaRegistro__lte=fechaFinalFormat,
																estatus=1).order_by("tallerAsignado__id")
		#print armador.query
		for e in armador:
			
			resultado = {	"value": 2,
							"id":e['id'],
							"cantidad":e['cantidadAsignada'],
							"proveedor":e['funcion__proveedor'],
							"apoyo":e['apoyo__numero'],
							"folio":e['folio'],
							"taller":e['tallerAsignado__nombre'],
							"remision":e['remision'],
							"material":e['material__nombre'],
							"cantidadReal":e['cantidadReal'],
							"elemento":e['elemento__nombre']
						}
			data.append(resultado)

		array["data"]=data
		return JsonResponse(array)

	elif idTaller!='0' and idFrente=='0' and idFuncion=='0':
		print "TAller del Habilitador"
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
				
			resultado = {   "value": 4,
								"id":e['id'],
								"orden":e['idOrden'],
								"pesoTotal":e['pesoNeto'],
								"peso":e['remisiondetalle__peso'],
								"fechaR":e['fechaRemision'],
								"fechaA":e['fechaActualizacion'],
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
			resultado={	"value": 3,
						"id":e['id'],
						"cantidad":e['cantidadAsignada'],
						"fechaR":e['fechaRegistro'],
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
		return JsonResponse(array)

	elif idFuncion!='0' and idFrente=='0' and tipo=='2':
		print "Proveedor HAbilitado"

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
				
			resultado = {   "value": 4,
								"id":e['id'],
								"orden":e['idOrden'],
								"pesoTotal":e['pesoNeto'],
								"peso":e['remisiondetalle__peso'],
								"fechaR":e['fechaRemision'],
								"fechaA":e['fechaActualizacion'],
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
			resultado={	"value": 4,
						"id":s['id'],
						"cantidad":s['cantidadAsignada'],
						"fechaR":s['fechaRegistro'],
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
		return JsonResponse(array)


	else:
		mensaje = {"estatus":"ok", "mensaje":"Consulta invalida"}
		print mensaje
	array = mensaje
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
	
	# despiece = request.POST.get('despiece', 1)
	# elemento = request.POST.get('elemento', 1)
	# apoyo = request.POST.get('apoyo', 1)
	# cantidadFisica = request.POST.get('cantidadFisica', 1)
	# longitudFisica = request.POST.get('longitudFisica', 1)
	# funcion = request.POST.get('funcion', 1)
	# frente = request.POST.get('frente', 1)
	
	# e = InventarioFisico.objects.create(despiece = despiece,
	# 									elemento=elemento,
	# 									apoyo = apoyo,
	# 									cantidadFisica = cantidadFisica,
	# 									longitudFisica = longitudFisica, 
	# 									proveedor_id = funcion,
	# 									frente_id = frente,
	# 									estatus=1)

	# print e.query
				
		# 	for data in json_object:
		# datos = data["data"]
		# splitData = datos.split("|")
		# despiece = splitData[0]
		# elemento = splitData[1]
		# apoyo = splitData[2]
		# idFuncion = splitData[3]
		# idFrente = splitData[4]
		# longitudFisica = splitData[5]
		# cantidadFisica = splitData[6]
	mensaje = {"estatus":"ok", "mensaje":"Se guardo correctamente."}
	array = mensaje
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


def mail(header, body, to):
	try:
		send_mail(header, body, 'control-acero@grupohi.mx',
		    [to], html_message=body, fail_silently=False)
	except:
		return True;