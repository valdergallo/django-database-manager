from django.contrib import admin
from .models import Backup


class BackupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status", "database", "server")

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()


admin.site.register(Backup, BackupAdmin)