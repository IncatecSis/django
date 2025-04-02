from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from src.models import *



def parametros(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo')

        if tipo == 'roles':
            id_rol = request.POST.get('id_rol')
            nombre = request.POST.get('nombre')

            if id_rol:
                rol = get_object_or_404(Rol, id_rol=id_rol)
                rol.nombre = nombre
                rol.save()
                messages.success(request, 'Rol actualizado correctamente.')
            else:
                Rol.objects.create(
                    nombre=nombre
                )
                messages.success(request, 'Rol creado correctamente.')

    return render(request, 'plantillas/parametros.html', {
        'titulo': 'Parámetros',
        'roles': Rol.objects.all()
    })