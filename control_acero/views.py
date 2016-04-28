from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from control_acero.report.models_auth import Empresa, Usuario
from .models import Elemento, Despiece, Material, Frente, Funcion, ControlAsignacion, AsignacionEtapa, FrenteAsigna
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
from .forms import ApoyoForm


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

def frenteGuardaFrenteView(request):
	respuesta = request.POST.get('json')
	json_object = json.loads(respuesta)
	array = {}
	mensaje = {}
	for data in json_object:
		datos = data["data"]
		splitData = datos.split("|")
		orden = splitData[0]
		frente = splitData[1]
		tipo = splitData[2]
		estructura = splitData[3]
		f = FrenteAsigna(idOrden = orden, idFrente = frente, tipo = tipo, idEstructuraElemento = estructura)
		f.save()
		if f.pk is not None:
			mensaje = {"estatus":"ok", "mensaje":"El Frente de Trabajo fue asignado correctamente"}
		else:
			mensaje = {"estatus":"error", "mensaje":"Ocurrio un error al intentar crear el Frente de Trabajo"}
	array = mensaje
	return JsonResponse(array)

def controlAsignacionView(request):
	template = 'control_acero/control_asignacion/control_asignacion.html'
	return render(request, template)

def controlAsignacionNuevoView(request):
	template = 'control_acero/control_asignacion/control_asignacion.html'
	return render(request, template)

def suministroView(request):
	template = 'control_acero/suministro/suministro.html'
	return render(request, template)

def habilitadoView(request):
	template = 'control_acero/habilitado/habilitado.html'
	return render(request, template)

def habilitadoCambioTallerView(request):
	template = 'control_acero/habilitado/habilitado_cambio_taller.html'
	return render(request, template)

def armadoView(request):
	template = 'control_acero/armado/armado.html'
	return render(request, template)

def colocadoView(request):
	template = 'control_acero/colocado/colocado.html'
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
	#v = Empresa.objects.using('auth_db').all()
	#print v
	if (usuario == ""):
		resultado = {"estatus":"error","mensaje":"El campo usuario esta vacio"}
		return JsonResponse(resultado)
	if (clave == ""):
		resultado = {"estatus":"error","mensaje":"El campo clave esta vacio"}
		return JsonResponse(resultado)
	login = Usuario.objects.using('auth_db').filter(usuario=usuario, clave=md5.new(clave).hexdigest())
	print login
	for e in login:
		if(e != ""):
			print e.usuario
			#request.session['idUsuario'] = e.idUsuario
			request.session['usuario'] = e.usuario
			request.session['clave'] = clave
			#cursor.execute("SELECT [IDBaseDatos],[Nombre],[Mascara],[Servidor],[IDTipoSistemaOrigen],[IDTipoBaseDatos],[EstaActiva],[FechaHoraRegistro] FROM [BasesDatos].[BasesDatos] WHERE EstaActiva = 1")
			#row = cursor.fetchall()
			url = '/control_acero/acceso'
			#url = reverse('/otro', kwargs={'dbs': row})
			return HttpResponseRedirect(url)

	template_name = '/control_acero'
	messages.error(request, 'Usuario y/o Password invalidos')
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
	frente = Frente.objects.all()
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
	#v = Venta(usuario_id=usuario_id)
	elemento = Elemento.objects.all()
	for e in elemento:
			resultado = {"idElemento":e.id,"nombre":e.nombre}
			data.append(resultado)

	array = mensaje
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

def controlNuevo(request):
	array = {}
	mensaje = {}
	data = []
	mensaje = {"estatus":"ok", "mensaje":"Correcto"}
	funcion = request.POST['funcion']
	frente = request.POST['frente']
	cantidad = request.POST['cantidad']
	tiempo = request.POST['tiempo']
	c = ControlAsignacion(cantidad=cantidad, tiempoEntrega=tiempo, estatus=1, frente_id=frente, funcion_id=funcion, fechaRegistro=timezone.now())
	c.save()
	e = AsignacionEtapa(estatusEtapa=1, etapa=1, ControlAsignacion_id=c.id, funcion_id=funcion)
	e.save()
	array = mensaje
	return JsonResponse(array)

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

def apoyosEditView(request):
	if request.method == "POST":
		form = ApoyoForm(request.POST)
		if(form.is_valid()):
			apoyo = form.save(commit=False)
			apoyo.save()
			#return render(request, 'control_acero/catalogos/apoyos/apoyo.html', {'form': form})
	else:
		form = ApoyoForm()
		
	return render(request, 'control_acero/catalogos/apoyos/apoyo_new.html', {'form': form})

def recepcionRegistros(request):
	print "aqui"
	#funcion = request.POST['funcion']
	#frente = request.POST['frente']
	#cantidad = request.POST['cantidad']
	#tiempo = request.POST['tiempo']
	#c = ControlAsignacion(cantidad=cantidad, tiempoEntrega=tiempo, estatus=1, frente_id=frente, funcion_id=funcion, fechaRegistro=timezone.now())
	#c.save()

	#e = AsignacionEtapa(estatusEtapa=1, etapa=1, ControlAsignacion_id=c.id, funcion_id=funcion)
	#e.save()