function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$( "#btnRegistrar" ).click(function() {
	var mail = $("#registroMail").val();
	var password = $("#registroPassword").val();
	var passwordr = $("#registroPasswordRepetido").val();
	$(".success").empty();
	$(".danger").empty();
    $.ajax({
        type: "POST",
        url: "usuario/agregar/",
        async: false,
        dataType: "json",
        data: {csrfmiddlewaretoken: csrftoken,
	        	mail: mail,
	        	password: password,
	        	passwordr: passwordr
				},
        beforeSend: function (objeto) {
        },
        success: function (datos) {
            try {
            	if(datos.estatus == "ok"){
                    $(".success").append(datos.mensaje);
                    $(".success").show();
                    setTimeout(function () {
                        $(".success").hide("slide");
                        $("#registro-modal").modal('hide');
                    }, 4000);
                    limpiarRegistro();
            	}else{
                    $(".danger").append(datos.mensaje);
	                    $(".danger").show();
	                    setTimeout(function () {
	                        $(".danger").hide("slide");
	                    }, 4000);
	                    return false;
            	}
            } catch (e) {
                alert("Error al cargar Juicios:" + e);
            }
        },
        error: function (objeto, quepaso, otroobj) {
            alert("Error en la peticion de Juicios:\n\n" + otroobj);
        }
    });
});
$( "#btnLogea" ).click(function() {
	var mail = $("#mailLogin").val();
	var password = $("#passwordLogin").val();
	$(".success").empty();
	$(".danger").empty();
    $.ajax({
        type: "POST",
        url: "usuario/login/",
        async: false,
        dataType: "json",
        data: {csrfmiddlewaretoken: csrftoken,
	        	mail: mail,
	        	password: password
				},
        beforeSend: function (objeto) {
        },
        success: function (datos) {
            try {
            	if(datos.estatus == "ok"){
                    $(".success").append(datos.mensaje);
                    $(".success").show();
                    setTimeout(function () {
                        $(".success").hide("slide");
                        $("#registro-modal").modal('hide');
                    }, 4000);
                    limpiarRegistro();
            	}else{
                    $(".danger").append(datos.mensaje);
	                    $(".danger").show();
	                    setTimeout(function () {
	                        $(".danger").hide("slide");
	                    }, 4000);
	                    return false;
            	}
            } catch (e) {
                alert("Error al cargar Juicios:" + e);
            }
        },
        error: function (objeto, quepaso, otroobj) {
            alert("Error en la peticion de Juicios:\n\n" + otroobj);
        }
    });
});
$( "#logout" ).click(function() {
    window.location.replace("/polls/");
    /*$.ajax({
        type: "POST",
        url: "/polls/usuario/logout/",
        async: false,
        dataType: "json",
        data: {csrfmiddlewaretoken: csrftoken
                },
        beforeSend: function (objeto) {
        },
        success: function (datos) {
        },
        error: function (objeto, quepaso, otroobj) {
            alert("Error en la peticion de Juicios:\n\n" + otroobj);
        }
    });*/
});
$( ".urlIndex" ).click(function() {
    window.location.replace("/polls/");
});
$( ".urlHome" ).click(function() {
    window.location.replace("/polls/home/");
});
$( ".urlCarrito" ).click(function() {
    window.location.replace("/polls/carrito/");
});
limpiarRegistro = function () {
    $("#registroMail").val('');
    $("#registroPassword").val('');
    $("#registroPasswordRepetido").val('');
},
$('#detalle-modal').on('show.bs.modal', function (e) {
    var id = $(e.relatedTarget).data('id');
    var nombre = $(e.relatedTarget).data('nombre');
    var imagen = $(e.relatedTarget).data('imagen');
    var descripcion = $(e.relatedTarget).data('descripcion');
    var precio = $(e.relatedTarget).data('precio');
    $("#txtId").val(id);
    $("#nombreDetalle").html("<h4>"+nombre+"</h4>");
    $("#descripcionDetalle").html(descripcion);
    $("#precioDetalle").html("$ "+precio);
    $("#imagenDetalle").attr("src", "../../media/"+imagen);
});
$( "#btnAgregarCarrito" ).click(function() {
    $(".alertCarritoSucces").empty();
    var idProducto = $("#txtId").val();
    $.ajax({
        type: "POST",
        url: "/polls/venta/agregar/",
        async: false,
        dataType: "json",
        data: {csrfmiddlewaretoken: csrftoken,
                idProducto: idProducto
                },
        beforeSend: function (objeto) {
        },
        success: function (datos) {
            try {
                console.log(datos);
                if(datos.estatus == "ok"){
                    $(".alertCarritoSucces").append(datos.mensaje);
                    $(".alertCarritoSucces").show();
                    setTimeout(function () {
                        $(".alertCarritoSucces").hide("slide");
                        $("#detalle-modal").modal('hide');
                    }, 4000);
                    items();
                    cargaItems();
                    cargaItemsComprados();
                }else{
                    $(".danger").append(datos.mensaje);
                        $(".danger").show();
                        setTimeout(function () {
                        }, 4000);
                        return false;
                }
            } catch (e) {
                alert("Error al agregar al Carrito:" + e);
            }
        },
        error: function (objeto, quepaso, otroobj) {
            alert("Error al agregar al Carrito:\n\n" + otroobj);
        }
    });

});
$( "#btnPago" ).click(function() {
    var nombre = $("#nombrePago").val();
    var direccion = $("#direccionPago").val();
    var telefono = $("#telefonoPago").val();
    var cp = $("#cpPago").val();
    var tarjeta = $("#tarjetaPago").val();
    var nip = $("#nipPago").val();
    var facturaProductos = $("#facturaProductos").html();
    var factura = $("#factura").html();
    $.ajax({
        type: "POST",
        url: "/polls/pago/transferencia/",
        async: false,
        dataType: "json",
        data: {csrfmiddlewaretoken: csrftoken,
                facturaProductos: facturaProductos,
                factura: factura,
                nombre: nombre,
                direccion: direccion,
                telefono: telefono,
                cp: cp,
                tarjeta: tarjeta,
                nip: nip
                },
        beforeSend: function (objeto) {
        },
        success: function (datos) {
            try {
                if(datos.estatus == "ok"){
                    $(".alertPago").append(datos.mensaje);
                    $(".alertPago").show();
                    setTimeout(function () {
                        $(".alertPago").hide("slide");
                        $("#pago-modal").modal('hide');
                    }, 4000);
                    items();
                    cargaItems();
                    cargaItemsComprados();
                }else{
                    $(".danger").append(datos.mensaje);
                        $(".danger").show();
                        setTimeout(function () {
                        }, 4000);
                        return false;
                }
            } catch (e) {
                alert("Error al agregar al Carrito:" + e);
            }
        },
        error: function (objeto, quepaso, otroobj) {
            alert("Error al agregar al Carrito:\n\n" + otroobj);
        }
    });

});
items = function () {
    var html = "";
    $.ajax({
        type: "POST",
        url: "/polls/items/usuario/",
        async: false,
        dataType: "json",
        data: {csrfmiddlewaretoken: csrftoken
                },
        beforeSend: function (objeto) {
        },
        success: function (datos) {
            try {
                console.log(datos);
                if(datos.estatus == "ok"){
                    html += datos.items;
                }
            } catch (e) {
                alert("Error al agregar al Carrito:" + e);
            }
        },
        error: function (objeto, quepaso, otroobj) {
            alert("Error al agregar al Carrito:\n\n" + otroobj);
        }
    });
    $("#items").html("Tienes "+html+" Productos");
    $("#itemsDesc").html("Actualmente tienes "+html+" productos en tu carrito de compra");
},
cargaItems = function () {
    $("#tablaProductos tbody").empty();
    $("#total tbody").empty();
    $(".subtotal").empty();
    $(".cantidadTotal").empty();
    var tabla = "";
    var total = 0;
    $.ajax({
        type: "POST",
        url: "/polls/items/detalle/",
        async: false,
        dataType: "json",
        data: {csrfmiddlewaretoken: csrftoken
                },
        beforeSend: function (objeto) {
        },
        success: function (datos) {
            try {
                console.log(datos);
                if(datos.estatus == "ok"){
                    $.each(datos.data, function (count, object) {
                        total += parseFloat(object.total);
                        tabla += '<tr>';
                            tabla += '<td><img src="../../media/'+object.imagen+'" alt="Producto" class="img-responsive"></td>';
                            tabla += '<td>'+object.nombre+'</td>';
                            tabla += '<td>'+object.cantidadUsuario+'</td>';
                            tabla += '<td>'+object.precio+'</td>';
                            tabla += '<td>'+object.total+'</td>';
                            tabla += '<td><a style="cursor:pointer;" onclick="eliminaProducto('+object.producto_id+');"">Eliminar</a></td>';
                        tabla += '</tr>';
                    });
                    $(".subtotal").html("$ "+total);
                    $(".cantidadTotal").html("$ "+total);
                }
            } catch (e) {
                alert("Error al consultar el Carrito:" + e);
            }
        },
        error: function (objeto, quepaso, otroobj) {
            alert("Error al consultar el Carrito:\n\n" + otroobj);
        }
    });
    $("#tablaProductos tbody").append(tabla);
},
cargaItemsComprados = function () {
    $("#tablaProductosComprados tbody").empty();
    $("#total tbody").empty();
    var tabla = "";
    var total = 0;
    $.ajax({
        type: "POST",
        url: "/polls/items/historial/",
        async: false,
        dataType: "json",
        data: {csrfmiddlewaretoken: csrftoken
                },
        beforeSend: function (objeto) {
        },
        success: function (datos) {
            try {
                console.log(datos);
                if(datos.estatus == "ok"){
                    $.each(datos.data, function (count, object) {
                        total += parseFloat(object.total);
                        tabla += '<tr>';
                            tabla += '<td><img src="../../media/'+object.imagen+'" alt="Producto" class="img-responsive"></td>';
                            tabla += '<td>'+object.nombre+'</td>';
                            tabla += '<td>'+object.cantidadUsuario+'</td>';
                            tabla += '<td>'+object.precio+'</td>';
                            tabla += '<td>'+object.total+'</td>';
                        tabla += '</tr>';
                    });
                    //$(".subtotal").html("$ "+total);
                    $(".cantidadTotalHistorial").html("$ "+total);
                }
            } catch (e) {
                alert("Error al consultar el Carrito:" + e);
            }
        },
        error: function (objeto, quepaso, otroobj) {
            alert("Error al consultar el Carrito:\n\n" + otroobj);
        }
    });
    $("#tablaProductosComprados tbody").append(tabla);
},
eliminaProducto = function (producto_id) {
    var html = "";
    $(".alertElimina").empty();
    $.ajax({
        type: "POST",
        url: "/polls/items/eliminar/",
        async: false,
        dataType: "json",
        data: {csrfmiddlewaretoken: csrftoken,
                producto_id: producto_id
                },
        beforeSend: function (objeto) {
        },
        success: function (datos) {
            try {
                console.log(datos);
                if(datos.estatus == "ok"){
                    html += datos.mensaje;
                    items();
                    cargaItems();
                    cargaItemsComprados();
                    $(".alertElimina").append(datos.mensaje);
                        $(".alertElimina").show();
                        setTimeout(function () {
                            $(".alertElimina").hide("slide");
                        }, 4000);
                }
            } catch (e) {
                alert("Error al eliminar el producto:" + e);
            }
        },
        error: function (objeto, quepaso, otroobj) {
            alert("Error al eliminar el producto:\n\n" + otroobj);
        }
    });
},
$(function () {
        items();
        cargaItems();
        cargaItemsComprados();
});