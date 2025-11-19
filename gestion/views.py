from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from .models import Tarea
from .forms import TareaForm

# READ (Lista)
def lista_tareas(request):
    tareas = Tarea.objects.all().order_by('-fecha_creacion')
    
    # Calcular estadísticas
    total_tareas = tareas.count()
    pendientes = tareas.filter(estado='Pendiente').count()
    en_progreso = tareas.filter(estado='En Progreso').count()
    en_revision = tareas.filter(estado='En Revisión').count()
    completadas = tareas.filter(estado='Finalizada').count()
    
    contexto = {
        'tareas': tareas,
        'total_tareas': total_tareas,
        'pendientes': pendientes,
        'en_progreso': en_progreso,
        'en_revision': en_revision,
        'completadas': completadas,
    }
    return render(request, 'gestion/lista_tareas.html', contexto)

# READ (Detalle)
def detalle_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, pk=tarea_id)
    contexto = {'tarea': tarea}
    return render(request, 'gestion/detalle_tarea.html', contexto)

# CREATE
def crear_tarea(request):
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_tareas')
    else:
        form = TareaForm()
    
    contexto = {'form': form}
    return render(request, 'gestion/tarea_form.html', contexto)

# UPDATE
def editar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, pk=tarea_id)
    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return redirect('detalle_tarea', tarea_id=tarea.id)
    else:
        form = TareaForm(instance=tarea)
    
    contexto = {'form': form}
    return render(request, 'gestion/tarea_form.html', contexto)

# DELETE
def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, pk=tarea_id)
    if request.method == 'POST':
        tarea.delete()
        return redirect('lista_tareas')
    
    contexto = {'tarea': tarea}
    return render(request, 'gestion/tarea_confirm_delete.html', contexto)