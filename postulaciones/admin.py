#coding:utf-8
from django.contrib import admin
from models import *
# Register your models here.


class PostulanteAdmin(admin.ModelAdmin):
	list_display = ('RUT', 'nombres', 'apellidos', 'fecha_de_nacimiento', 'sexo',
		'comuna','telefono', 'os10_al_dia', 'vencimiento')
	list_filter = ('sexo', 'os10_al_dia', 'vencimiento', 'comuna', )
	radio_fields = {'sexo':admin.HORIZONTAL, 'escolaridad': admin.HORIZONTAL,
	'sistema_de_salud':admin.HORIZONTAL}
	# raw_id_fields = ('')
	search_fields = ('nombres', 'apellidos', 'RUT')
	fieldsets = (
		('', {
			'fields':('RUT', 'nombres', 'apellidos', 'fecha_de_nacimiento', 
				'sexo', 'nacionalidad', 'escolaridad', 'estado_civil', 'hijos',
				'direccion', 'comuna', 'telefono', 'email', 'contacto_emergencia',
				'telefono_emergencia', 'cuenta_rut', 'jubilado', 'AFP', 
				'sistema_de_salud', ('ha_sido_condenado_o_detenido', 'motivo'),
				('os10_al_dia', 'vencimiento'), ('certificado_de_antecedentes',
					'certificado_de_estudios'))
			}),
		)


class EntrevistaAdmin(admin.ModelAdmin):
	raw_id_fields = ('postulante',)
	list_display = ( 'fecha', 'RUT','comuna', 'industrial', 'retail', 'manana', 'tarde', 'noche', 'seis_por_uno', 
		'cinco_por_uno', 'cuatro_por_cuatro', 'visto_bueno', 'contratado')
	list_filter = ('fecha', 'industrial', 'manana', 'tarde', 'noche', 'retail', 'seis_por_uno', 'cinco_por_uno',
	 'cuatro_por_cuatro', 'visto_bueno', 'contratado')
	search_fields = ('RUT',)
	fieldsets = (
		('', {
			'fields':('contacto', 'postulante', 
				'experiencia', ('industrial', 'retail'), ('seis_por_uno',
					'cinco_por_uno', 'cuatro_por_cuatro'), ('manana',
					'tarde', 'noche'), ('visto_bueno', 'contratado'), 
					'observaciones')
			}),

		)

class ComunaAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'region')
	list_filter = ('region',)


class InstalacionAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'cliente', 'direccion', 'comuna',)
	list_filter = ('cliente', 'comuna', )
	search_fields = ('comuna', 'nombre')


class GuardiaAdmin(admin.ModelAdmin):
	list_display = ('RUT', 'nombres', 'apellidos', 'comuna','instalacion')
	raw_id_fields = ('postulante',)
	search_fields = ('RUT','nombres', 'apellidos')


class ContratoAdmin(admin.ModelAdmin):
	list_display = ('RUT', 'nombres', 'apellidos', 'instalacion', 'fecha_inicio',
		'fecha_termino')
	list_filter = ('instalacion', )
	search_fields = ('RUT','nombres', 'apellidos', 'instalacion')	
	raw_id_fields = ('guardia', 'instalacion',)


admin.site.register(Cliente)
admin.site.register(Comuna, ComunaAdmin)
admin.site.register(Contacto)	
admin.site.register(Contrato, ContratoAdmin)
admin.site.register(Entrevista, EntrevistaAdmin)
admin.site.register(Guardia, GuardiaAdmin)
admin.site.register(Instalacion, InstalacionAdmin)
admin.site.register(Postulante, PostulanteAdmin)#, PersonaAdmin)#, PostulanteAdmin)
admin.site.register(Region)
# admin.site.register(Guardia, PersonaAdmin)
# admin.site.register(Postulante, PersonaAdmin)
# admin.site.register(Cargo)