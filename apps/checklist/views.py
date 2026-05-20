from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .models import FaseChecklist, ItemChecklist, RegistroChecklist
from apps.predios.models import Predio

@login_required
def checklist_predio(request, predio_pk):
    predio = get_object_or_404(Predio, pk=predio_pk, usuarios=request.user)
    fases = FaseChecklist.objects.prefetch_related('items').all()
    registros = {r.item_id: r for r in RegistroChecklist.objects.filter(predio=predio)}

    for fase in fases:
        for item in fase.items.all():
            item.registro = registros.get(item.pk)

    return render(request, 'checklist/checklist.html', {
        'predio': predio,
        'fases': fases,
        'porcentaje': predio.porcentaje_cumplimiento(),
    })

@login_required
@require_POST
def actualizar_item(request, predio_pk, item_pk):
    predio = get_object_or_404(Predio, pk=predio_pk, usuarios=request.user)
    item = get_object_or_404(ItemChecklist, pk=item_pk)
    data = json.loads(request.body)
    RegistroChecklist.objects.update_or_create(
        predio=predio,
        item=item,
        defaults={
            'estado': data.get('estado', 'pendiente'),
            'observacion': data.get('observacion', ''),
            'usuario': request.user,
        }
    )
    return JsonResponse({
        'ok': True,
        'porcentaje': predio.porcentaje_cumplimiento(),
        'nivel_riesgo': predio.nivel_riesgo(),
    })