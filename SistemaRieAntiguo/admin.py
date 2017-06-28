# -*- coding: utf-8 -*-
from django.contrib import admin
from sanvalentin_app.models import *

admin.site.register(Alumno)
admin.site.register(Profesor) 
admin.site.register(Curso)
admin.site.register(Materia)
admin.site.register(AlumnoCurso)
admin.site.register(Evaluacion)
admin.site.register(Notas)
admin.site.register(Informacion)
admin.site.register(DesarrolloPersonal)
admin.site.register(InformeDesarrolloPersonal)
admin.site.register(AlumnoMateriaPromedio)
admin.site.register(Directiva)
admin.site.register(Apoderado)
admin.site.register(AntecedentesAlumno)
admin.site.register(DiasTrabajados)
admin.site.register(PromedioAlumno)
admin.site.register(ObservacionesAlumno)