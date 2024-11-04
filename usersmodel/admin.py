from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser
from django.utils.translation import gettext as _
class CustomUserAdmin(BaseUserAdmin):
 
    list_display = ('email', 'name', 'surname', 'is_staff', 'is_active', 'telegram_id', 'country', 'city', 'phone')
    list_filter = ('is_staff', 'is_active', 'country', 'city')  
    search_fields = ('email', 'name', 'surname', 'telegram_id', 'phone')  
    ordering = ('email',)  
    

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name', 'surname', 'photo', 'telegram_id', 'country', 'city', 'address', 'phone')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'surname', 'photo', 'telegram_id', 'country', 'city', 'address', 'phone', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions',)  # Для удобства редактирования групп и прав пользователя

admin.site.register(CustomUser, CustomUserAdmin)
