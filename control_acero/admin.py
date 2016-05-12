from django.contrib import admin

# Register your models here.
from .models import Apoyo, Material, Despiece, Elemento, Ingenieria, Transporte, Taller, Funcion, Frente, Factor

admin.site.register(Apoyo)
admin.site.register(Material)
admin.site.register(Despiece)
admin.site.register(Elemento)
admin.site.register(Transporte)
admin.site.register(Taller)
admin.site.register(Funcion)
admin.site.register(Frente)
admin.site.register(Factor)