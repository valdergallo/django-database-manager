from django.contrib import admin

# Register your models here.
from .models import Database
from .models import Server
from .models import ServerGroup


class ServerGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()


class ServerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "host")

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()


class DatabaseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "host", "username", "storage_type")

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()


admin.site.register(Database, DatabaseAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(ServerGroup, ServerGroupAdmin)