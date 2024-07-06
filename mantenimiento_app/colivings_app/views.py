from django.shortcuts import render, redirect

# Create your views here.
def colivings_home(request):
    return render(request, 'colivings_home.html')

from .models import ColivingModel
from django.utils.timezone import now

def registrar_coliving(request):
    if request.method == 'POST':
        # Process the form submission
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        ciudad = request.POST.get('ciudad')
        estado = request.POST.get('estado')
        pais = request.POST.get('pais')
        descripcion = request.POST.get('descripcion')
        servicios = request.POST.getlist('servicios')  # Assuming servicios is a list in the form
        foto_perfil = request.FILES.get('foto_perfil')  # Handle the file upload

        # Assuming you're using Django's built-in user authentication
        propietario = request.user
        
        # Create the ColivingModel instance
        coliving = ColivingModel.objects.create(
            nombre=nombre,
            direccion=direccion,
            ciudad=ciudad,
            estado=estado,
            pais=pais,
            descripcion=descripcion,
            servicios=servicios,
            foto_perfil=foto_perfil,
            propietario=propietario,
            creado_en=now(),
            actualizado_en=now()
        )
        
        # Redirect to a success URL
        return redirect('colivings_home')  # Replace 'success_url' with your desired redirect URL
    
    # If it's a GET request, render the form
    return render(request, 'coliving_app/registrar_coliving.html')