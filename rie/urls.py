from django.conf.urls import url, include
from django.contrib import admin
from rie import views

urlpatterns = [
    url(
        r'^admin/',
        admin.site.urls
    ),
    url(
        r'^login/',
        views.login_view,
        name='login',
    ),
    url(
        r'^logout/$',
        views.logout_view,
        name='logout',
    ),
    url(
        r'^',
        include('registro.urls')
    ),
]
