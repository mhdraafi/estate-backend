from django.contrib import admin
from .models import Property, ContactMessage, Register


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type', 'price')
    list_filter = ('type',)
    search_fields = ('title', 'location')


@admin.register(ContactMessage)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')


@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ('fname', 'email', 'mobile')
