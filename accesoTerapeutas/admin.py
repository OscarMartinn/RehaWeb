from django.contrib import admin
from .models import Calificaciones, Diagnosticos, Edad, Ejercicios, Extremidades, Gmfcs, Idiomas, Lateralidad, Macs, ObjetivoTerapeutico, Pacientes, Pci, Posicion, Sesiones, Terapeutas, SesionesEjercicios, EjerciciosRealizados, RegistroSesiones, ValoracionPacientes, FormularioPacientes 

# Register your models here.

class DiagnosticosAdmin(admin.ModelAdmin):
    list_display = ("nombre", "creado", "actualizado",)
    search_fields = ("nombre",)
    list_filter = ("creado",)
    date_hierarchy = "creado"
    readonly_fields = ('creado', 'actualizado')

class ObjetivoTerapeuticoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "creado", "actualizado",)
    search_fields = ("nombre",)
    list_filter = ("creado",)
    date_hierarchy = "creado"
    readonly_fields = ('creado', 'actualizado')

class MacsAdmin(admin.ModelAdmin):
    list_display = ("nombre", "creado", "actualizado",)
    search_fields = ("nombre",)
    list_filter = ("creado",)
    date_hierarchy = "creado"
    readonly_fields = ('creado', 'actualizado')

class GmfcsAdmin(admin.ModelAdmin):
    list_display = ("nombre", "creado", "actualizado",)
    search_fields = ("nombre",)
    list_filter = ("creado",)
    date_hierarchy = "creado"
    readonly_fields = ('creado', 'actualizado')

class CalificacionesAdmin(admin.ModelAdmin):
    list_display = ("nombre", "creado", "actualizado",)
    search_fields = ("nombre",)
    list_filter = ("creado",)
    date_hierarchy = "creado"
    readonly_fields = ('creado', 'actualizado')

class EdadAdmin(admin.ModelAdmin):
    list_display = ("nombre", "creado", "actualizado",)
    search_fields = ("nombre",)
    list_filter = ("creado",)
    date_hierarchy = "creado"
    readonly_fields = ('creado', 'actualizado')

class ExtremidadesAdmin(admin.ModelAdmin):
    list_display = ("nombre", "creado", "actualizado",)
    search_fields = ("nombre",)
    list_filter = ("creado",)
    date_hierarchy = "creado"
    readonly_fields = ('creado', 'actualizado')

class LateralidadAdmin(admin.ModelAdmin):
    list_display = ("nombre", "creado", "actualizado",)
    search_fields = ("nombre",)
    list_filter = ("creado",)
    date_hierarchy = "creado"
    readonly_fields = ('creado', 'actualizado')

class PosicionAdmin(admin.ModelAdmin):
    list_display = ("nombre", "creado", "actualizado",)
    search_fields = ("nombre",)
    list_filter = ("creado",)
    date_hierarchy = "creado"
    readonly_fields = ('creado', 'actualizado')

class PciAdmin(admin.ModelAdmin):
    list_display = ("nombre", "creado", "actualizado",)
    search_fields = ("nombre",)
    list_filter = ("creado",)
    date_hierarchy = "creado"
    readonly_fields = ('creado', 'actualizado')

class EjerciciosAdmin(admin.ModelAdmin):
    #inlines = [SesionesEjerciciosInline,]

    list_display = ("codigo","nombre", "descripcion", "creado","actualizado",)
    search_fields = ("nombre", "codigo",)
    list_filter = ("edad", "lateralidad", "posicion", "objetivoTerapeutico", "diagnostico", "pci","creado",)
    date_hierarchy = "creado"
    readonly_fields = ('creado', 'actualizado')

class TerapeutasAdmin(admin.ModelAdmin):
    list_display = ("usuario","nombre", "apellidos", "creado", "actualizado",)
    fields = ["usuario",("nombre", "apellidos"),"idioma","creado", "actualizado",]
    search_fields = ("nombre",)
    list_filter = ("creado",)
    date_hierarchy = "creado"
    readonly_fields = ('creado', 'actualizado')

class SesionesEjerciciosInline(admin.TabularInline):
    model = SesionesEjercicios
    extra = 1
    autocomplete_fields = ['ejercicios',] # nos ayuda cuando hay muchos ejercicios, es necesario que el modelo base tenga un searchfield
    

class SesionesAdmin(admin.ModelAdmin):
    inlines = [SesionesEjerciciosInline,]

    list_display = ("paciente", "fechaInicial", "fechaFinal", "enviado", "visible", "creado", "actualizado",)
    search_fields = ("paciente",)
    list_filter = ("fechaInicial", "fechaInicial", "enviado", "creado", )
    date_hierarchy = "creado"
    readonly_fields = ('creado','actualizado')

class PacientesAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellidos","fechaNacimiento", "creado", "actualizado",)
    search_fields = ("nombre",)
    list_filter = ("diagnostico", "macs", "gmfcs", "calificacion5", "calificacion50", "calificacion500", "fechaNacimiento", "creado",)
    date_hierarchy = "creado"
    readonly_fields = ('creado', 'actualizado')

class EjerciciosRealizadosAdmin(admin.ModelAdmin):
    list_display = ("ejercicio", "fecha","sesion",)
class RegistroSesionesAdmin(admin.ModelAdmin):
    list_display = ("fechaI", "fechaF","sesion","comentario",)
class FormularioPacientesAdmin(admin.ModelAdmin):
    #list_display = ("dia","momento", "horas", "usuario",)
    list_display = ("dia","momento", "horas",)
class ValoracionPacientesAdmin(admin.ModelAdmin):
    list_display = ("usuario","ejercicio", "valoracion1", "valoracion2", "valoracion3", "valoracion4", "valoracion5", "fecha","sesion",)


admin.site.register(Diagnosticos, DiagnosticosAdmin)
admin.site.register(ObjetivoTerapeutico, ObjetivoTerapeuticoAdmin)
admin.site.register(Macs, MacsAdmin)
admin.site.register(Gmfcs, GmfcsAdmin)
admin.site.register(Calificaciones, CalificacionesAdmin)
admin.site.register(Edad, EdadAdmin) 
admin.site.register(Extremidades, ExtremidadesAdmin) 
admin.site.register(Lateralidad, LateralidadAdmin) 
admin.site.register(Posicion, PosicionAdmin) 
admin.site.register(Pci, PciAdmin) 
admin.site.register(Ejercicios, EjerciciosAdmin)
admin.site.register(Terapeutas, TerapeutasAdmin)
admin.site.register(Sesiones, SesionesAdmin)
admin.site.register(Pacientes, PacientesAdmin)
admin.site.register(EjerciciosRealizados, EjerciciosRealizadosAdmin)
admin.site.register(RegistroSesiones, RegistroSesionesAdmin)
admin.site.register(ValoracionPacientes, ValoracionPacientesAdmin)
admin.site.register(FormularioPacientes, FormularioPacientesAdmin)
admin.site.register(Idiomas)
