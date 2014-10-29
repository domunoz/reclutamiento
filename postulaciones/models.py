#coding:utf-8
from django.db import models
from django.utils import timezone
from audit_log.models.fields import CreatingUserField, LastUserField, LastSessionKeyField
#from localflavor.cl.forms import CLRutField
# Create your models here
class Region(models.Model):
	nombre = models.CharField(max_length=140)

	def __unicode__(self):
		return self.nombre

	class Meta:
		verbose_name = 'región'
		verbose_name_plural = 'regiones'


class Comuna(models.Model):
	nombre = models.CharField(max_length=140)
	region = models.ForeignKey(Region)

	def __unicode__(self):
		return self.nombre


class Postulante(models.Model):
	SEXO = (
		('M','Masculino'),
		('F','Femenino'),
	)
	ESTADO_CIVIL = (
		('SO','Soltero'),
		('CA','Casado'),
		('SE','Separado'),
		('VI','Viudo'),
	)

	ESCOLARIDAD = (
		('B','Básica'),
		('M','Media'),
	)
	AFPS = (
		('PR', 'Provida'),
		('HA', 'Habitat'),
		('CA', 'Capital'),
		('MO', 'Modelo'),
		('CU', 'Cuprum'),
		('PL', 'Planvital'),
	)
	SISTEMA_SALUD =(
		('F','FONASA'),
		('I','ISAPRE')
	)
	#información personal
	RUT = models.CharField(primary_key=True, max_length=140, help_text="ej:17555111-7")
	nombres = models.CharField(max_length=140, null=True, blank=True)
	apellidos = models.CharField('apellidos', max_length=140, null=True, blank=True)
	fecha_de_nacimiento = models.DateField(null=True, blank=True)
	sexo = models.CharField(max_length=1, choices=SEXO, default='M')
	nacionalidad = models.CharField(max_length=140, default="chilena")
	escolaridad = models.CharField(max_length=1, choices=ESCOLARIDAD, default='M')
	estado_civil = models.CharField(max_length=2, null=True, blank=True, choices=ESTADO_CIVIL)
	hijos = models.PositiveIntegerField(null=True, blank=True)
	#informacion de contacto
	#region = models.models.CharField(max_length=2, default="13")#esto lo manejo a nivel interno, yo sabiendo la comuna calculo la region :D
	#provincia = models.CharField(max_length=3, default="131")#y la provincia

	direccion = models.CharField('dirección', max_length=140, null=True, blank=True)
	comuna = models.ForeignKey(Comuna)
	telefono = models.CharField('teléfono', max_length=140, null=True, blank=True)
	email = models.EmailField(max_length=140, null=True, blank=True)
	contacto_emergencia = models.CharField('en caso de emergencia llamar a', max_length=140, null=True, blank=True)
	telefono_emergencia = models.CharField('teléfono', max_length=140, null=True, blank=True)
	cuenta_rut = models.BooleanField(default=False)
	#
	jubilado = models.BooleanField(default=False)
	AFP = models.CharField(max_length=140, choices=AFPS)
	sistema_de_salud = models.CharField(max_length=1, choices=SISTEMA_SALUD, default='F')
	
	ha_sido_condenado_o_detenido = models.BooleanField(default=False)
	motivo = models.CharField(max_length=140, null=True, blank=True)
	os10_al_dia = models.BooleanField('OS-10', default=False)
	vencimiento = models.DateField(null=True, blank=True)
	#certificado_os10 = models.FileField(upload_to="certificados_os10", null=True, blank=True)
	
	#documentacion 
	certificado_de_antecedentes = models.BooleanField(default=False)
	certificado_de_estudios = models.BooleanField(default=False)

	fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)

	def __unicode__(self):
		return "%s %s"%(self.nombres, self.apellidos)

class Contacto(models.Model):
	nombre = models.CharField(max_length=140)

	def __unicode__(self):
		return self.nombre


class Cliente(models.Model):
	nombre = models.CharField(max_length=140)

	def __unicode__(self):
		return self.nombre


class Instalacion(models.Model):
	nombre = models.CharField(max_length=140)
	cliente = models.ForeignKey(Cliente)
	direccion = models.CharField('dirección', max_length=140,null=True, blank=True)
	comuna = models.ForeignKey(Comuna)

	def __unicode__(self):
		return self.nombre 

	class Meta:
		verbose_name = 'instalación'
		verbose_name_plural = 'instalaciones'


class Entrevista(models.Model): #esto es lo que toca reclutamiento
	fecha = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	contacto = models.ForeignKey(Contacto)
	postulante = models.ForeignKey(Postulante, null=True, blank=True)
	experiencia = models.TextField(help_text="experiencia en seguridad privada", null=True, blank=True)
	industrial = models.BooleanField(default=False)
	retail = models.BooleanField(default=False)
	#sistema de turnos
	seis_por_uno = models.BooleanField('6x1', default=False)
	cinco_por_uno = models.BooleanField('5x1',default=False)
	cuatro_por_cuatro = models.BooleanField('4x4', default=False) 
	#jornada
	manana = models.BooleanField('mañana', default=False)
	tarde = models.BooleanField(default=False)
	noche = models.BooleanField(default=False)
	
	visto_bueno = models.BooleanField(default=False)
	contratado = models.BooleanField(default=False)
	observaciones = models.TextField(null=True, blank=True)
	reclutador = CreatingUserField()

	def RUT(self):
		return self.postulante.RUT

	def comuna(self):
		return self.postulante.comuna


class Guardia(models.Model):
	postulante = models.ForeignKey(Postulante)
	instalacion = models.ForeignKey(Instalacion,null=True, blank=True)#Gexoper :O

	def RUT(self):
		return self.postulante.RUT

	def nombres(self):
		return self.postulante.nombres

	def apellidos(self):
		return self.postulante.apellidos 

	def comuna(self):
		return self.postulante.comuna

	def __unicode__(self):
		return self.postulante.RUT


class Contrato(models.Model):
	fecha_inicio = models.DateField(default=timezone.now)
	fecha_termino = models.DateField(null=True, blank=True)
	guardia = models.ForeignKey(Guardia)
	instalacion = models.ForeignKey(Instalacion, verbose_name='instalación')
	renta = models.PositiveIntegerField(null=True, blank=True)
	observaciones = models.TextField(null=True, blank=True)
	creado_por = CreatingUserField()
	#renta = models.PositiveIntegerField()
	# monto_primer_anticipo = models.PositiveIntegerField(null=True, blank=True)
	# fecha_primer_anticipo = models.DateField(null=True, blank=True)
	def RUT(self):
		return self.guardia.postulante.RUT

	def nombres(self):
		return self.guardia.postulante.nombres

	def apellidos(self):
		return self.guardia.postulante.apellidos



class Amonestacion(models.Model):
	fecha = models.DateTimeField(default=timezone.now)
	guardia = models.ForeignKey(Guardia)
	causa = models.CharField(max_length=140)