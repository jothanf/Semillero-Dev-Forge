from django.shortcuts import render

# Create your views here.
def mantenimiento_home(request):
    return render(request, 'mantenimiento_home.html')