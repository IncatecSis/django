from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from django.views.decorators.cache import cache_control
from datetime import datetime
from django.contrib import messages 
from src.models import *




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if request.method == 'POST':
        documento = request.POST.get('username')
        password = request.POST.get('password')

        try:
            usuario = Usuario.objects.get(documento_identidad=documento)

            if not usuario.estado:
                messages.error(request, 'Usuario inactivo.')
                return redirect('login')
            
            if check_password(password, usuario.password):
                request.session['usuario_id'] = usuario.id_usuario
                request.session['usuario_nombre'] = usuario.nombre
                request.session['is_authenticated'] = True

                messages.success(request, f'Bienvenido {usuario.nombre}')
                return redirect('sistema:dasbohard')
            else:
                messages.error(request, 'Contraseña incorrecta.')

        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario no encontrado.')

    return render(request, 'login/login.html', {
        'titulo': 'Login',
    })


def logout(request):
    request.session.flush()
    return redirect('login')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dasbohard(request):
    if not request.session.get('is_authenticated'):
        return redirect('login')
    
    if request.method == 'POST':
        id_detenido = request.POST.get('id_detenido')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        numero_documento = request.POST.get('documento')
        ingreso = request.POST.get('fecha_ingreso')
        salida = request.POST.get('fecha_salida')
        historial = request.POST.get('historial')

        fecha_ingreso = (
            datetime.strptime(ingreso, "%Y-%m-%dT%H:%M")
            if ingreso else None
        )

        fecha_salida = (
            datetime.strptime(salida, "%Y-%m-%dT%H:%M")
            if salida else None
        )

        if id_detenido:
            detenido = get_object_or_404(Detenido, id_detenido=id_detenido)
            detenido.nombre = nombre
            detenido.apellido = apellido
            detenido.documento_identidad = numero_documento
            detenido.fecha_ingreso = fecha_ingreso
            detenido.fecha_salida = fecha_salida
            detenido.historial = historial
            detenido.save()
            messages.success(request, 'Detenido actualizado correctamente.')
        else:
            Detenido.objects.create(
                nombre=nombre,
                apellido=apellido,
                documento_identidad=numero_documento,
                fecha_salida=fecha_salida,
                fecha_ingreso=fecha_ingreso,
                historial=historial,
            )
            messages.success(request, 'Detenido creado correctamente.')

    detenidos = Detenido.objects.all()
    incidentes = Incidente.objects.count()
    incidentes_recientes = Incidente.objects.select_related('id_detenido').order_by('-fecha')[:5]


    return render(request, 'index/dasbohard.html', {
        'titulo': 'Dasbohard',
        'detenidos': detenidos,
        'incidentes': incidentes,
        'incidentes_recientes': incidentes_recientes,
    })

