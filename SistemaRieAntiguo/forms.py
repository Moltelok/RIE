# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from localflavor.cl.forms import CLRutField
from sanvalentin_app.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit, Div
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FormActions)


class AlumnoForm(ModelForm):
    class Meta:
        model = Alumno
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'datepicker'}),
        }

    rut = CLRutField()


class ApoderadoForm(ModelForm):
    class Meta:
        model = Apoderado
        exclude = ["alumno"]

    rut_a = CLRutField()


class ProfesorForm(ModelForm):
    class Meta:
        model = Profesor
        exclude = ["usuario", "logo"]

    rut = CLRutField()


class CursoForm(ModelForm):
    class Meta:
        model = Curso


class EvaluacionForm(ModelForm):
    class Meta:
        model = Evaluacion
        exclude = ['materia', 'semestre']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'datepicker'}),
        }


class NotasUpdateForm(ModelForm):
    class Meta:
        model = Notas
        exclude = ['alumno', 'evaluacion', 'valor']


class NotasUpdateReligionForm(ModelForm):
    class Meta:
        model = Notas
        exclude = ['alumno', 'evaluacion', 'nota']


class MateriaForm(ModelForm):
    class Meta:
        model = Materia
        exclude = ['curso']


class InformePersonalForm(ModelForm):
    class Meta:
        model = InformeDesarrolloPersonal
        exclude = ['alumno', 'item', 'semestre', 'fecha']


class InasistenciaUpdateForm(ModelForm):
    class Meta:
        model = Informacion
        fields = ['inasistencias']


class AtrasoUpdateForm(ModelForm):
    class Meta:
        model = Informacion
        fields = ['atrasos']


class DirectivaForm(ModelForm):
    class Meta:
        model = Directiva


class DirectivaUpdateForm(ModelForm):
    class Meta:
        model = Directiva
        exclude = ['imagen']


class AntecedentesForm(ModelForm):
    class Meta:
        model = AntecedentesAlumno
        fields = ['nombrep', 'gradop','ocupacionp', 'nombrem', 'gradom', 'ocupacionm']


class AntecedentesEconomicosForm(ModelForm):
    class Meta:
        model = AntecedentesAlumno
        fields = ['vive', 'hermanos', 'lugar', 'personas', 'Vivienda', 'habitaciones', 'renta', 'beneficiochs', 'fonasa', 'previcion', 'isapre', 'religion', 'pae']


class AntecedentesSaludForm(ModelForm):
    class Meta:
        model = AntecedentesAlumno
        fields = ['certificadoMedico', 'dificultades', 'dificultad', 'alergias', 'alergia']


class DiasTrabajadosUpdateForm(ModelForm):
    class Meta:
        model = DiasTrabajados
        fields = ['diastrabajados']


class ObservacionesAlumnoForm(ModelForm):
    class Meta:
        model = ObservacionesAlumno
        exclude = ["alumno"]


class PromoverForm(ModelForm):
    class Meta:
        model = AlumnoCurso
        fields = ["curso"]


class AsignarForm(ModelForm):
    class Meta:
        model = AlumnoCurso
        exclude = ['alumno', 'promedio']


class MatriculaForm(ModelForm):
    class Meta:
        model = Alumno
        fields = ['matricula']


class DeleteEvaForm(ModelForm):
    class Meta:
        model = Evaluacion
        fields = []


class UsserForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)


class MateriaUpForm(ModelForm):
    class Meta:
        model = Materia
        exclude = ['curso']


class CursoUpForm(ModelForm):
    class Meta:
        model = Curso


class Info_PerForm(ModelForm):
    class Meta:
        model = DesarrolloPersonal
