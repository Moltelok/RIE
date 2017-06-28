# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from registro import models


class MateriaInline(admin.TabularInline):
    model = models.Materia
    extra = 1


@admin.register(models.Curso)
class CursoAdmin(admin.ModelAdmin):
    inlines = [
        MateriaInline
    ]
    search_fields = ['nombre']
    list_filter = [
        'nombre',
        'profesor_jefe'
    ]
    list_display = (
        'nombre',
        'profesor_jefe'
    )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
