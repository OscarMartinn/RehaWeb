from django.db import models
from django.conf import settings
from datetime import date

from accesoTerapeutas.models import Terapeutas

# Create your models here.

class Diagnostics(models.Model):
    nombre = models.CharField(max_length=40, help_text="Add a new diagnostic.")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta :
        verbose_name = 'Diagnostic'
        verbose_name_plural = 'Diagnostics'
    
    def __str__ (self):
        return self.nombre


class Languages(models.Model):
    lenguage = models.CharField(max_length=30)
    code = models.CharField(max_length=8,null=True, blank=True)

    class Meta :
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'

    def __str__ (self):
        return self.lenguage


class Therapists(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,blank=True)
    name = models.CharField(max_length=30, help_text="Therapist name.", verbose_name="Name")
    lastnames = models.CharField(max_length=20, help_text="Therapist lastnames.", verbose_name="Lastnames")
    language = models.ForeignKey(Languages,on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta :
        verbose_name = 'Therapist'
        verbose_name_plural = 'Therapists'
        ordering = ['-created']
    
    def __str__ (self):
        return self.name


class TherapeuticObjective(models.Model):
    nombre = models.CharField(max_length=40, help_text="Add a new therapeutic objective")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now_add=True)

    def autoAlias(self):
        nombreCambiado = self.nombre.replace(" ", "")
        return str(nombreCambiado)

    class Meta :
        verbose_name = 'Therapeutic Objective'
        verbose_name_plural = 'Therapeutic Objectives'
    
    def __str__ (self):
        return self.nombre

class MacsEnglish(models.Model):
    nombre = models.CharField(max_length=40, help_text="Add a new level of manual skill.")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def autoAlias(self):
        return "MACS" + str(self.nombre)

    class Meta :
        verbose_name = 'MACS'
        verbose_name_plural = 'MACS'
    
    def __str__ (self):
        return self.nombre
    
   
class GmfcsEnglish(models.Model):
    nombre = models.CharField(max_length=40, help_text="Add a new level of gross motor function")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def autoAlias(self):
        return "GMFCS" + str(self.nombre)

    class Meta :
        verbose_name = 'GMFCS'
        verbose_name_plural = 'GMFCS'
    
    def __str__ (self):
        return self.nombre
    
class Classifications(models.Model):
    name = models.CharField(max_length=40, help_text="Add a new functional mobility classification level [1-6,C and N]")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def autoAlias(self):
        return "Classifications" + str(self.name)

    class Meta :
        verbose_name = 'Classification'
        verbose_name_plural = 'Classifications'
    
    def __str__ (self):
        return self.name
  

class Ages(models.Model):
    nombre = models.CharField(max_length=40, help_text="Add a new age range")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now_add=True)

    def autoAlias(self):
        nombreCambiado = self.nombre.replace(" ", "")
        return str(nombreCambiado)

    class Meta :
        verbose_name = 'Age'
        verbose_name_plural = 'Ages'
    
    def __str__ (self):
        return self.nombre
    
    
class Extremities(models.Model):
    nombre = models.CharField(max_length=40, help_text="Add a new extremity")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now_add=True)

    class Meta :
        verbose_name = 'Extremity'
        verbose_name_plural = 'Extremities'
    
    def __str__ (self):
        return self.nombre
    
     
class Laterality(models.Model):
    nombre = models.CharField(max_length=40, help_text="Add a new laterality name.")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now_add=True)

    class Meta :
        verbose_name = 'Laterality'
        verbose_name_plural = 'Laterality'
    
    def __str__ (self):
        return self.nombre
    
    
class Position(models.Model):
    nombre = models.CharField(max_length=40, help_text="Add a new position", null=True, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now_add=True)

    class Meta :
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'
    
    def __str__ (self):
        return self.nombre
    
class PciEnglish(models.Model):
    nombre = models.CharField(max_length=40, help_text="Add a new PCI")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now_add=True)

    class Meta :
        verbose_name = 'PCI'
        verbose_name_plural = 'PCI'
    
    def __str__ (self):
        return self.nombre
    
class Exercices(models.Model):
    codigo = models.CharField(max_length=8, help_text="Indicate the code of the exercise.", verbose_name="Code")
    nombre = models.CharField(max_length=60, help_text="Give a name for the exercise.", verbose_name="Exercise name")
    descripcion = models.TextField(max_length=500, null=True, blank=True, help_text="If you wish, add an explanatory description.", verbose_name="Description")
    edad = models.ManyToManyField(Ages, help_text="Select the age ranges for this exercise.", verbose_name="Age ranges")
    extremidades = models.ManyToManyField(Extremities, help_text="Select the limbs involved in this exercise.", verbose_name="Extremities")
    lateralidad = models.ForeignKey(Laterality, on_delete=models.CASCADE, help_text="Select the laterality of this exercise.", verbose_name="Laterality")
    posicion = models.ManyToManyField(Position, help_text="Select the position associated with this exercise.", verbose_name="Position")
    objetivoTerapeutico = models.ManyToManyField(TherapeuticObjective, help_text="Select the therapeutic objectives associated with this exercise.", verbose_name="Therapeutic Objectives") 
    diagnostico = models.ManyToManyField(Diagnostics, help_text="Select the diagnoses associated with this exercise.", verbose_name="Diagnostic") 
    pci = models.ManyToManyField(PciEnglish, verbose_name="PCI") 
    video = models.FileField(upload_to='ejercicios',help_text="Select the video you want to associate with the exercise. With the following format: code_exercise.mp4", null=True, blank=True, verbose_name="Video")
    visible = models.BooleanField(default=True, help_text="When you want to hide an exercise, uncheck the box.", verbose_name="Without hiding")
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
        verbose_name = 'Exercise'
        verbose_name_plural = 'Exercises'
        ordering = ['-creado']
    
    def __str__ (self):
        return self.nombre


class Patients(models.Model):
    #Lo que queramos que tenga nuestra tabla
    nombre = models.CharField(max_length=80, help_text="Indique el nombre completo del paciente.", verbose_name="Name")
    apellidos = models.CharField(max_length=60, help_text="Indique los apellidos del paciente.", verbose_name="Lastnames")
    birthDate = models.DateField(verbose_name="Birth Date",null=True,blank=True)
    email = models.EmailField(max_length=30, help_text="Correo electróncio.", verbose_name="Email")
    telefono = models.CharField(max_length=10, help_text="Número de teléfono.", verbose_name="Phone")
    diagnostico = models.ForeignKey(Diagnostics,on_delete=models.CASCADE, help_text="Seleccione el diagnostico de este paciente.", verbose_name="Diagnostic")
    macs = models.ForeignKey(MacsEnglish,on_delete=models.CASCADE, verbose_name="MACS")
    gmfcs = models.ForeignKey(GmfcsEnglish,on_delete=models.CASCADE, verbose_name="GMFCS")
    calificacion5 = models.ForeignKey(Classifications,on_delete=models.CASCADE, related_name='calificacion_cinco', help_text="Indica la calificacion FMS5 para una distacia de 5 metros", verbose_name="FMS5 - Classification")
    calificacion50 = models.ForeignKey(Classifications,on_delete=models.CASCADE, related_name='calificacion_cincuenta', help_text="Indica la calificacion FMS50 para una distacia de 50 metros", verbose_name="FMS50 - Classification")
    calificacion500 = models.ForeignKey(Classifications,on_delete=models.CASCADE, related_name='calificacion_quinientos', help_text="Indica la calificacion FMS500 para una distacia de 500 metros", verbose_name="FMS500 - Classification")
    usuario = models.CharField(max_length=30, help_text="Indique el usuario que desea asignar al paciente.(Longitud mínima 5 caracteres [a-z, 0-9 y guiones bajos]", verbose_name="User BOT")
    contraseña = models.CharField(max_length=15, help_text="Indique la contraseña que se usará en las funciones del bot.", verbose_name="Password BOT")
    terapeuta = models.ForeignKey(Terapeutas,on_delete=models.CASCADE, help_text="Seleccione el terapeuta de este paciente.", verbose_name="Therapist")
    visible = models.BooleanField(default=True, help_text="Cuando quieras dejar oculto un Paciente, desmarca la casilla", verbose_name="Without hiding")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now_add=True)

    def calcula_edad(self):
        fecha = self.birthDate
        edad = int(date.today().year) - int(fecha.year)
        return edad

    class Meta :
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
        ordering = ['-creado']

    def __str__ (self):
        return "%s, %s" % (self.nombre, self.apellidos)



class Sessions(models.Model):
    paciente = models.ForeignKey(Patients, on_delete=models.CASCADE, help_text="Selecciona al paciente asigando para esta sesión.", verbose_name="Patient")
    ejercicios = models.ManyToManyField(Exercices, through='SessionsExercices', help_text="Seleccione los ejercicios para esta sesión.", verbose_name="Exercises")
    periodicidad = models.IntegerField(default=1, help_text="Indique las veces que puede realizar el paciente esta sesión a lo largo de la semana.", verbose_name="Periodicity")
    initialDate = models.DateField(verbose_name="Initial date",null=True, blank=True)
    finalDate = models.DateField(verbose_name="Final date",null=True, blank=True)
    terapeuta = models.ForeignKey(Terapeutas,on_delete=models.CASCADE, help_text="Seleccione el terapeuta de esta sesión.", verbose_name="Therapist",null=True, blank=True)
    visible = models.BooleanField(default=True, help_text="Cuando quieras dejar oculto una Sesión, desmarca la casilla", verbose_name="Whithout hiding")
    enviado = models.BooleanField(default=False, help_text="Si la casilla no se encuentra marcada, las sesion no ha sido programada", verbose_name="Sended")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now_add=True)

    def get_ejercicios(self):
        return "\n".join([e.nombre for e in self.ejercicios.all()])

    class Meta :
        verbose_name = 'Session'
        verbose_name_plural = 'Sessions'
        ordering = ['-creado']
    
    def __str__ (self):
        return self.paciente.nombre

class SessionsExercices(models.Model):
    ejercicios=models.ForeignKey(Exercices, on_delete=models.CASCADE, verbose_name="Exercises")
    sesiones=models.ForeignKey(Sessions, on_delete=models.CASCADE, verbose_name="Sessions")
    repeticiones = models.SmallIntegerField(default=1, verbose_name="Repetitions")

    class Meta :
        verbose_name = 'Session Exercise'
        verbose_name_plural = 'Session Exercises'
        
    
    def __str__(self):
        sesion = self.sesiones.paciente.nombre
        return sesion

#Se usan para el Feedback que se recibe desde el paciente
class ExercisesDone(models.Model):
    exercise = models.CharField(max_length=80, verbose_name="Ejercicio")
    date = models.CharField(max_length=30, verbose_name="Fecha de realización")
    session = models.IntegerField(default=0, verbose_name="ID Sesión")

    class Meta :
        verbose_name = 'Exercise done in the session'
        verbose_name_plural = 'Exercises done in the session'
        
    
    def __str__(self):
        return self.exercise

class RegistrationSession(models.Model):
    initialDate = models.CharField(max_length=30, verbose_name="Fecha de inicio")
    finalDate =models.CharField(max_length=30, verbose_name="Fecha de finalización")
    session = models.IntegerField(default=0, verbose_name="ID Sesión")
    comment = models.CharField(max_length=100, verbose_name="Comentarios", default="sin comentario")

    class Meta :
        verbose_name = 'Session Registration'
        verbose_name_plural = 'Session Registrations'
        
    
    def __str__(self):
        return self.initialDate

class PatientForm(models.Model):
    dia=models.CharField(max_length=100, verbose_name="Día preferido")
    momento=models.CharField(max_length=30, verbose_name="Momento del día")
    horas = models.CharField(max_length=120,verbose_name="Horario preferido")
    #usuario=models.CharField(max_length=30, verbose_name="Usuario")
    #idUser = models.IntegerField(default=0, verbose_name="Id Usuario")
    paciente = models.ForeignKey(Patients, on_delete=models.CASCADE, help_text="Seleccione el paciente", verbose_name="Paciente", blank=True, null=True) 

    class Meta :
        verbose_name = 'Form'
        verbose_name_plural = 'Forms'
        
    
    def __str__(self):
        return self.dia

class AssessmentPatiens(models.Model):    
    usuario=models.CharField(max_length=30, verbose_name="Paciente")
    ejercicio=models.CharField(max_length=30, verbose_name="Ejercicio",null=True,blank=True)
    valoracion1=models.IntegerField(verbose_name="Pregunta 1", help_text="¿Te ha parecido claro el ejercicio? [0 poco claro y 5 muy claro]")
    valoracion2=models.IntegerField(verbose_name="Pregunta 2", help_text="¿Te ha parecido difícil el ejercicio? [0 poco difícil y 5 muy fácil]")
    valoracion3=models.IntegerField(verbose_name="Pregunta 3", help_text="¿Te ha parecido útil el ejercicio para tus objetivos? [0 poco útil y 5 muy útil]")
    valoracion4=models.IntegerField(verbose_name="Pregunta 4", help_text="¿Has sentido algún tipo de dolor? [0 nada y 5 muchísimo]")
    valoracion5=models.CharField(max_length=4, verbose_name="Pregunta 5", help_text="¿Te gustaría repetir el ejercicio en un futuro?")
    fecha=models.CharField(max_length=30, verbose_name="Fecha")
    sesion = models.IntegerField(default=0, verbose_name="ID Sesión")
    

    class Meta :
        verbose_name = 'Evaluation of the exercises'
        verbose_name_plural = 'Evaluations of the exercises'
        
    
    def __str__(self):
        return self.usuario
