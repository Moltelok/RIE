# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Establecimiento(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    rol = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    logo = models.ImageField(
        upload_to='img/',
        blank=True,
        null=True
    )

    def __unicode__(self):
        return u"{0}".format(
            self.nombre
        )

    class Meta:
        verbose_name = u'Establecimiento'
        verbose_name_plural = u'Establecimientos'


TIPO_PERFIL = (
    ('admin', u'Administrador'),
    ('director', u'Director'),
    ('utp', u'Jefe de Unidad Técnica Pedagógica'),
    ('inspector', u'Inspector General'),
    ('secretario', u'Secretario General'),
    ('profesor', u'Profesor'),
    ('externo', u'Usuario Externo')
)


class Perfil(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(
        max_length=50,
        choices=TIPO_PERFIL
    )
    establecimiento = models.ForeignKey(
        Establecimiento,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __unicode__(self):
        return u"{0} {1} de {2}".format(
            self.usuario,
            self.establecimiento,
            self.get_tipo_display()
        )

    class Meta:
        verbose_name = u'Perfil'
        verbose_name_plural = u'Perfiles'


class DatosUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=200)
    activo = models.BooleanField(default=0)

    def __unicode__(self):
        return u"{0}".format(
            self.usuario
        )

    class Meta:
        verbose_name = u'Datos Usuario'
        verbose_name_plural = u'Datos Usuarios'


class Alumno(models.Model):
    matricula = models.IntegerField()
    rut = models.CharField(max_length=15, unique=True)
    nombres = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField(verbose_name='Fecha de Nacimiento')
    domicilio = models.CharField(max_length=200)
    procedencia = models.CharField(max_length=200)

    def __unicode__(self):
        return u"{0} {1}".format(
            self.nombres,
            self.apellidos
        )

    class Meta:
        verbose_name = u'Alumno'
        verbose_name_plural = u'Alumnos'


class Apoderado(models.Model):
    alumno = models.OneToOneField(Alumno, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200, verbose_name='Nombre completo')
    rut_a = models.CharField(max_length=200, verbose_name='Rut')
    telefono = models.CharField(max_length=20)
    celular = models.CharField(max_length=20)
    otroapoderado = models.CharField(max_length=200, blank=True, null=True, verbose_name='Nombre Apoderado Alterno')
    telefonootroapoderado = models.CharField(max_length=20, blank=True, null=True,
                                             verbose_name='Telefono Apoderado Alterno')

    def __unicode__(self):
        return u"{0} apoderado de {1}".format(
            self.nombre,
            self.alumno
        )

    class Meta:
        verbose_name = u'Apoderado'
        verbose_name_plural = u'Apoderados'


class TipoVivienda(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    def __unicode__(self):
        return u"{0}".format(
            self.nombre
        )

    class Meta:
        verbose_name = u'Tipo de Vivienda'
        verbose_name_plural = u'Tipos de Vivienda'


class AntecedentesAlumno(models.Model):
    alumno = models.OneToOneField(Alumno, on_delete=models.CASCADE)
    nombrep = models.CharField(max_length=200, verbose_name='Nombre Padre', blank=True, null=True)
    gradop = models.CharField(max_length=200, blank=True, null=True, verbose_name='Escolaridad Padre')
    ocupacionp = models.CharField(max_length=200, blank=True, null=True, verbose_name='Ocupación Padre')
    nombrem = models.CharField(max_length=200, verbose_name='Nombre Madre', blank=True, null=True)
    gradom = models.CharField(max_length=200, blank=True, null=True, verbose_name='Escolaridad Madre')
    ocupacionm = models.CharField(max_length=200, blank=True, null=True, verbose_name='Ocupación Madre')
    vive = models.CharField(max_length=200, verbose_name='Vive con', blank=True, null=True)
    hermanos = models.IntegerField(verbose_name='N° hermanos', blank=True, null=True)
    lugar = models.CharField(max_length=200, blank=True, null=True)
    personas = models.IntegerField(verbose_name='N° de personas', blank=True, null=True)
    Vivienda = models.ForeignKey(TipoVivienda, on_delete=models.CASCADE, blank=True, null=True)
    habitaciones = models.IntegerField(verbose_name='N° de habitaciones', blank=True, null=True)
    renta = models.CharField(max_length=200, verbose_name='Renta mensual', blank=True, null=True)
    beneficiochs = models.BooleanField(default=False, verbose_name='Recibe beneficios de Chile Solidario')
    fonasa = models.CharField(max_length=200, verbose_name='Previsión Fonasa', blank=True, null=True)
    isapre = models.CharField(max_length=200, verbose_name='Señale Isapre', blank=True, null=True)
    previcion = models.CharField(max_length=200, verbose_name='Señale otra Previsión', blank=True, null=True)
    religion = models.CharField(max_length=200, blank=True, null=True)
    pae = models.BooleanField(default=False, verbose_name='Postula al P.A.E')
    certificadoMedico = models.BooleanField(default=False)
    dificultades = models.BooleanField(default=False)
    dificultad = models.TextField(max_length=200, verbose_name='Mencionar Dificultad', blank=True, null=True)
    alergias = models.BooleanField(default=False)
    alergia = models.TextField(max_length=200, verbose_name='Mencionar Alergias', blank=True, null=True)

    def __unicode__(self):
        return u"{0}".format(
            self.alumno
        )

    class Meta:
        verbose_name = u'Antecedentes Alumno'
        verbose_name_plural = u'Antecedentes Alumnos'


class Curso(models.Model):
    nombre = models.CharField(max_length=200)
    profesor_jefe = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    anio = models.IntegerField(verbose_name='Año')
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE)

    def __unicode__(self):
        return u"{0} {1}".format(
            self.nombre,
            self.profesor_jefe
        )

    class Meta:
        verbose_name = u'Curso'
        verbose_name_plural = u'Cursos'


class Materia(models.Model):
    nombre = models.CharField(max_length=200)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    profesor = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    orden = models.PositiveIntegerField(default=1)

    def __unicode__(self):
        return u"{0} | {1}".format(
            self.nombre,
            self.curso
        )

    class Meta:
        verbose_name = u'Materia'
        verbose_name_plural = u'Materias'
        ordering = ['orden', 'nombre']


class AlumnoCurso(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)

    def __unicode__(self):
        return u"{0} de {1}".format(
            self.alumno,
            self.curso
        )

    class Meta:
        verbose_name = u'Alumno Curso'
        verbose_name_plural = u'Alumnos Cursos'
        ordering = ["alumno"]


semestres = (
    ('primer_semestre', 'Primer Semestre'),
    ('segundo semestre', 'Segundo Semestre'),
    ('anual', 'Anual')
)


class Evaluacion(models.Model):
    nombre = models.CharField(max_length=200)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    descripcion = models.TextField(max_length=500)
    semestre = models.CharField(max_length=50, choices=semestres)
    fecha = models.DateField()

    def __unicode__(self):
        return u"{0} {1}".format(
            self.nombre,
            self.materia
        )

    class Meta:
        verbose_name = u'Evaluacion'
        verbose_name_plural = u'Evaluaciones'
        ordering = ["materia", "fecha"]


valores = (
    (4, 'MB'),
    (3, 'B'),
    (2, 'S'),
    (1, 'I')
)


class Nota(models.Model):
    alumno = models.ForeignKey(AlumnoCurso, on_delete=models.CASCADE)
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    nota = models.FloatField(max_length=5, blank=True, null=True)
    valor = models.IntegerField(choices=valores, null=True, blank=True, default=4)

    def __unicode__(self):
        return u"{0} {1}".format(
            self.alumno,
            self.evaluacion
        )

    class Meta:
        verbose_name = u'Nota'
        verbose_name_plural = u'Notas'
        ordering = ["alumno", "evaluacion"]


meses = (
    (1, 'Enero'),
    (2, 'Febrero'),
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
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    mes = models.IntegerField(choices=meses, default=1)
    diastrabajados = models.IntegerField(default=0, verbose_name='Dias trabajados')

    def __unicode__(self):
        return u"{0} - {1}".format(
            self.curso,
            self.mes
        )

    class Meta:
        verbose_name = u'Días Trabajados'
        verbose_name_plural = u'Días Trabajados'


class AsistenciaAlumno(models.Model):
    alumno = models.ForeignKey(AlumnoCurso, on_delete=models.CASCADE)
    mes = models.IntegerField(choices=meses, default=1)
    inasistencias = models.IntegerField(default=0)
    atrasos = models.IntegerField(default=0)
    asistencia = models.IntegerField(default=0)
    puntualidad = models.IntegerField(default=0)
    fecha = models.DateField(auto_now=True)

    def __unicode__(self):
        return u"{0} - {1}".format(
            self.alumno,
            self.mes
        )

    class Meta:
        verbose_name = u'Asistencia Alumno'
        verbose_name_plural = u'Asistencias Alumnos'


class AreaDesarrolloPersonal(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(
        max_length=2500
    )

    def __unicode__(self):
        return u"{0}".format(
            self.nombre
        )

    class Meta:
        verbose_name = u'Área de Desarrollo Personal'
        verbose_name_plural = u'Áreas de Desarrollo Personal'


class ItemDesarrolloPersonal(models.Model):
    nombre = models.CharField(max_length=200)
    area = models.ForeignKey(AreaDesarrolloPersonal, on_delete=models.CASCADE)
    descripcion = models.TextField(
        max_length=2500
    )

    def __unicode__(self):
        return u"{0} - {1}".format(
            self.nombre,
            self.area
        )

    class Meta:
        verbose_name = u'Item de Área de Desarrollo Personal'
        verbose_name_plural = u'Items de Área de Desarrollo Personal'
        ordering = ['nombre', 'area']


valores_desarrollo = (
    (0, 'Ocasionalmente'),
    (1, 'Generalmente'),
    (2, 'Siempre')
)


class InformeDesarrolloPersonal(models.Model):
    alumno = models.ForeignKey(AlumnoCurso, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemDesarrolloPersonal, on_delete=models.CASCADE)
    valor = models.IntegerField(choices=valores_desarrollo, default=2)
    semestre = models.IntegerField(choices=semestres, default=1)
    fecha = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return u"{0} - {1}".format(
            self.alumno,
            self.item
        )

    class Meta:
        verbose_name = u'Informe de Desarrollo Personal'
        verbose_name_plural = u'Informe de Desarrollo Personal'
        ordering = ['item']


class AlumnoMateriaPromedio(models.Model):
    alumno = models.ForeignKey(AlumnoCurso, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    promedio = models.FloatField(max_length=3, default=0, blank=True, null=True)
    semestre = models.IntegerField(choices=semestres, default=1)
    valor = models.IntegerField(choices=valores, null=True, blank=True, default=4)

    def __unicode__(self):
        return u"{0} - {1}".format(
            self.alumno,
            self.materia
        )

    class Meta:
        verbose_name = u'Promedio por Materia del Alumno'
        verbose_name_plural = u'Promedios por Materias de los Alumnos'
        ordering = ["semestre"]


class PromedioAlumno(models.Model):
    alumno = models.ForeignKey(AlumnoCurso, on_delete=models.CASCADE)
    mes = models.IntegerField(choices=semestres, default=1)
    promedio = models.FloatField(max_length=3, default=0)
    promedio_neto = models.FloatField(max_length=6)

    def __unicode__(self):
        return u"{0} - {1}".format(
            self.alumno,
            self.mes
        )

    class Meta:
        verbose_name = u'Promedio Alumno'
        verbose_name_plural = u'Promedios Alumnos'
        ordering = ["mes"]


class ObservacionAlumno(models.Model):
    alumno = models.ForeignKey(AlumnoCurso, on_delete=models.CASCADE)
    semestre = models.IntegerField(choices=semestres, default=1)
    observacion = models.TextField(max_length=2000, null=True, blank=True)

    def __unicode__(self):
        return u"{0} - {1}".format(
            self.alumno,
            self.semestre
        )

    class Meta:
        verbose_name = u'Observación Alumno'
        verbose_name_plural = u'Observaciones Alumnos'
        ordering = ["semestre"]
