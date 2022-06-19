from django.contrib import admin

from englishAccess.models import Ages, Languages, AssessmentPatiens, Classifications, Diagnostics, Exercices, ExercisesDone, Extremities, GmfcsEnglish, Laterality, MacsEnglish, PatientForm, Patients, PciEnglish, Position, RegistrationSession, Sessions, SessionsExercices, Therapeutic_Objective, Therapists

# Register your models here.

class DiagnosticsAdmin(admin.ModelAdmin):
    list_display = ("nombre", "created", "updated",)
    search_fields = ("nombre",)
    list_filter = ("created",)
    date_hierarchy = "created"
    readonly_fields = ('created', 'updated')

class TherapistsAdmin(admin.ModelAdmin):
    list_display = ("user","name", "lastnames", "created", "updated",)
    fields = ["user",("name", "lastnames"),"language","created", "updated",]
    search_fields = ("name",)
    list_filter = ("created",)
    date_hierarchy = "created"
    readonly_fields = ('created', 'updated')

#class SessionsExercicesInline(admin.TabularInline):
#    model = SessionsExercices
#    extra = 1
#    search_fields = ("ejercicios",)
#    autocomplete_fields = ['ejercicios',] # nos ayuda cuando hay muchos ejercicios, es necesario que el modelo base tenga un searchfield

class SessionsAdmin(admin.ModelAdmin):
#    inlines = [SessionsExercicesInline,]

    list_display = ("paciente", "initial_Date", "final_Date", "enviado", "visible", "creado", "actualizado",)
    search_fields = ("paciente",)
    list_filter = ("initial_Date", "final_Date", "enviado", "creado", )
    date_hierarchy = "creado"
    readonly_fields = ('creado','actualizado')



admin.site.register(Therapists, TherapistsAdmin)
admin.site.register(Diagnostics, DiagnosticsAdmin)
admin.site.register(SessionsExercices)
admin.site.register(Languages)
admin.site.register(Therapeutic_Objective)
admin.site.register(MacsEnglish)
admin.site.register(GmfcsEnglish)
admin.site.register(Classifications)
admin.site.register(Ages) 
admin.site.register(Extremities) 
admin.site.register(Laterality) 
admin.site.register(Position) 
admin.site.register(PciEnglish) 
admin.site.register(Exercices)
admin.site.register(Sessions, SessionsAdmin)
admin.site.register(Patients)
admin.site.register(ExercisesDone)
admin.site.register(RegistrationSession)
admin.site.register(AssessmentPatiens)
admin.site.register(PatientForm)