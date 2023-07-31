from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.
# admin.site.register(User)
@admin.register(User)
class MyUserAdmin(UserAdmin):
    model = User
    list_display = ('id','username','phone_number', 
                    'email','first_name','last_name','password')
    list_filter = ('phone_number',
                    'email')
    search_fields = ('username',) 
    ordering = ('id','username',)  
    filter_horizontal = ()
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('phone_number',)}),
    )

admin.site.register(Topic)
admin.site.register(Room)
admin.site.register(Message)