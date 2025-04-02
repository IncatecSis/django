from django.shortcuts import redirect,render, get_object_or_404
from django.contrib import messages
from src.models import *



def p_medico(request):
    if request.method == 'POST':
        id_medico = request.POST.get('id_medico')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        especialidad = request.POST.get('especialidad')

        if id_medico:
            medico = get_object_or_404(Personalmedico, id_medico=id_medico)
            medico.nombre = nombre
            medico.apellido = apellido
            medico.especialidad = especialidad
            medico.save()
            messages.success(request, 'Personal médico actualizado correctamente.')
        else:
            Personalmedico.objects.create(
                nombre=nombre,
                apellido=apellido,
                especialidad=especialidad
            )
            messages.success(request, 'Personal médico creado correctamente.')

    medicos = Personalmedico.objects.all()
    return render(request, 'plantillas/medico.html',{
        'titulo': 'Personal Médico',
        'medicos': medicos,
    })