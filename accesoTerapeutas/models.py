from fnmatch import translate
from django.db import models
from datetime import date
from django.conf import settings

# Create your models here.

class Diagnosticos(models.Model):
    nombre = models.CharField(max_length=40, help_text="Añada un nuevo diagnóstico.")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now_add=True)

    class Meta :
        verbose_name = 'Diagnóstico'
        verbose_name_plural = 'Diagnósticos'
    
    def __str__ (self):
        return self.nombre

class ObjetivoTerapeutico(models.Model):
    nombre = models.CharField(max_length=40, help_text="Añada un nuevo objetivo terapéutivo")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now_add=True)

    def autoAlias(self):
        nombreCambiado = self.nombre.replace(" ", "")
        return str(nombreCambiado)

    class Meta :
        verbose_name = 'Objetivo'
        verbose_name_plural = 'Objetivos'
    
    def __str__ (self):
        return self.nombre

class Macs(models.Model):
    nombre = models.CharField(max_length=40, help_text="Añada un nuevo nivel de habilidad manual")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now_add=True)

    def autoAlias(self):
        return "MACS" + str(self.nombre)

    class Meta :
        verbose_name = 'MACS'
        verbose_name_plural = 'MACS'
    
    def __str__ (self):
        return self.nombre
    
   
class Gmfcs(models.Model):
    nombre = models.CharField(max_length=40, help_text="Añada un nuevo nivel de función motora gruesa")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now_add=True)

    def autoAlias(self):
        return "GMFCS" + str(self.nombre)

    class Meta :
        verbose_name = 'GMFCS'
        verbose_name_plural = 'GMFCS'
    
    def __str__ (self):
        return self.nombre
    
class Calificaciones(models.Model):
    nombre = models.CharField(max_length=40, help_text="Añada un nuevo nivel de clasificación de la movilidad funcional [1-6,C y N]")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now_add=True)

    def autoAlias(self):
        return "Calificaciones" + str(self.nombre)

    class Meta :
        verbose_name = 'Clasificación'
        verbose_name_plural = 'Clasificaciones'
    
    def __str__ (self):
        return self.nombre
  

class Edad(models.Model):
    nombre = models.CharField(max_length=40, help_text="Añada un nuevo rango de edad")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now_add=True)

    def autoAlias(self):
        nombreCambiado = self.nombre.replace(" ", "")
        return str(nombreCambiado)

    class Meta :
        verbose_name = 'Edad'
        verbose_name_plural = 'Edades'
    
    def __str__ (self):
        return self.nombre
    
    
class Extremidades(models.Model):
    nombre = models.CharField(max_length=40, help_text="Añada un nombre de una nueva extremidad")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now_add=True)

    class Meta :
        verbose_name = 'Extremidad'
        verbose_name_plural = 'Extremidades'
    
    def __str__ (self):
        return self.nombre
    
     
class Lateralidad(models.Model):
    nombre = models.CharField(max_length=40, help_text="Añada un nuevo nombre de lateralidad")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now_add=True)

    class Meta :
        verbose_name = 'Lateralidad'
        verbose_name_plural = 'Lateralidad'
    
    def __str__ (self):
        return self.nombre
    
    
class Posicion(models.Model):
    nombre = models.CharField(max_length=40, help_text="Añada una nueva posición", null=True, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now_add=True)

    class Meta :
        verbose_name = 'Posición'
        verbose_name_plural = 'Posiciones'
    
    def __str__ (self):
        return self.nombre
    
class Pci(models.Model):
    nombre = models.CharField(max_length=40, help_text="Añada una nuevo PCI")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now_add=True)

    class Meta :
        verbose_name = 'PCI'
        verbose_name_plural = 'PCI'
    
    def __str__ (self):
        return self.nombre
    
class Ejercicios(models.Model):
    codigo = models.CharField(max_length=8, help_text="Indique el código del ejercicio.", verbose_name="Código")
    nombre = models.CharField(max_length=60, help_text="Indique un nombre para el nuevo ejercicio.", verbose_name="Nombre del Ejercicio")
    descripcion = models.TextField(max_length=500, null=True, blank=True, help_text="Si lo desea, añade una descripción explicativo.", verbose_name="Descripción")
    edad = models.ManyToManyField(Edad, help_text="Seleccione los rangos de edad para este ejercicio.", verbose_name="Rangos de Edad")
    extremidades = models.ManyToManyField(Extremidades, help_text="Seleccione las extremidades involucradas eneste ejercicio.", verbose_name="Extremidades")
    lateralidad = models.ForeignKey(Lateralidad, on_delete=models.CASCADE, help_text="Seleccione la lateralidad de este ejercicio.", verbose_name="Lateralidad")
    posicion = models.ManyToManyField(Posicion, help_text="Seleccione la posicion asociada a este ejercicio.", verbose_name="Posición")
    objetivoTerapeutico = models.ManyToManyField(ObjetivoTerapeutico, help_text="Selecciona los objetivos terapéuticos asociados este ejercicio.", verbose_name="Objetivos Terapéuticos") 
    diagnostico = models.ManyToManyField(Diagnosticos, help_text="Seleccione los diagnósticos asociadosa a este ejercicio.", verbose_name="Diagnostico") 
    pci = models.ManyToManyField(Pci, verbose_name="PCI") 
    video = models.FileField(upload_to='ejercicios',help_text="Seleccione el video que quieres asociar al ejercicio. Con el siguiente formato: codigo_ejercicio.mp4", null=True, blank=True, verbose_name="Video")
    visible = models.BooleanField(default=True, help_text="Cuando quieras dejar oculto un Ejercicio, desmarca la casilla", verbose_name="Sin ocultar")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now_add=True)

    def get_edades(self):
        return "\n".join([e.nombre for e in self.edad.all()])
    def get_extremidades(self):
        return "\n".join([e.nombre for e in self.extremidades.all()])
    def get_posiciones(self):
        return "\n".join([e.nombre for e in self.posicion.all()])
    def get_objetivos(self):
        return "\n".join([e.nombre for e in self.objetivoTerapeutico.all()])
    def get_diagnosticos(self):
        return "\n".join([e.nombre for e in self.diagnostico.all()])
    def get_pci(self):
        return "\n".join([e.nombre for e in self.pci.all()])

    class Meta :
        verbose_name = 'Ejercicio'
        verbose_name_plural = 'Ejercicios'
        ordering = ['-creado']
    
    def __str__ (self):
        return self.nombre


class Idiomas(models.Model):
    lenguage = models.CharField(max_length=30)
    code = models.CharField(max_length=8,null=True, blank=True)

    class Meta :
        verbose_name = 'Idioma'
        verbose_name_plural = 'Idiomas'

    def __str__ (self):
        return self.lenguage

class Terapeutas(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,blank=True)
    nombre = models.CharField(max_length=30, help_text="Indique el nombre del terapeuta.", verbose_name="Nombre")
    apellidos = models.CharField(max_length=20, help_text="Indique los apellidos del terapeuta.", verbose_name="Apellidos")
    idioma = models.ForeignKey(Idiomas,on_delete=models.CASCADE, null=True, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now_add=True)

    class Meta :
        verbose_name = 'Terapeuta'
        verbose_name_plural = 'Terapeutas'
        ordering = ['-creado']
    
    def __str__ (self):
        return self.nombre

class Pacientes(models.Model):
    #Lo que queramos que tenga nuestra tabla
    nombre = models.CharField(max_length=80, help_text="Indique el nombre completo del paciente.", verbose_name="Nombre")
    apellidos = models.CharField(max_length=60, help_text="Indique los apellidos del paciente.", verbose_name="Apellidos")
    fechaNacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    email = models.EmailField(max_length=30, help_text="Correo electróncio.", verbose_name="Email")
    telefono = models.CharField(max_length=10, help_text="Número de teléfono.", verbose_name="Telefono")
    diagnostico = models.ForeignKey(Diagnosticos,on_delete=models.CASCADE, help_text="Seleccione el diagnostico de este paciente.", verbose_name="Diagnóstico")
    macs = models.ForeignKey(Macs,on_delete=models.CASCADE, verbose_name="MACS")
    gmfcs = models.ForeignKey(Gmfcs,on_delete=models.CASCADE, verbose_name="GMFCS")
    calificacion5 = models.ForeignKey(Calificaciones,on_delete=models.CASCADE, related_name='calificacion_cinco', help_text="Indica la calificacion FMS5 para una distacia de 5 metros", verbose_name="FMS5 - Clasificación")
    calificacion50 = models.ForeignKey(Calificaciones,on_delete=models.CASCADE, related_name='calificacion_cincuenta', help_text="Indica la calificacion FMS50 para una distacia de 50 metros", verbose_name="FMS50 - Clasificación")
    calificacion500 = models.ForeignKey(Calificaciones,on_delete=models.CASCADE, related_name='calificacion_quinientos', help_text="Indica la calificacion FMS500 para una distacia de 500 metros", verbose_name="FMS500 - Clasificación")
    usuario = models.CharField(max_length=30, help_text="Indique el usuario que desea asignar al paciente.(Longitud mínima 5 caracteres [a-z, 0-9 y guiones bajos]", verbose_name="Usuario del BOT")
    contraseña = models.CharField(max_length=15, help_text="Indique la contraseña que se usará en las funciones del bot.", verbose_name="Contraseña del BOT")
    #terapeuta = models.ForeignKey(Terapeutas,on_delete=models.CASCADE, help_text="Seleccione el terapeuta de este paciente.", verbose_name="Terapeuta")
    terapeuta = models.ManyToManyField(Terapeutas, help_text="Seleccione el terapeuta de este paciente.", verbose_name="Terapeuta")
    visible = models.BooleanField(default=True, help_text="Cuando quieras dejar oculto un Paciente, desmarca la casilla", verbose_name="Sin ocultar")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now_add=True)

    def calcula_edad(self):
        fecha = self.fechaNacimiento
        edad = int(date.today().year) - int(fecha.year)
        return edad

    class Meta :
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['-creado']

    def __str__ (self):
        return "%s, %s" % (self.nombre, self.apellidos)


class Sesiones(models.Model):
    paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE, help_text="Selecciona al paciente asigando para esta sesión.", verbose_name="Paciente") 
    #through nos indica que la tabla intermedia que se crea en ManyToMany es la que yo le indico porque quiero que tenga mas campos.
    ejercicios= models.ManyToManyField(Ejercicios, through='SesionesEjercicios', help_text="Seleccione los ejercicios para esta sesión.", verbose_name="Ejercicios")
    periodicidad = models.IntegerField(default=1, help_text="Indique las veces que puede realizar el paciente esta sesión a lo largo de la semana.", verbose_name="Periodicidad")
    fecha_Inicial = models.DateField(verbose_name="Fecha de Inicio")
    fecha_Final = models.DateField(verbose_name="Fecha de Final")
    terapeuta = models.ForeignKey(Terapeutas,on_delete=models.CASCADE, help_text="Seleccione el terapeuta de esta sesión.", verbose_name="Terapeuta")
    visible = models.BooleanField(default=True, help_text="Cuando quieras dejar oculto una Sesión, desmarca la casilla", verbose_name="Sin ocultar")
    enviado = models.BooleanField(default=False, help_text="Si la casilla no se encuentra marcada, las sesion no ha sido programada", verbose_name="Enviado")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now_add=True)

    def get_ejercicios(self):
        return "\n".join([e.nombre for e in self.ejercicios.all()])

    class Meta :
        verbose_name = 'Sesion'
        verbose_name_plural = 'Sesiones'
        ordering = ['-creado']
    
    def __str__ (self):
        return self.paciente.nombre

class SesionesEjercicios(models.Model):
    ejercicios=models.ForeignKey(Ejercicios, on_delete=models.CASCADE, verbose_name="Ejercicios")
    sesiones=models.ForeignKey(Sesiones, on_delete=models.CASCADE, verbose_name="Sesiones")
    repeticiones = models.SmallIntegerField(default=1, verbose_name="Repeticiones")

    class Meta :
        verbose_name = 'Ejercicio de la sesión'
        verbose_name_plural = 'Ejercicios de la sesión'
        
    
    def __str__(self):
        sesion= self.sesiones.paciente.nombre
        return sesion

#Se usan para el Feedback que se recibe desde el paciente
class EjerciciosRealizados(models.Model):
    ejercicio=models.CharField(max_length=80, verbose_name="Ejercicio")
    fecha=models.CharField(max_length=30, verbose_name="Fecha de realización")
    sesion = models.IntegerField(default=0, verbose_name="ID Sesión")

    class Meta :
        verbose_name = 'Ejercicio realizado en la sesion'
        verbose_name_plural = 'Ejercicios realizados en la sesión'
        
    
    def __str__(self):
        return self.ejercicio

class RegistroSesiones(models.Model):
    fechaI=models.CharField(max_length=30, verbose_name="Fecha de inicio")
    fechaF=models.CharField(max_length=30, verbose_name="Fecha de finalización")
    sesion = models.IntegerField(default=0, verbose_name="ID Sesión")
    comentario = models.CharField(max_length=100, verbose_name="Comentarios", default="sin comentario")

    class Meta :
        verbose_name = 'Registro de la sesión'
        verbose_name_plural = 'Registros de la sesión'
        
    
    def __str__(self):
        return self.fechaI

class FormularioPacientes(models.Model):
    dia=models.CharField(max_length=100, verbose_name="Día preferido")
    momento=models.CharField(max_length=30, verbose_name="Momento del día")
    horas = models.CharField(max_length=120,verbose_name="Horario preferido")
    #usuario=models.CharField(max_length=30, verbose_name="Usuario")
    #idUser = models.IntegerField(default=0, verbose_name="Id Usuario")
    paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE, help_text="Seleccione el paciente", verbose_name="Paciente", blank=True, null=True) 

    class Meta :
        verbose_name = 'Formulario'
        verbose_name_plural = 'Formularios'
        
    
    def __str__(self):
        return self.dia

class ValoracionPacientes(models.Model):
    usuario=models.CharField(max_length=30, verbose_name="Paciente")
    ejercicio=models.CharField(max_length=30, verbose_name="Ejercicio")
    valoracion1=models.IntegerField(verbose_name="Pregunta 1", help_text="¿Te ha parecido claro el ejercicio? [0 poco claro y 5 muy claro]")
    valoracion2=models.IntegerField(verbose_name="Pregunta 2", help_text="¿Te ha parecido difícil el ejercicio? [0 poco difícil y 5 muy fácil]")
    valoracion3=models.IntegerField(verbose_name="Pregunta 3", help_text="¿Te ha parecido útil el ejercicio para tus objetivos? [0 poco útil y 5 muy útil]")
    valoracion4=models.IntegerField(verbose_name="Pregunta 4", help_text="¿Has sentido algún tipo de dolor? [0 nada y 5 muchísimo]")
    valoracion5=models.CharField(max_length=4, verbose_name="Pregunta 5", help_text="¿Te gustaría repetir el ejercicio en un futuro?")
    fecha=models.CharField(max_length=30, verbose_name="Fecha")
    sesion = models.IntegerField(default=0, verbose_name="ID Sesión")
    

    class Meta :
        verbose_name = 'Valoración de los ejercicios'
        verbose_name_plural = 'Valoraciones de los ejercicios'
        
    
    def __str__(self):
        return self.usuario
