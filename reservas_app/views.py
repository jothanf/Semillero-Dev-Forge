from django.shortcuts import render

# Create your views here.
def reservas_home(request):
    return render(request, 'reservas_home.html')