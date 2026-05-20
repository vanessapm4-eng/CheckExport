from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Predio, UsuarioPredio

def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')

@login_required
def dashboard(request):
    predios = request.user.predios.all()
    context = {
        'predios': predios,
        'total_predios': predios.count(),
        'habilitados': predios.filter(estado_habilitacion='habilitado').count(),
        'alertas_activas': sum(p.alertas_activas() for p in predios),
    }
    return render(request, 'dashboard.html', context)

@login_required
def crear_predio(request):
    if request.method == 'POST':
        predio = Predio.objects.create(
            nombre=request.POST.get('nombre'),
            registro_ica=request.POST.get('registro_ica'),
            municipio=request.POST.get('municipio'),
            departamento=request.POST.get('departamento'),
            vereda=request.POST.get('vereda', ''),
            estado_habilitacion=request.POST.get('estado_habilitacion'),
        )
        UsuarioPredio.objects.create(usuario=request.user, predio=predio, rol='admin')
        messages.success(request, f'Predio "{predio.nombre}" creado exitosamente.')
        return redirect('dashboard')
    return render(request, 'predios/form.html')