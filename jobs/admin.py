from django.contrib import admin
from jobs.models import Backup, Restore


class BackupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status", "database", "server")
    list_display_links = ("id", "name")

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()


class RestoreAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "database", "server", "backup")
    list_display_links = ("id", "backup", "server")

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()


admin.site.register(Backup, BackupAdmin)
admin.site.register(Restore, RestoreAdmin)
