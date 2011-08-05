from django.contrib import admin
from cbir.models import Year, Lawmaker, Earmark

class LawmakerAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    

admin.site.register(Year)
admin.site.register(Lawmaker, LawmakerAdmin)
admin.site.register(Earmark)