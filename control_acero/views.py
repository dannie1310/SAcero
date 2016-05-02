from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from control_acero.report.models_auth import Empresa, Usuario
from .models import Apoyo, Elemento, Despiece, Material, Frente, Funcion, ControlAsignacion, FrenteAsigna, ProgramaSuministro, ProgramaSuministroDetalle, EtapaAsignacion, Taller, Transporte
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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response


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
			resultado = {"idApoyo":a.id,"numero":a.numero}
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
	idPrograma = request.POST.get('programa', 0)
	idFuncion = request.POST.get('funcion', 0)
	suministro = EtapaAsignacion.objects.values('id', 'pesoSolicitado', 'pesoRecibido', 'controlAsignacion_id', 'funcion_id', 'programaSuministro_id').filter(programaSuministro_id=idPrograma, funcion_id=idFuncion)
	for s in suministro:
		resultado = {"id":s["id"],"pesoSolicitado":s["pesoSolicitado"],"pesoRecibido":s["pesoRecibido"],"idAsignacion":s["controlAsignacion_id"],"idFuncion":s["funcion_id"],"idPrograma":s["programaSuministro_id"]}
		data.append(resultado)
	array = mensaje
	array["data"]=data
	return JsonResponse(array)

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
	elemento = Elemento.objects.filter(apoyo=1)
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
	p = ProgramaSuministro(idOrden=idOrden, fechaInicial=timezone.now(), fechaFinal=timezone.now(), frente_id=idFrente, estatus=1)
	p.save()
	for data in json_object:
		datos = data["data"]
		splitData = datos.split("|")
		apoyo = splitData[0]
		elemento = splitData[1]
		numeroCuatro = splitData[2]
		numeroCinco= splitData[3]
		numeroSeis = splitData[4]
		numeroSiete = splitData[5]
		numeroOcho = splitData[6]
		numeroNueve = splitData[7]
		numeroDiez = splitData[8]
		numeroOnce = splitData[9]
		numeroDoce = splitData[10]
		total = splitData[11]
		pd = ProgramaSuministroDetalle(idProgramaSuministro=p.pk, apoyo_id=apoyo, elemento_id=elemento, numeroCuatro=numeroCuatro, numeroCinco=numeroCinco, numeroSeis=numeroSeis, numeroSiete=numeroSiete, numeroOcho=numeroOcho, numeroNueve=numeroNueve, numeroDiez=numeroDiez, numeroOnce=numeroOnce, numeroDoce=numeroDoce)
		pd.save();
	mensaje = {"estatus":"ok", "mensaje":"Se creo el Programa de Suministro exitosamente"}
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
	elemento = Elemento.objects.values('id','nombre', 'material__id', 'material__nombre', 'material__numero', 'material__peso', 'material__proveedor').filter(id=idElemento)
	for e in elemento:
		resultado = {"idElemento":e["id"],"nombreElemento":e['nombre'],"idMaterial":e['material__id'],"nombreMaterial":e['material__nombre'],"materialNumero":e['material__numero'],"materialPeso":e['material__peso'],"materialProveedor":e['material__proveedor']}
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
	paginator = Paginator(apoyo_list, 5)
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
		e = EtapaAsignacion(pesoSolicitado=pesoSolicitado, pesoRecibido=pesoRecibido, estatusEtapa=1, estatus=1, controlAsignacion_id=idAsignacion, funcion_id=idFuncion, programaSuministro_id=idSuministro)
		e.save();
	mensaje = {"estatus":"ok", "mensaje":"Se realizo la recepcion de suministro correctamente."}
	array = mensaje
	return JsonResponse(array)

def suministroAsignarSave(request):
	array = {}
	mensaje = {}
	respuesta = request.POST.get('json')
	json_object = json.loads(respuesta)
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
		e = EtapaAsignacion(controlAsignacion_id=idAsignacion, pesoSolicitado=pesoSolicitado, pesoRecibido=pesoRecibido, estatusEtapa=2, estatus=1, funcion_id=idFuncion, taller_id=idTaller, transporte_id=idTransporte, cantidadAsignada=cantidadAsignada, programaSuministro_id=idPrograma, idEtapaPertenece=etapaPertenece)
		e.save();
	mensaje = {"estatus":"ok", "mensaje":"Se realizo la asignacion de Suministro correctamente."}
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
			print ec.id
	# 	e = EtapaAsignacion(pesoSolicitado=pesoSolicitado, pesoRecibido=pesoRecibido, estatusEtapa=1, estatus=1, controlAsignacion_id=idAsignacion, funcion_id=idFuncion, programaSuministro_id=idSuministro)
	# 	e.save();
	# mensaje = {"estatus":"ok", "mensaje":"Se realizo la recepcion de suministro correctamente."}
	# array = mensaje
	# return JsonResponse(array)