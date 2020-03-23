from django.contrib import admin

# Register your models here.

from .models import Poll, Choice, Vote



class ChoiceInline(admin.TabularInline):
    model = Choice
    
class PollAdmin(admin.ModelAdmin):
    inlines = [
        ChoiceInline,
    ]
    list_display = ['question', 'created_by']
    list_editable = []

admin.site.register(Poll, PollAdmin)

admin.site.site_header = "Администрирование сайта Опросы"

