from django.contrib import admin
from .models import PropertyModel

class PropertyModelAdmin(admin.ModelAdmin):
    list_display = ('owner', 'address', 'price', 'area')  
    search_fields = ('address', 'owner__user__username')  
    list_filter = ('owner',)  

admin.site.register(PropertyModel, PropertyModelAdmin)