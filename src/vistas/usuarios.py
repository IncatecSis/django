from django.shortcuts import render, redirect,get_object_or_404
from datetime import datetime
from django.contrib import messages
from src.models import *



def Usuarios(request):
    if request.method == 'POST':
        id_usuario = request.POST.get('id_usuario')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        documento = request.POST.get('numero_documento')
        correo = request.POST.get('correo')
        contraseña = request.POST.get('password')
        id_rol = request.POST.get('rol')

        if id_usuario:
            usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
            usuario.nombre = nombre
            usuario.apellido = apellido
            usuario.documento_identidad = documento
            usuario.correo = correo
            usuario.password = contraseña
            usuario.id_rol = get_object_or_404(Rol, id_rol=id_rol)
            usuario.save()
            messages.success(request, 'Usuario actualizado correctamente.')
        else:
            Usuario.objects.create(
                nombre=nombre,
                apellido=apellido,
                documento_identidad=documento,
                correo=correo,
                password=contraseña,
                id_rol=get_object_or_404(Rol, id_rol=id_rol)
            )
            messages.success(request, 'Usuario creado correctamente.')

    usuario = Usuario.objects.all()
    roles = Rol.objects.all()

    return render(request, 'plantillas/usuarios.html',{
        'titulo': 'Usuarios',
        'usuarios': usuario,
        'roles': roles,
    })



def incidentes(request):
    if request.method == 'POST':
        id_incidente = request.POST.get('id_incidente')
        descripcion = request.POST.get('descripcion')
        inicio = request.POST.get('fecha')
        id_guardia = request.POST.get('guardia')
        id_detenido = request.POST.get('detenido')

        fecha = (
            datetime.strptime(inicio, "%Y-%m-%dT%H:%M")
            if inicio else None
        )
        if id_incidente:
            incidente = get_object_or_404(Incidente, id_incidente=id_incidente)
            incidente.descripcion = descripcion
            incidente.fecha = fecha
            incidente.id_guardia = get_object_or_404(Guardiaseguridad, id_guardia=id_guardia)
            incidente.id_detenido = get_object_or_404(Detenido, id_detenido=id_detenido)
            incidente.save()
            messages.success(request, 'Incidente actualizado correctamente.')
        else:
            Incidente.objects.create(
                descripcion=descripcion,
                fecha=fecha,
                id_guardia= get_object_or_404(Guardiaseguridad, id_guardia=id_guardia),
                id_detenido = get_object_or_404(Detenido, id_detenido=id_detenido),
            )
            messages.success(request, 'Incidente creado correctamente.')

    detenidos = Detenido.objects.filter(estado=True)
    guardias = Guardiaseguridad.objects.all()
    incidentes = Incidente.objects.select_related('id_guardia', 'id_detenido').order_by('-fecha')

    return render(request, 'plantillas/incidentes.html',{
        'titulo': 'Incidentes',
        'detenidos': detenidos,
        'guardias': guardias,
        'incidentes': incidentes,
    })