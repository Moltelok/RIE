# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView

# Create your views here.


class HomeTemplateView(TemplateView):
    """
        Vista de Inicio
    """
    template_name = 'registro/base/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeTemplateView, self).get_context_data(**kwargs)
        return context