from django.contrib import admin
from .models import UserAgentModel, UserCustomerModel

class UserAgentModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'phone')  
    search_fields = ('user__username', 'nickname', 'phone')  

admin.site.register(UserAgentModel, UserAgentModelAdmin)

class UserCustomerModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'owner')  
    search_fields = ('user__username', 'phone')  
    list_filter = ('owner',)  

admin.site.register(UserCustomerModel, UserCustomerModelAdmin)