from django.conf.urls import url
from registro import views

app_name = 'registro'

urlpatterns = [
    url(
        r'^$',
        views.HomeTemplateView.as_view(),
        name='home'
    )
]
