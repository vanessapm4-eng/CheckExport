from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario

def logout_view(request):
    logout(request)
    return redirect('/')

def registro_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('first_name')
        apellido = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'usuarios/registro.html')

        if Usuario.objects.filter(username=username).exists():
            messages.error(request, 'Ese nombre de usuario ya está en uso.')
            return render(request, 'usuarios/registro.html')

        usuario = Usuario.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=nombre,
            last_name=apellido,
            rol='productor'
        )
        login(request, usuario)
        messages.success(request, f'Bienvenido/a, {nombre}. Tu cuenta fue creada exitosamente.')
        return redirect('/dashboard/')

    return render(request, 'usuarios/registro.html')