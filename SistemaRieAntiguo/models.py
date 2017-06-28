# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Alumno(models.Model):
    matricula = models.IntegerField(max_length=20)
    rut = models.CharField(max_length=15, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(verbose_name='Fecha de Nacimiento')
    domicilio = models.CharField(max_length=100)
    procedencia = models.CharField(max_length=100)

    def __unicode__(self):
        return u"%s" % self.apellidos + ' ' + self.nombres

    class Meta:
        ordering = ["apellidos"]


class Apoderado(models.Model):
    alumno = models.OneToOneField(Alumno)
    nombre = models.CharField(max_length=100, verbose_name='Nombre completo')
    rut_a = models.CharField(max_length=100, verbose_name='Rut')
    telefono = models.CharField(max_length=20)
    celular = models.CharField(max_length=20)
    otroapoderado = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nombre Apoderado Alterno')
    telefonootroapoderado = models.CharField(max_length=20, blank=True, null=True,
                                             verbose_name='Telefono Apoderado Alterno')

    def __unicode__(self):
        return u"%s" % self.nombre + ' - ' + self.alumno.nombres + ' - ' + self.alumno.apellidos

    class Meta:
        ordering = ["alumno"]


class AntecedentesAlumno(models.Model):
    alumno = models.OneToOneField(Alumno)
    nombrep = models.CharField(max_length=100, verbose_name='Nombre Padre', blank=True, null=True)
    gradop = models.CharField(max_length=100, blank=True, null=True, verbose_name='Escolaridad Padre')
    ocupacionp = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ocupación Padre')
    nombrem = models.CharField(max_length=100, verbose_name='Nombre Madre', blank=True, null=True)
    gradom = models.CharField(max_length=100, blank=True, null=True, verbose_name='Escolaridad Madre')
    ocupacionm = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ocupación Madre')
    vive = models.CharField(max_length=100, verbose_name='Vive con', blank=True, null=True)
    hermanos = models.IntegerField(max_length=3, verbose_name='N° hermanos', blank=True, null=True)
    lugar = models.CharField(max_length=100, blank=True, null=True)
    personas = models.IntegerField(max_length=3, verbose_name='N° de personas', blank=True, null=True)
    viviendas = ((0, 'P'), (1, 'A'), (2, 'C'))
    Vivienda = models.IntegerField(choices=viviendas, max_length=2, default=0, blank=True, null=True)
    habitaciones = models.IntegerField(max_length=3, verbose_name='N° de habitaciones', blank=True, null=True)
    renta = models.CharField(max_length=100, verbose_name='Renta mensual', blank=True, null=True)
    beneficiochs = models.BooleanField(default=False, verbose_name='Recibe beneficios de Chile Solidario')
    fonasa = models.CharField(max_length=100, verbose_name='Previsión Fonasa', blank=True, null=True)
    isapre = models.CharField(max_length=100, verbose_name='Señale Isapre', blank=True, null=True)
    previcion = models.CharField(max_length=100, verbose_name='Señale otra Previsión', blank=True, null=True)
    religion = models.CharField(max_length=100, blank=True, null=True)
    pae = models.BooleanField(default=False, verbose_name='Postula al P.A.E')
    certificadoMedico = models.BooleanField(default=False)
    dificultades = models.BooleanField(default=False)
    dificultad = models.TextField(max_length=100, verbose_name='Mencionar Dificultad', blank=True, null=True)
    alergias = models.BooleanField(default=False)
    alergia = models.TextField(max_length=100, verbose_name='Mencionar Alergias', blank=True, null=True)

    def __unicode__(self):
        return self.alumno.nombres + ' ' + self.alumno.apellidos


class Logo(models.Model):
    logo = models.ImageField(upload_to='img/', verbose_name='Imagen', blank=True, null=True)


class Profesor(models.Model):
    usuario = models.OneToOneField(User, unique=True)
    rut = models.CharField(max_length=15)
    nombre = models.CharField(max_length=100, verbose_name='Nombre Completo')
    correo = models.CharField(max_length=50)
    logo = models.ForeignKey(Logo, blank=True, null=True)

    def __unicode__(self):
        return u"%s" % self.nombre


class Directiva(models.Model):
    funcionario = models.OneToOneField(Profesor)
    cargos = ((0, 'Director'), (1, 'Jefe de UTP'))
    cargo = models.IntegerField(choices=cargos)

    def __unicode__(self):
        return u"%s" % self.funcionario.nombre


class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    profesor_jefe = models.ForeignKey(Profesor)
    anio = models.IntegerField(max_length=4, verbose_name='Año')

    def __unicode__(self):
        return u"%s" % self.nombre + ' - ' + self.profesor_jefe.nombre + ' - ' + str(self.anio)

    class Meta:
        ordering = ["-anio", "nombre"]


class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    curso = models.ForeignKey(Curso)
    profesor = models.ForeignKey(Profesor)
    orden = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["orden", "nombre"]

    def __unicode__(self):
        return u"%s" % self.nombre + ' - ' + self.curso.nombre


class AlumnoCurso(models.Model):
    curso = models.ForeignKey(Curso)
    alumno = models.ForeignKey(Alumno)

    def __unicode__(self):
        return self.alumno.nombres + ' ' + self.alumno.apellidos + ' - ' + self.curso.nombre

    class Meta:
        ordering = ["alumno"]


semestres = ((1, 'primer semestre'), (2, 'segundo semestre'), (3, 'anual'))


class Evaluacion(models.Model):
    nombre = models.CharField(max_length=100)
    materia = models.ForeignKey(Materia)
    descripcion = models.TextField(max_length=500)
    semestre = models.IntegerField(max_length=20, choices=semestres, default=1)
    fecha = models.DateField()

    def __unicode__(self):
        return self.nombre + ' - ' + self.materia.nombre

    class Meta:
        ordering = ["materia", "fecha"]


class Notas(models.Model):
    alumno = models.ForeignKey(AlumnoCurso)
    evaluacion = models.ForeignKey(Evaluacion)
    nota = models.FloatField(max_length=5, blank=True, null=True)
    valores = ((4, 'MB'), (3, 'B'), (2, 'S'), (1, 'I'))
    valor = models.IntegerField(choices=valores, max_length=10, null=True, blank=True, default=4)

    def __unicode__(self):
        return self.alumno.alumno.nombres + ' ' + self.alumno.alumno.apellidos + ' - ' + self.evaluacion.nombre

    class Meta:
        ordering = ["alumno", "evaluacion"]


meses = (
    (3, 'Marzo'),
    (4, 'Abril'),
    (5, 'Mayo'),
    (6, 'Junio'),
    (7, 'Julio'),
    (8, 'Agosto'),
    (9, 'Septiembre'),
    (10, 'Octubre'),
    (11, 'Noviembre'),
    (12, 'Diciembre'),
    (13, 'Primer Semestre'),
    (14, 'Segundo Semestre'),
    (15, 'Anual')
)


class DiasTrabajados(models.Model):
    curso = models.ForeignKey(Curso)
    mes = models.IntegerField(max_length=20, choices=meses, default=1)
    diastrabajados = models.IntegerField(max_length=3, default=0, verbose_name='Dias trabajados')

    def __unicode__(self):
        return self.curso.nombre + ' - ' + str(self.mes) + ' >> ' + str(self.diastrabajados)


class Informacion(models.Model):
    alumno = models.ForeignKey(AlumnoCurso)
    mes = models.IntegerField(max_length=20, choices=meses, default=1)
    inasistencias = models.IntegerField(max_length=2, default=0)
    atrasos = models.IntegerField(max_length=2, default=0)
    asistencia = models.IntegerField(max_length=2, default=0)
    puntualidad = models.IntegerField(max_length=2, default=0)
    fecha = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.alumno.alumno.nombres + ' ' + self.alumno.alumno.apellidos + ' - ' + str(self.mes) + ' >> ' + str(
            self.inasistencias)


class DesarrolloPersonal(models.Model):
    areas = ((0, 'Area Personal'), (1, 'Area Afectiva y Social'), (2, 'Desarrollo Pensamiento'))
    area = models.IntegerField(max_length=20, choices=areas, default=0)
    descripcion_item = models.TextField(max_length=500)

    def __unicode__(self):
        return str(self.area) + '' + self.descripcion_item

    class Meta:
        ordering = ['area', 'descripcion_item']


class InformeDesarrolloPersonal(models.Model):
    alumno = models.ForeignKey(AlumnoCurso)
    item = models.ForeignKey(DesarrolloPersonal)
    valores = ((0, 'Ocasionalmente'), (1, 'Generalmente'), (2, 'Siempre'))
    valor = models.IntegerField(max_length=20, choices=valores, default=2)
    semestre = models.IntegerField(max_length=20, choices=semestres, default=1)
    fecha = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.alumno.alumno.nombres + ' ' + self.alumno.alumno.apellidos + ' - ' + self.item.descripcion_item + ' >> ' + str(
            self.valor)

    class Meta:
        ordering = ['item']


class AlumnoMateriaPromedio(models.Model):
    alumno = models.ForeignKey(AlumnoCurso)
    materia = models.ForeignKey(Materia)
    promedio = models.FloatField(max_length=3, default=0, blank=True, null=True)
    semestre = models.IntegerField(choices=semestres, default=1)
    valores = ((4, 'MB'), (3, 'B'), (2, 'S'), (1, 'I'))
    valor = models.IntegerField(choices=valores, max_length=10, null=True, blank=True, default=4)

    def __unicode__(self):
        return str(self.alumno.alumno.nombres) + ' - ' + self.materia.nombre

    class Meta:
        ordering = ["semestre"]


class PromedioAlumno(models.Model):
    alumno = models.ForeignKey(AlumnoCurso)
    mes = models.IntegerField(choices=semestres, default=1)
    promedio = models.FloatField(max_length=3, default=0)
    promedio_neto = models.FloatField(max_length=6)

    def __unicode__(self):
        return self.alumno.alumno.nombres + ' - ' + self.get_mes_display() + ' - ' + str(self.promedio)

    class Meta:
        ordering = ["mes"]


class ObservacionesAlumno(models.Model):
    alumno = models.ForeignKey(AlumnoCurso)
    semestre = models.IntegerField(choices=semestres, default=1)
    observacion = models.TextField(max_length=1000, null=True, blank=True)

    def __unicode__(self):
        return self.alumno.alumno.nombres + ' - ' + self.alumno.curso.nombre + ' - ' + self.get_semestre_display()

    class Meta:
        ordering = ["semestre"]
