from django.shortcuts import render,  get_object_or_404
from .models import UsuarioModel

# Create your views here.
def home(request):
    if request.method == 'POST':
        try:
            nombre_usuario = request.POST.get('nombre_usuario')

            # Verifica si se recibió un nombre de usuario válido
            if nombre_usuario:
                nuevo_usuario = UsuarioModel(nombre=nombre_usuario)
                nuevo_usuario.save()

                mensaje = f'El usuario {nombre_usuario} se registró satisfactoriamente.'
            else:
                mensaje = 'Debe ingresar un nombre de usuario válido.'
            
            return render(request, 'home.html', {'mensaje': mensaje})
        
        except Exception as e:
            print(f"Error al guardar el usuario: {e}")
            mensaje = 'Error al guardar el usuario. Inténtelo nuevamente.'
            return render(request, 'home.html', {'mensaje': mensaje})

    return render(request, 'home.html')

def signin(request):
    mensaje = ""
    usuarios = []
    if request.method == 'POST':
        nombre_usuario = request.POST.get('nombre')
        usuarios = UsuarioModel.objects.filter(nombre=nombre_usuario)
        if usuarios.exists():
            mensaje = f"El usuario {nombre_usuario} ya está registrado."
        else:
            mensaje = f"El usuario {nombre_usuario} no está registrado."
    
    return render(request, 'signin.html', {'mensaje': mensaje, 'usuarios': usuarios})

def user_detail(request, user_id):
    usuario = get_object_or_404(UsuarioModel, id=user_id)
    return render(request, 'detalles_usuario.html', {'usuario': usuario})