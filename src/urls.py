from django.urls import path
from src.vistas.login import *
from src.vistas.usuarios import *
from src.vistas.p_medico import *
from src.vistas.parametros import *


urlpatterns = [
    path('dasbohard/', dasbohard, name='dasbohard'),
    path('usuarios/', Usuarios, name='usuarios'),
    path('incidentes/', incidentes, name='incidentes'),
    path('medicos/', p_medico, name='medicos'),
    path('parametros/', parametros, name='parametros'),
]