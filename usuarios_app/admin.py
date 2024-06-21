from django.contrib import admin
from .models import UsuarioModel

# Register your models here.

@admin.register(UsuarioModel)
class UsuarioModelAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'direccion')
    search_fields = ('nombre', 'telefono')