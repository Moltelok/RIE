# -*- coding: utf-8 -*-
import datetime

from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, add_to_builtins
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.core.urlresolvers import reverse
from easy_pdf.views import PDFTemplateView
from django.template import add_to_builtins

from sanvalentin_app.forms import *

add_to_builtins('djangojs.templatetags.js')


class LoginRequired(object):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequired, self).dispatch(request, *args, **kwargs)


@login_required(login_url='login')
def home(request):
    return render(request, 'sanvalentin_app/home.html')


@login_required(login_url='login')
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')


def iniciar_sesion(request):
    if request.method == "POST":
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.add_message(request, messages.ERROR,
                                         u"Su cuenta se encuentra inactiva, converse con el administrador para solucionar su problema.")
            else:
                messages.add_message(request, messages.ERROR,
                                     u"Error en su contraseña o nombre de usuario. Vuelva a intentarlo.")
    else:
        messages.add_message(request, messages.INFO, u"Ingrese con su usuario")
        formulario = AuthenticationForm()
    return render(request, 'registration/login.html', {'formulario': formulario})


def porcentaje(i, t):
    porcentaje = i * 100 / t
    porcentaje = round(porcentaje, 1)
    porcentaje = 100 - porcentaje
    return porcentaje


@login_required(login_url='login')
def nuevo_alumno(request, curso):
    curso = get_object_or_404(Curso, pk=curso)
    if request.method == 'POST':
        formulario_alumno = AlumnoForm(request.POST)
        formulario_apoderado = ApoderadoForm(request.POST)
        formulario_antecedentesf = AntecedentesForm(request.POST)
        formulario_antecedentess = AntecedentesEconomicosForm(request.POST)
        formulario_salud = AntecedentesSaludForm(request.POST)
        if formulario_alumno.is_valid() and formulario_apoderado.is_valid() and formulario_antecedentesf.is_valid() and formulario_antecedentess.is_valid() and formulario_salud.is_valid():
            matricula = formulario_alumno.cleaned_data.get('matricula', None)
            rut = formulario_alumno.cleaned_data.get('rut', None)
            nombres = formulario_alumno.cleaned_data.get('nombres', None)
            apellidos = formulario_alumno.cleaned_data.get('apellidos', None)
            fecha = formulario_alumno.cleaned_data.get('fecha_nacimiento', None)
            domicilio = formulario_alumno.cleaned_data.get('domicilio', None)
            procedencia = formulario_alumno.cleaned_data.get('procedencia', None)

            alumno = Alumno.objects.create(matricula=matricula, rut=rut, nombres=nombres, apellidos=apellidos,
                                           fecha_nacimiento=fecha, domicilio=domicilio, procedencia=procedencia)
            alumnocurso = AlumnoCurso.objects.create(curso=curso, alumno=alumno)

            nombre = formulario_apoderado.cleaned_data.get('nombre', None)
            rut_a = formulario_apoderado.cleaned_data.get('rut_a', None)
            telefono = formulario_apoderado.cleaned_data.get('telefono', None)
            celular = formulario_apoderado.cleaned_data.get('celular', None)
            otroapoderado = formulario_apoderado.cleaned_data.get('otroapoderado', None)
            telefonootroapoderado = formulario_apoderado.cleaned_data.get('telefonootroapoderado', None)

            Apoderado.objects.create(alumno=alumno, nombre=nombre, rut_a=rut_a, telefono=telefono, celular=celular,
                                     otroapoderado=otroapoderado, telefonootroapoderado=telefonootroapoderado)

            nombrep = formulario_antecedentesf.cleaned_data.get('nombrep', None)
            gradop = formulario_antecedentesf.cleaned_data.get('gradop', None)
            ocupacionp = formulario_antecedentesf.cleaned_data.get('ocupacionp', None)
            nombrem = formulario_antecedentesf.cleaned_data.get('nombrem', None)
            gradom = formulario_antecedentesf.cleaned_data.get('gradom', None)
            ocupacionm = formulario_antecedentesf.cleaned_data.get('ocupacionm', None)

            vive = formulario_antecedentess.cleaned_data.get('vive', None)
            hermanos = formulario_antecedentess.cleaned_data.get('hermanos', None)
            lugar = formulario_antecedentess.cleaned_data.get('lugar', None)
            personas = formulario_antecedentess.cleaned_data.get('personas', None)
            Vivienda = formulario_antecedentess.cleaned_data.get('Vivienda', None)
            habitaciones = formulario_antecedentess.cleaned_data.get('habitaciones', None)
            renta = formulario_antecedentess.cleaned_data.get('renta', None)
            beneficiochs = formulario_antecedentess.cleaned_data.get('beneficiochs', None)
            fonasa = formulario_antecedentess.cleaned_data.get('fonasa', None)
            isapre = formulario_antecedentess.cleaned_data.get('isapre', None)
            previcion = formulario_antecedentess.cleaned_data.get('previcion', None)
            religion = formulario_antecedentess.cleaned_data.get('religion', None)
            pae = formulario_antecedentess.cleaned_data.get('pae', None)

            certificadoMedico = formulario_salud.cleaned_data.get('certificadoMedico', None)
            dificultades = formulario_salud.cleaned_data.get('dificultades', None)
            dificultad = formulario_salud.cleaned_data.get('dificultad', None)
            alergias = formulario_salud.cleaned_data.get('alergias', None)
            alergia = formulario_salud.cleaned_data.get('alergia', None)

            AntecedentesAlumno.objects.create(alumno=alumno, nombrep=nombrep, gradop=gradop, ocupacionp=ocupacionp,
                                              nombrem=nombrem, gradom=gradom, ocupacionm=ocupacionm,
                                              vive=vive, hermanos=hermanos, lugar=lugar, personas=personas,
                                              Vivienda=Vivienda, habitaciones=habitaciones, renta=renta,
                                              beneficiochs=beneficiochs, fonasa=fonasa, isapre=isapre,
                                              previcion=previcion, religion=religion, pae=pae,
                                              certificadoMedico=certificadoMedico, dificultades=dificultades,
                                              dificultad=dificultad, alergias=alergias, alergia=alergia)

            dp = DesarrolloPersonal.objects.all()

            for x in dp:
                InformeDesarrolloPersonal.objects.create(alumno=alumnocurso, item=x)
                InformeDesarrolloPersonal.objects.create(alumno=alumnocurso, item=x, semestre=2)
            for m in curso.materia_set.all():
                for e in m.evaluacion_set.all():
                    Notas.objects.create(alumno=alumnocurso, evaluacion=e, nota=0)
                AlumnoMateriaPromedio.objects.create(alumno=alumnocurso, materia=m, promedio=0, semestre=1)
                AlumnoMateriaPromedio.objects.create(alumno=alumnocurso, materia=m, promedio=0, semestre=2)
                AlumnoMateriaPromedio.objects.create(alumno=alumnocurso, materia=m, promedio=0, semestre=3)

            PromedioAlumno.objects.create(alumno=alumnocurso, mes=1, promedio=0, promedio_neto=0)
            PromedioAlumno.objects.create(alumno=alumnocurso, mes=2, promedio=0, promedio_neto=0)
            PromedioAlumno.objects.create(alumno=alumnocurso, mes=3, promedio=0, promedio_neto=0)

            meses = ['3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
            for mes in meses:
                Informacion.objects.create(alumno=alumnocurso, mes=mes, inasistencias=0, atrasos=0, asistencia=100,
                                           puntualidad=100)
            return redirect('listar-cursoalumno', curso.id)
    else:
        formulario_alumno = AlumnoForm()
        formulario_apoderado = ApoderadoForm()
        formulario_antecedentesf = AntecedentesForm()
        formulario_antecedentess = AntecedentesEconomicosForm()
        formulario_salud = AntecedentesSaludForm()
    return render_to_response('sanvalentin_app/addalumno.html',
                              {'formulario_alumno': formulario_alumno, 'formulario_apoderado': formulario_apoderado,
                               'formulario_antecedentesf': formulario_antecedentesf,
                               'formulario_antecedentess': formulario_antecedentess,
                               'formulario_salud': formulario_salud},
                              context_instance=RequestContext(request))


@login_required(login_url='login')
def nuevo_profesor(request):
    if request.method == 'POST':
        formulario_profesor = ProfesorForm(request.POST)
        if formulario_profesor.is_valid():
            rut = formulario_profesor.cleaned_data.get('rut', None)
            nombre = formulario_profesor.cleaned_data.get('nombre', None)
            correo = formulario_profesor.cleaned_data.get('correo', None)

            user_name = correo.split('@')
            u = User.objects.create_user(user_name[0], correo, rut)
            u.save()

            Profesor.objects.create(usuario=u, rut=rut, nombre=nombre, correo=correo)

            return HttpResponseRedirect('/home')
    else:
        formulario_profesor = ProfesorForm()
    return render_to_response('sanvalentin_app/addprofesor.html',
                              {'formulario_profesor': formulario_profesor},
                              context_instance=RequestContext(request))


@login_required(login_url='login')
def nuevo_curso(request):
    if request.method == 'POST':
        formulario_curso = CursoForm(request.POST)
        if formulario_curso.is_valid():
            curso = formulario_curso.save()

            meses = ['3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
            for mes in meses:
                DiasTrabajados.objects.create(curso=curso, mes=mes, diastrabajados=0)
            materia = Materia.objects.create(nombre='Religion', curso=curso, profesor=curso.profesor_jefe)
            evaluacion = Evaluacion.objects.create(nombre='Evaluacion 01', materia=materia,
                                                   descripcion='Evaluacion de Prueba',
                                                   fecha=datetime.datetime.now())

            return redirect('detalle-curso', curso.id)
    else:
        formulario_curso = CursoForm()
    return render_to_response('sanvalentin_app/addcurso.html',
                              {'formulario_curso': formulario_curso},
                              context_instance=RequestContext(request))


class ProfesorListView(LoginRequired, ListView):
    model = Profesor
    context_object_name = 'profesores'
    template_name = 'sanvalentin_app/profesor_list.html'

    def get_queryset(self):
        name = self.request.GET.get('name', None)
        qs = super(ProfesorListView, self).get_queryset()
        if name:
            qs = qs.filter(nombre__icontains=name)
        return qs


class CursoListView(LoginRequired, ListView):
    model = Curso
    context_object_name = 'cursos'
    template_name = 'sanvalentin_app/curso_lista.html'

    def get_queryset(self):
        name = self.request.GET.get('name', None)
        qs = super(CursoListView, self).get_queryset()
        anio = datetime.datetime.now().year
        if name:
            qs = qs.filter(nombre__icontains=name)
        return qs


class ProfesorMateriasDetailView(LoginRequired, DetailView):
    model = Profesor
    template_name = 'sanvalentin_app/materias.html'

    def get_context_data(self, **kwargs):
        context = super(ProfesorMateriasDetailView, self).get_context_data(**kwargs)
        context['profesores'] = Profesor.objects.all()
        name = self.request.GET.get('name', None)
        if name:
            context['profesores'] = Profesor.objects.filter(nombre__icontains=name)
        return context


class IDPListView(LoginRequired, ListView):
    model = InformeDesarrolloPersonal
    context_object_name = 'items'
    template_name = 'sanvalentin_app/informe_personal.html'

    def get_queryset(self):
        qs = super(IDPListView, self).get_queryset()
        return qs.filter(alumno=self.kwargs['alumno'])


class CursoMateriaDetailView(LoginRequired, DetailView):
    model = Curso
    template_name = 'sanvalentin_app/materias_curso.html'

    def get_context_data(self, **kwargs):
        context = super(CursoMateriaDetailView, self).get_context_data(**kwargs)
        context['cursos'] = Curso.objects.all()
        name = self.request.GET.get('name', None)
        if name:
            context['cursos'] = Curso.objects.filter(nombre__icontains=name)
        return context


class CursoDetailView(LoginRequired, DetailView):
    model = Curso
    context_object_name = 'curso'
    template_name = 'sanvalentin_app/alumnocurso_lista.html'

    def get_context_data(self, **kwargs):
        context = super(CursoDetailView, self).get_context_data(**kwargs)
        context['cursos'] = Curso.objects.all()
        name = self.request.GET.get('name', None)
        if name:
            context['cursos'] = Curso.objects.filter(nombre__icontains=name)
        return context


class CursoDetalleDetailView(LoginRequired, DetailView):
    model = Curso
    template_name = 'sanvalentin_app/cursodetalle_lista.html'

    def get_context_data(self, **kwargs):
        context = super(CursoDetalleDetailView, self).get_context_data(**kwargs)
        context['cursos'] = Curso.objects.all()
        name = self.request.GET.get('name', None)
        if name:
            context['cursos'] = Curso.objects.filter(nombre__icontains=name)
        return context


class ProfesorDetailView(LoginRequired, DetailView):
    model = Profesor
    template_name = 'sanvalentin_app/profesor_detalle.html'

    def get_context_data(self, **kwargs):
        context = super(ProfesorDetailView, self).get_context_data(**kwargs)
        context['profesores'] = Profesor.objects.all()
        name = self.request.GET.get('name', None)
        if name:
            context['profesores'] = Profesor.objects.filter(nombre__icontains=name)
        return context


class DireccionListView(LoginRequired, ListView):
    model = Directiva
    context_object_name = 'directiva'
    template_name = 'sanvalentin_app/direccion.html'


class EvaluacionDetailView(LoginRequired, DetailView):
    model = Evaluacion
    template_name = 'sanvalentin_app/evaluacion.html'

    def get_context_data(self, **kwargs):
        context = super(EvaluacionDetailView, self).get_context_data(**kwargs)
        return context


def update_prom_alumno(alumno):
    alumno = get_object_or_404(AlumnoCurso, id=alumno)
    pmps = []
    for pm in alumno.alumnomateriapromedio_set.all():
        if pm.semestre == 1 and pm.promedio > 0.0:
            pmps.append(pm.promedio)
    pmss = []
    for pm in alumno.alumnomateriapromedio_set.all():
        if pm.semestre == 2 and pm.promedio > 0.0:
            pmss.append(pm.promedio)
    pma = []
    for pm in alumno.alumnomateriapromedio_set.all():
        if pm.semestre == 3 and pm.promedio > 0.0:
            pma.append(pm.promedio)
    if len(pmps) > 0:
        paps = promedio(pmps, len(pmps))
        PromedioAlumno.objects.filter(alumno=alumno, mes=1).update(promedio=round(paps, 1), promedio_neto=(sum(pmps)/len(pmps)))
    if len(pmss) > 0:
        pases = promedio(pmss, len(pmss))
        PromedioAlumno.objects.filter(alumno=alumno, mes=2).update(promedio=round(pases, 1), promedio_neto=(sum(pmss)/len(pmss)))
    if len(pma) > 0:
        paa = promedio(pma, len(pma))
        PromedioAlumno.objects.filter(alumno=alumno, mes=3).update(promedio=round(paa, 1), promedio_neto=(sum(pma)/len(pma)))


def update_prom_anual(materia, alumno):
    materia = get_object_or_404(Materia, pk=materia)
    alumno = get_object_or_404(AlumnoCurso, pk=alumno)
    promedios = []
    for p in alumno.alumnomateriapromedio_set.all():
        if p.semestre != 3 and p.alumno == alumno and p.materia == materia and p.promedio > 0.0:
            promedios.append(p.promedio)
    cont = 0000
    if len(promedios) > 0:
        for n in promedios:
            cont = cont + n
    if len(promedios) != 0:
        pr = cont / len(promedios)
        prome = pr.__str__()
        if len(prome) > 3:
            if prome[3] == '5':
                print 'pr anual ' + prome
                pr += 0.05
    else:
        pr = 0
    AlumnoMateriaPromedio.objects.filter(alumno=alumno, materia=materia, semestre=3).update(
        promedio=round(pr, 1))
    update_prom_alumno(alumno.id)


def update_prom_anual_materia(materia):
    materia = get_object_or_404(Materia, pk=materia)
    for a in materia.curso.alumnocurso_set.all():
        promedios = []
        for p in a.alumnomateriapromedio_set.all():
            if p.semestre != 3 and p.promedio > 0.0:
                promedios.append(p.promedio)
        cont = 0000
        if len(promedios) > 0:
            for n in promedios:
                cont = cont + n
        if len(promedios) != 0:
            pr = cont / len(promedios)
            prome = pr.__str__()
            if len(prome) > 3:
                if prome[3] == '5':
                    print 'pr anual materia ' + prome
                    pr += 0.05
        else:
            pr = 0
        AlumnoMateriaPromedio.objects.filter(alumno=a, materia=materia, semestre=3).update(
            promedio=round(pr, 1))
        update_prom_anual(materia.id, a.id)


def update_promedio_semestre(materia, semestre):
    materia = get_object_or_404(Materia, pk=materia)

    for a in materia.curso.alumnocurso_set.all():
        notas = []
        for n in a.notas_set.all():
            if n.evaluacion.materia == materia and n.evaluacion.semestre == semestre and n.nota > 0.0:
                notas.append(n.nota)
        cont = 0
        for n in notas:
            cont = cont + n
        if len(notas) != 0:
            pr = cont / len(notas)
            prome = pr.__str__()
            print 'prome semestre materia ' + prome
            if len(prome) > 3:
                if prome[3] == '5':
                    print 'pr semestre ' + prome
                    pr += 0.05
        else:
            pr = 0
        AlumnoMateriaPromedio.objects.filter(alumno=a, materia=materia, semestre=semestre).update(
            promedio=round(pr, 1))

    update_prom_anual_materia(materia.id)


@login_required(login_url='login')
def nueva_evaluacion(request, materia):
    materia = get_object_or_404(Materia, pk=materia)
    if request.method == 'POST':

        if materia.nombre == 'Religion' or materia.nombre == 'Religión':
            formulario_evaluacion = EvaluacionForm(request.POST)
            if formulario_evaluacion.is_valid():
                nombre = formulario_evaluacion.cleaned_data.get('nombre', None)
                descripcion = formulario_evaluacion.cleaned_data.get('descripcion', None)
                fecha = formulario_evaluacion.cleaned_data.get('fecha', None)

                if fecha.month >= 8:
                    semestre = 2
                else:
                    semestre = 1

                evaluacion = Evaluacion.objects.create(nombre=nombre, materia=materia, descripcion=descripcion,
                                                       semestre=semestre, fecha=fecha)

                for a in materia.curso.alumnocurso_set.all():
                    Notas.objects.create(alumno=a, evaluacion=evaluacion, valor=0)

                return redirect('materias-nota', evaluacion.materia.id)

        else:
            formulario_evaluacion = EvaluacionForm(request.POST)
            if formulario_evaluacion.is_valid():
                nombre = formulario_evaluacion.cleaned_data.get('nombre', None)
                descripcion = formulario_evaluacion.cleaned_data.get('descripcion', None)
                fecha = formulario_evaluacion.cleaned_data.get('fecha', None)

                if fecha.month >= 8:
                    semestre = 2
                else:
                    semestre = 1

                evaluacion = Evaluacion.objects.create(nombre=nombre, materia=materia, descripcion=descripcion,
                                                       semestre=semestre, fecha=fecha)

                for a in materia.curso.alumnocurso_set.all():
                    Notas.objects.create(alumno=a, evaluacion=evaluacion, nota=0)

                    notas = []
                    for eva in materia.evaluacion_set.all():
                        if eva.semestre == semestre:
                            for n in eva.notas_set.all():
                                if a == n.alumno and n.nota > 0.0:
                                    notas.append(n.nota)
                    cont = 0000
                    for n in notas:
                        cont = cont + n
                    if len(notas) != 0:
                        promedio = cont / len(notas)
                    else:
                        promedio = 0

                    AlumnoMateriaPromedio.objects.filter(alumno=a, materia=materia, semestre=semestre).update(
                        promedio=round(promedio, 1))
                update_prom_anual_materia(materia.id)

            return redirect('materias-nota', evaluacion.materia.id)
    else:
        formulario_evaluacion = EvaluacionForm()
    return render_to_response('sanvalentin_app/addevaluacion.html',
                              {'formulario_evaluacion': formulario_evaluacion, 'materia': materia},
                              context_instance=RequestContext(request))


@login_required(login_url='login')
def alumnosMateriaNota(request, materia):
    materia = get_object_or_404(Materia, id=materia)
    context = {}
    evaluaciones = []
    alumnos = []
    for e in materia.evaluacion_set.all():
        evaluaciones.append(e)
    for a in materia.curso.alumnocurso_set.all():
        alumnos.append(a)
    context['evaluaciones'] = evaluaciones
    context['alumnos'] = alumnos
    context['materia'] = materia
    return render(request, 'sanvalentin_app/alumnos_materia.html', context)


@login_required(login_url='login')
def mod_notas(request, nota):
    id_nota = get_object_or_404(Notas, id=nota)
    if request.method == 'POST':
        cadena = id_nota.evaluacion.materia.nombre
        if cadena == "Religion":
            validar_formulario = NotasUpdateReligionForm(request.POST)
            if validar_formulario.is_valid():
                valor = validar_formulario.cleaned_data.get('valor', None)

                Notas.objects.filter(id=id_nota.id).update(valor=valor)
                valores = []
                for eva in id_nota.evaluacion.materia.evaluacion_set.all():
                    if eva.semestre == id_nota.evaluacion.semestre:
                        for n in eva.notas_set.all():
                            if id_nota.alumno == n.alumno:
                                valores.append(n.valor)
                total = 0
                for val in valores:
                    total = total + val
                lenght = float(len(valores))
                promre = float(total / lenght)
                promrel = promre.__str__()
                if len(promrel) > 2:
                    if promrel[2] == '5':
                        promre += 0.5
                    if promrel[2] > '6':
                        promre += 1
                AlumnoMateriaPromedio.objects.filter(alumno=id_nota.alumno, materia=id_nota.evaluacion.materia.id,
                                                     semestre=id_nota.evaluacion.semestre).update(
                    valor=round(int(promre), 1))
                promsr = []
                for pm in id_nota.evaluacion.materia.alumnomateriapromedio_set.all():
                    if pm.semestre != 3:
                        promsr.append(pm.valor)
                sumpr = 0
                for pr in promsr:
                    sumpr = sumpr + pr
                pra = float(sumpr) / float(len(promsr))
                prar = pra.__str__()
                if len(prar) > 2:
                    print ' dentro del if' + prar
                    if prar[2] == '5':
                        pra += 0.5
                AlumnoMateriaPromedio.objects.filter(alumno=id_nota.alumno, materia=id_nota.evaluacion.materia.id,
                                                     semestre=3).update(valor=round(pra, 1))
        else:
            validar_formulario = NotasUpdateForm(request.POST)
            if validar_formulario.is_valid():
                nota = validar_formulario.cleaned_data.get('nota', None)

                Notas.objects.filter(id=id_nota.id).update(nota=nota)

                notas = []
                materia = id_nota.evaluacion.materia
                alumno = id_nota.alumno
                for eva in materia.evaluacion_set.all():
                    if eva.semestre == id_nota.evaluacion.semestre:
                        for n in eva.notas_set.all():
                            if alumno == n.alumno and n.nota > 0.0:
                                notas.append(n.nota)
                cont = 0
                for n in notas:
                    cont = cont + n
                if len(notas) != 0:
                    promedio = cont / len(notas)
                    prome = promedio.__str__()
                    print 'prome semestre materia ' + prome
                    print len(prome)
                    if len(prome) > 3:
                        print 'prome_3 ' + prome[3]
                        if prome[3] == '5':
                            print 'pr semestre ' + prome
                            promedio += 0.05
                else:
                    promedio = 0
                AlumnoMateriaPromedio.objects.filter(alumno=id_nota.alumno, materia=id_nota.evaluacion.materia.id,
                                                     semestre=id_nota.evaluacion.semestre).update(
                    promedio=round(promedio, 1))
                update_prom_anual(id_nota.evaluacion.materia.id, id_nota.alumno.id)

                update_prom_alumno(id_nota.alumno.id)

        return redirect('materias-nota', id_nota.evaluacion.materia.id)
    else:
        if id_nota.evaluacion.materia.nombre == 'Religion' or id_nota.evaluacion.materia.nombre == 'Religión':
            validar_formulario = NotasUpdateReligionForm()
        else:
            validar_formulario = NotasUpdateForm()
    return render_to_response('sanvalentin_app/updateNota.html',
                              {'validar_formulario': validar_formulario, 'nota': id_nota},
                              context_instance=RequestContext(request))


class AlumnoListView(LoginRequired, ListView):
    model = Notas
    context_object_name = 'notas'
    template_name = 'sanvalentin_app/notas_alumno.html'

    def get_queryset(self):
        qs = super(AlumnoListView, self).get_queryset()
        return qs.filter(alumno=self.kwargs['alumno'])


@login_required(login_url='login')
def agregar_materia(request, curso):
    curso = get_object_or_404(Curso, pk=curso)
    if request.method == 'POST':
        formulario_materia = MateriaForm(request.POST)
        if formulario_materia.is_valid():
            nombre = formulario_materia.cleaned_data.get('nombre', None)
            profesor = formulario_materia.cleaned_data.get('profesor', None)

            materia = Materia.objects.create(nombre=nombre, curso=curso, profesor=profesor)
            evaluacion = Evaluacion.objects.create(nombre='Evaluacion 01', materia=materia,
                                                   descripcion='Evaluacion de Prueba',
                                                   fecha=datetime.datetime.now())

            for ac in curso.alumnocurso_set.all():
                AlumnoMateriaPromedio.objects.create(alumno=ac, materia=materia, promedio=0, semestre=1)
                AlumnoMateriaPromedio.objects.create(alumno=ac, materia=materia, promedio=0, semestre=2)
                AlumnoMateriaPromedio.objects.create(alumno=ac, materia=materia, promedio=0, semestre=3)
                Notas.objects.create(alumno=ac, evaluacion=evaluacion, nota=0)

        return redirect('listar-materiascurso', curso.id)
    else:
        formulario_materia = MateriaForm()
    return render_to_response('sanvalentin_app/addmateria.html',
                              {'formulario_materia': formulario_materia, 'curso': curso},
                              context_instance=RequestContext(request))


class InformeUpdate(UpdateView):
    model = InformeDesarrolloPersonal
    form_class = InformePersonalForm
    template_name = 'sanvalentin_app/update_informe.html'

    def get_success_url(self):
        return reverse('informe-alumno', kwargs={'alumno': self.object.alumno.id})


class InformacionListView(LoginRequired, ListView):
    model = Informacion
    context_object_name = 'asistencia'
    template_name = 'sanvalentin_app/asistenciaAlumno.html'

    def get_queryset(self):
        qs = super(InformacionListView, self).get_queryset()
        return qs.filter(alumno=self.kwargs['alumno'])


def promedio(datos, total):
    cont = 0
    for n in datos:
        cont = cont + n
    if total != 0:
        prom = cont / total
        prome = prom.__str__()
        if len(prome) > 3:
            if prome[3] == '5':
                print 'promedio ' + prome
                prom += 0.05
    else:
        prom = 0
    return prom


def update_inasis(info):
    info = get_object_or_404(Informacion, id=info)
    diast = 0
    if info.mes < 8:
        inasistencias = 0

        for i in info.alumno.informacion_set.all():
            if i.mes < 8:
                inasistencias += i.inasistencias

        for d in info.alumno.curso.diastrabajados_set.all():
            if d.mes == 13:
                diast = d.diastrabajados

        porcen_inasistencia = porcentaje(inasistencias, diast)
        Informacion.objects.filter(alumno=info.alumno.id, mes=13).update(inasistencias=inasistencias,
                                                                         asistencia=porcen_inasistencia)

    else:
        inasistencias = 0

        for i in info.alumno.informacion_set.all():
            if 8 <= i.mes < 13:
                inasistencias += i.inasistencias

        for d in info.alumno.curso.diastrabajados_set.all():
            if d.mes == 14:
                diast = d.diastrabajados

        porcen_inasistencia = porcentaje(inasistencias, diast)
        Informacion.objects.filter(alumno=info.alumno.id, mes=14).update(inasistencias=inasistencias,
                                                                         asistencia=porcen_inasistencia)

    inas = 0
    for i in info.alumno.informacion_set.all():
        if i.mes == 13 or i.mes == 14:
            inas += i.inasistencias
    for d in info.alumno.curso.diastrabajados_set.all():
        if d.mes == 15:
            diast = d.diastrabajados
    porcen_inas = porcentaje(inas, diast)
    Informacion.objects.filter(alumno=info.alumno.id, mes=15).update(inasistencias=inas, asistencia=porcen_inas)


def update_atraso(info):
    info = get_object_or_404(Informacion, id=info)
    diast = 0
    if info.mes < 8:
        atrasos = 0

        for i in info.alumno.informacion_set.all():
            if i.mes < 8:
                atrasos += i.atrasos

        for d in info.alumno.curso.diastrabajados_set.all():
            if d.mes == 13:
                diast = d.diastrabajados

        porcen_atraso = porcentaje(atrasos, diast)
        Informacion.objects.filter(alumno=info.alumno.id, mes=13).update(atrasos=atrasos, puntualidad=porcen_atraso)

    else:
        atrasos = 0

        for i in info.alumno.informacion_set.all():
            if 8 <= i.mes < 13:
                atrasos += i.atrasos

        for d in info.alumno.curso.diastrabajados_set.all():
            if d.mes == 14:
                diast = d.diastrabajados

        porcen_atraso = porcentaje(atrasos, diast)
        Informacion.objects.filter(alumno=info.alumno.id, mes=14).update(atrasos=atrasos, puntualidad=porcen_atraso)

    atras = 0
    for i in info.alumno.informacion_set.all():
        if i.mes == 13 or i.mes == 14:
            atras += i.atrasos
    for d in info.alumno.curso.diastrabajados_set.all():
        if d.mes == 15:
            diast = d.diastrabajados
    porcen_atras = porcentaje(atras, diast)
    Informacion.objects.filter(alumno=info.alumno.id, mes=15).update(atrasos=atras, puntualidad=porcen_atras)


@login_required(login_url='login')
def inasistenciaUpdate(request, info):
    info = get_object_or_404(Informacion, id=info)
    if request.method == 'POST':
        inasistencia_formulario = InasistenciaUpdateForm(request.POST)
        if inasistencia_formulario.is_valid():
            inasistencia = inasistencia_formulario.cleaned_data.get('inasistencias', None)

            diast = 0
            for d in info.alumno.curso.diastrabajados_set.all():
                if d.mes == info.mes:
                    diast = d.diastrabajados
            por_inasistencia = porcentaje(inasistencia, diast)

            Informacion.objects.filter(id=info.id).update(inasistencias=inasistencia, asistencia=por_inasistencia)

            update_inasis(info.id)

        return redirect('asistencia-alumno', info.alumno.alumno.id)
    else:
        inasistencia_formulario = InasistenciaUpdateForm()
    return render_to_response('sanvalentin_app/inasistenciaUpdate.html',
                              {'inasistencia_formulario': inasistencia_formulario, 'info': info},
                              context_instance=RequestContext(request))


@login_required(login_url='login')
def atrasoUpdate(request, info):
    info = get_object_or_404(Informacion, id=info)
    if request.method == 'POST':
        validar_formulario = AtrasoUpdateForm(request.POST)
        if validar_formulario.is_valid():
            atraso = validar_formulario.cleaned_data.get('atrasos', None)

            diast = 0
            for d in info.alumno.curso.diastrabajados_set.all():
                if d.mes == info.mes:
                    diast = d.diastrabajados
            por_atraso = porcentaje(atraso, diast)

            Informacion.objects.filter(id=info.id).update(atrasos=atraso, puntualidad=por_atraso)

            update_atraso(info.id)

        return redirect('asistencia-alumno', info.alumno.alumno.id)
    else:
        validar_formulario = AtrasoUpdateForm()
    return render_to_response('sanvalentin_app/atrasoUpdate.html',
                              {'validar_formulario': validar_formulario, 'info': info},
                              context_instance=RequestContext(request))


@login_required(login_url='login')
def agregar_directiva(request):
    if request.method == 'POST':
        formulario_directiva = DirectivaForm(request.POST)
        if formulario_directiva.is_valid():
            formulario_directiva.save()
            return HttpResponseRedirect('/direccion')
    else:
        formulario_directiva = DirectivaForm()
    return render_to_response('sanvalentin_app/adddirectiva.html', {'formulario_directiva': formulario_directiva},
                              context_instance=RequestContext(request))


class DeleteDirectivaView(DeleteView):
    model = Directiva
    template_name = 'sanvalentin_app/directivadelete.html'

    def get_success_url(self):
        return reverse('direccion')


@login_required(login_url='login')
def directiva_update(request, dire):
    dire = get_object_or_404(Directiva, id=dire)
    if request.method == 'POST':
        validar_formulario = DirectivaUpdateForm(request.POST)
        if validar_formulario.is_valid():
            funcionario = validar_formulario.cleaned_data.get('funcionario', None)
            cargo = validar_formulario.cleaned_data.get('cargo', None)

            Directiva.objects.filter(id=dire.id).update(funcionario=funcionario, cargo=cargo)

        return HttpResponseRedirect('/direccion')
    else:
        validar_formulario = DirectivaUpdateForm()
    return render_to_response('sanvalentin_app/directivaupdate.html',
                              {'validar_formulario': validar_formulario, 'dire': dire},
                              context_instance=RequestContext(request))


class HelloPDFView(PDFTemplateView):
    model = Notas
    template_name = "sanvalentin_app/alumno_notas_pdf.html"

    def get_context_data(self, alumno, **kwargs):
        context = super(HelloPDFView, self).get_context_data(
            pagesize="A4",
            title="Hi there!",
            **kwargs
        )
        alumno = get_object_or_404(AlumnoCurso, id=alumno)
        context['notas'] = Notas.objects.filter(alumno=alumno)
        context['promedio'] = PromedioAlumno.objects.filter(alumno=alumno)
        context['asistencia'] = Informacion.objects.filter(alumno=alumno)
        return context


class AlumnosMatriculadosListView(LoginRequired, ListView):
    model = Alumno
    context_object_name = 'alumnos'
    template_name = 'sanvalentin_app/alumnos_matriculados.html'

    def get_queryset(self):
        qs = super(AlumnosMatriculadosListView, self).get_queryset()
        name = self.request.GET.get('name', None)
        if name:
            qs = qs.filter(nombres__icontains=name)
        return qs


class AlumnosMatriculados(PDFTemplateView):
    model = Alumno
    template_name = "sanvalentin_app/pdf_alumnos_matriculados.html"

    def get_context_data(self, **kwargs):
        context = super(AlumnosMatriculados, self).get_context_data(
            pagesize="A4",
            title="Hi there!",
            **kwargs
        )
        context['alumnos'] = Alumno.objects.all()
        return context


class AlumnoDetailView(LoginRequired, DetailView):
    model = Alumno
    template_name = 'sanvalentin_app/alumnos_detalle.html'

    def get_context_data(self, **kwargs):
        context = super(AlumnoDetailView, self).get_context_data(**kwargs)
        return context


@login_required(login_url='login')
def dias_trabajados_update(request, dt):
    dt = get_object_or_404(DiasTrabajados, id=dt)
    if request.method == 'POST':
        validar_formulario = DiasTrabajadosUpdateForm(request.POST)
        if validar_formulario.is_valid():
            diastrabajados = validar_formulario.cleaned_data.get('diastrabajados', None)

            DiasTrabajados.objects.filter(id=dt.id).update(diastrabajados=diastrabajados)

            dtp = 0
            for i in dt.curso.diastrabajados_set.all():
                if i.mes < 8:
                    dtp += i.diastrabajados
            DiasTrabajados.objects.filter(curso=dt.curso.id, mes=13).update(diastrabajados=dtp)

            dts = 0
            for i in dt.curso.diastrabajados_set.all():
                if 8 <= i.mes < 13:
                    dts += i.diastrabajados
            DiasTrabajados.objects.filter(curso=dt.curso.id, mes=14).update(diastrabajados=dts)

            dta = dtp + dts
            DiasTrabajados.objects.filter(curso=dt.curso.id, mes=15).update(diastrabajados=dta)

            for ac in dt.curso.alumnocurso_set.all():
                for i in ac.informacion_set.all():
                    if i.mes == dt.mes:
                        por_a = porcentaje(i.atrasos, diastrabajados)
                        por_i = porcentaje(i.inasistencias, diastrabajados)
                        Informacion.objects.filter(id=i.id).update(puntualidad=por_a, asistencia=por_i)

                        update_atraso(i.id)
                        update_inasis(i.id)

        return redirect('dias-trabajados', dt.curso.id)
    else:
        validar_formulario = DiasTrabajadosUpdateForm()
    return render_to_response('sanvalentin_app/diasTrabajados_update.html',
                              {'validar_formulario': validar_formulario, 'dt': dt},
                              context_instance=RequestContext(request))


@login_required(login_url='login')
def dias_trabajados(request, curso):
    curso = get_object_or_404(Curso, id=curso)
    context = {}
    diast = []
    for d in curso.diastrabajados_set.all():
        diast.append(d)
    context['diast'] = diast
    context['cursos'] = Curso.objects.all()
    name = request.GET.get('name', None)
    if name:
        context['cursos'] = Curso.objects.filter(nombre__icontains=name)
    return render(request, 'sanvalentin_app/dias_trabajados.html', context)


class DeleteCursoView(DeleteView):
    model = Curso
    template_name = 'sanvalentin_app/curso_confirm_delete.html'

    def get_success_url(self):
        return reverse('listar-cursos')


class DeleteProfesorView(DeleteView):
    model = Profesor
    template_name = 'sanvalentin_app/profesor_confirm_delete.html'

    def get_success_url(self):
        return reverse('listar-profesores')


class DeleteMateriaView(DeleteView):
    model = Materia
    template_name = 'sanvalentin_app/materia_confirm_delete.html'

    def get_success_url(self):
        return reverse('listar-cursos')


class DeleteAlumnoView(DeleteView):
    model = Alumno
    template_name = 'sanvalentin_app/alumno_confirm_delete.html'

    def get_success_url(self):
        return reverse('alumnos-matriculados')


class AlumnoUpdate(UpdateView):
    model = Alumno
    form_class = AlumnoForm
    template_name = 'sanvalentin_app/update_alumno.html'

    def get_success_url(self):
        return reverse('alumno-detalle', kwargs={'pk': self.object.id})


class ApoderadoUpdate(UpdateView):
    model = Apoderado
    form_class = ApoderadoForm
    template_name = 'sanvalentin_app/update_apoderado.html'

    def get_success_url(self):
        return reverse('alumno-detalle', kwargs={'pk': self.object.alumno.id})


class IDPPDF(PDFTemplateView):
    model = InformeDesarrolloPersonal
    template_name = "sanvalentin_app/pdf_IDP.html"

    def get_context_data(self, alumno, **kwargs):
        context = super(IDPPDF, self).get_context_data(
            pagesize="A4",
            title="Hi there!",
            **kwargs
        )
        context['fecha'] = datetime.datetime.now()
        context['items'] = InformeDesarrolloPersonal.objects.filter(alumno=alumno)
        return context


class IDPPDF1(PDFTemplateView):
    model = InformeDesarrolloPersonal
    template_name = "sanvalentin_app/pdf_IDP1.html"

    def get_context_data(self, alumno, **kwargs):
        context = super(IDPPDF1, self).get_context_data(
            pagesize="A4",
            title="Hi there!",
            **kwargs
        )
        context['fecha'] = datetime.datetime.now()
        context['items'] = InformeDesarrolloPersonal.objects.filter(alumno=alumno)
        return context


class IDPPDF2(PDFTemplateView):
    model = InformeDesarrolloPersonal
    template_name = "sanvalentin_app/pdf_IDP2.html"

    def get_context_data(self, alumno, **kwargs):
        context = super(IDPPDF2, self).get_context_data(
            pagesize="A4",
            title="Hi there!",
            **kwargs
        )
        context['fecha'] = datetime.datetime.now()
        context['items'] = InformeDesarrolloPersonal.objects.filter(alumno=alumno)
        return context


@login_required(login_url='login')
def nueva_observacion(request, alumno):
    alumno = get_object_or_404(AlumnoCurso, pk=alumno)
    if request.method == 'POST':
        formulario_observacion = ObservacionesAlumnoForm(request.POST)
        if formulario_observacion.is_valid():
            semestre = formulario_observacion.cleaned_data.get('semestre', None)
            observacion = formulario_observacion.cleaned_data.get('observacion', None)

            ObservacionesAlumno.objects.create(alumno=alumno, semestre=semestre, observacion=observacion)

            return redirect('notas-alumno', alumno.id)
    else:
        formulario_observacion = ObservacionesAlumnoForm()
    return render_to_response('sanvalentin_app/addobservacion.html',
                              {'formulario_observacion': formulario_observacion, 'alumno': alumno},
                              context_instance=RequestContext(request))


class DetalleNotaUpdate(UpdateView):
    model = Evaluacion
    form_class = EvaluacionForm
    template_name = 'sanvalentin_app/update_evaluacion.html'

    def get_success_url(self):
        return reverse('materias-nota', kwargs={'materia': self.object.materia.id})


@login_required(login_url='login')
def deleteevaluacion(request, eva):
    eva = get_object_or_404(Evaluacion, id=eva)

    if request.method == 'POST':
        deleteva_formulario = DeleteEvaForm(request.POST)
        if deleteva_formulario.is_valid():
            materia = eva.materia
            Evaluacion.objects.filter(id=eva.id).delete()
            update_promedio_semestre(materia.id, eva.semestre)

            return redirect('materias-nota', materia.id)
    else:
        deleteva_formulario = DeleteEvaForm()
    return render_to_response('sanvalentin_app/evaluacion_confirm_delete.html',
                              {'deleteva_formulario': deleteva_formulario, 'eva': eva},
                              context_instance=RequestContext(request))


@login_required(login_url='login')
def promoveralumno(request, alumno):
    alumno = get_object_or_404(Alumno, id=alumno)
    if request.method == 'POST':
        promover_formulario = PromoverForm(request.POST)
        if promover_formulario.is_valid():
            curso = promover_formulario.cleaned_data.get('curso', None)

            alumnocurso = AlumnoCurso.objects.create(curso=curso, alumno=alumno)

            dp = DesarrolloPersonal.objects.all()
            for x in dp:
                InformeDesarrolloPersonal.objects.create(alumno=alumnocurso, item=x)
                InformeDesarrolloPersonal.objects.create(alumno=alumnocurso, item=x, semestre=2)

            for m in curso.materia_set.all():
                for e in m.evaluacion_set.all():
                    Notas.objects.create(alumno=alumnocurso, evaluacion=e, nota=0)
                AlumnoMateriaPromedio.objects.create(alumno=alumnocurso, materia=m, promedio=0, semestre=1)
                AlumnoMateriaPromedio.objects.create(alumno=alumnocurso, materia=m, promedio=0, semestre=2)
                AlumnoMateriaPromedio.objects.create(alumno=alumnocurso, materia=m, promedio=0, semestre=3)

            PromedioAlumno.objects.create(alumno=alumnocurso, mes=1, promedio=0, promedio_neto=0)
            PromedioAlumno.objects.create(alumno=alumnocurso, mes=2, promedio=0, promedio_neto=0)
            PromedioAlumno.objects.create(alumno=alumnocurso, mes=3, promedio=0, promedio_neto=0)

            meses = ['3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
            for mes in meses:
                Informacion.objects.create(alumno=alumnocurso, mes=mes, inasistencias=0, atrasos=0, asistencia=100,
                                           puntualidad=100)

            return redirect('listar-cursoalumno', curso.id)
    else:
        promover_formulario = PromoverForm()
    return render_to_response('sanvalentin_app/promover.html',
                              {'promover_formulario': promover_formulario, 'alumno': alumno},
                              context_instance=RequestContext(request))


@login_required(login_url='login')
def asignarcurso(request, alumno):
    alumno = get_object_or_404(Alumno, id=alumno)
    if request.method == 'POST':
        asignarcurso_formulario = AsignarForm(request.POST)
        if asignarcurso_formulario.is_valid():
            curso = asignarcurso_formulario.cleaned_data.get('curso', None)
            alumnocurso = AlumnoCurso.objects.create(curso=curso, alumno=alumno)
            dp = DesarrolloPersonal.objects.all()
            for x in dp:
                InformeDesarrolloPersonal.objects.create(alumno=alumnocurso, item=x)
                InformeDesarrolloPersonal.objects.create(alumno=alumnocurso, item=x, semestre=2)
        return redirect('listar-cursoalumno', curso.id)
    else:
        asignarcurso_formulario = AsignarForm()
    return render_to_response('sanvalentin_app/asignar_curso.html',
                              {'asignarcurso_formulario': asignarcurso_formulario, 'alumno': alumno},
                              context_instance=RequestContext(request))


class NMatriculaUpdate(UpdateView):
    model = Alumno
    form_class = MatriculaForm
    template_name = 'sanvalentin_app/update_matricula.html'

    def get_success_url(self):
        return reverse('alumnos-matriculados')


def passwordUpdate(request, id_user):
    user = get_object_or_404(User, pk=id_user)
    if request.method == 'POST':
        password = UsserForm(request.POST)
        if password.is_valid():
            new_password = password.cleaned_data.get('password', None)
            u = User.objects.get(username=user.username)
            u.set_password(new_password)
            u.save()
        return HttpResponseRedirect('/home')
    else:
        password = UsserForm()
    return render_to_response('sanvalentin_app/update_user.html', {'password': password, 'user': user},
                              context_instance=RequestContext(request))


class MateriaUpdate(UpdateView):
    model = Materia
    form_class = MateriaUpForm
    template_name = 'sanvalentin_app/update_materia.html'

    def get_success_url(self):
        return reverse('listar-materiascurso', kwargs={'pk': self.object.curso.id})


class CursoUpdate(UpdateView):
    model = Curso
    form_class = CursoUpForm
    template_name = 'sanvalentin_app/update_curso.html'

    def get_success_url(self):
        return reverse('detalle-curso', kwargs={'pk': self.object.id})


def CrearInformePersonalidad(request):
    if request.method == 'POST':
        IP_formulario = Info_PerForm(request.POST)
        if IP_formulario.is_valid():
            IP_formulario.save()

        return HttpResponseRedirect('/home')
    else:
        IP_formulario = Info_PerForm()
    return render_to_response('sanvalentin_app/crear_ip.html', {'IP_formulario': IP_formulario},
                              context_instance=RequestContext(request))


class IPDireccionListView(LoginRequired, ListView):
    model = DesarrolloPersonal
    context_object_name = 'items'
    template_name = 'sanvalentin_app/informe_personal_dir.html'


class ItemIPUpdate(UpdateView):
    model = DesarrolloPersonal
    context_object_name = 'items'
    template_name = 'sanvalentin_app/updateitemip.html'

    def get_success_url(self):
        return reverse('informe-personalidad')


class FichaPDF(PDFTemplateView):
    model = Alumno
    template_name = "sanvalentin_app/pdf_ficha.html"

    def get_context_data(self, alumno, **kwargs):
        context = super(FichaPDF, self).get_context_data(
            pagesize="A4",
            title="Hi there!",
            **kwargs
        )
        context['alumno'] = get_object_or_404(Alumno, id=alumno)
        context['apoderado'] = Apoderado.objects.filter(alumno=alumno)
        context['antecedentes'] = AntecedentesAlumno.objects.filter(alumno=alumno)
        return context


class ObservacionUpdate(UpdateView):
    model = ObservacionesAlumno
    form_class = ObservacionesAlumnoForm
    template_name = 'sanvalentin_app/update_observacion.html'

    def get_success_url(self):
        return reverse('notas-alumno', kwargs={'alumno': self.object.alumno.id})


class AnteFamUpdate(UpdateView):
    model = AntecedentesAlumno
    form_class = AntecedentesForm
    template_name = 'sanvalentin_app/update_antefam.html'

    def get_success_url(self):
        return reverse('alumno-detalle', kwargs={'pk': self.object.alumno.id})


class AnteSocioUpdate(UpdateView):
    model = AntecedentesAlumno
    form_class = AntecedentesEconomicosForm
    template_name = 'sanvalentin_app/update_antesoci.html'

    def get_success_url(self):
        return reverse('alumno-detalle', kwargs={'pk': self.object.alumno.id})


class SaludUpdate(UpdateView):
    model = AntecedentesAlumno
    form_class = AntecedentesSaludForm
    template_name = 'sanvalentin_app/update_salud.html'

    def get_success_url(self):
        return reverse('alumno-detalle', kwargs={'pk': self.object.alumno.id})


class PromediosAlumnos(LoginRequired, DetailView):
    model = Curso
    context_object_name = 'curso'
    template_name = 'sanvalentin_app/prom_curso.html'

    def get_context_data(self, **kwargs):
        context = super(PromediosAlumnos, self).get_context_data(**kwargs)
        return context


class PromediosAlumnosPDF(PDFTemplateView):
    model = Curso
    template_name = "sanvalentin_app/pdf_promedios_alumnos.html"

    def get_context_data(self, curso, **kwargs):
        context = super(PromediosAlumnosPDF, self).get_context_data(
            pagesize="A4",
            title="Hi there!",
            **kwargs
        )
        context['curso'] = get_object_or_404(Curso, id=curso)
        return context

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def descargar_backup(request):
    file_name = "Hola.sql"
    path_backup = os.path.join(BASE_DIR, file_name)
    f = open(path_backup, 'rb')
    response = HttpResponse(f, content_type='application/text/plain')
    response['Content-Disposition'] = "attachment; filename={}".format(file_name)
    return response