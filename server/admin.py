from django.contrib import admin

# Register your models here.
from .models import Database
from .models import Server
from .models import ConnectionKeys
from .models import UploadStorageConfig


class UploadStorageConfigAdmin(admin.ModelAdmin):
    list_display = ("id", "storage_type")

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()


class ServerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "host")
    list_display_links = ("id", "name")

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()


class DatabaseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "username", "storage_type")
    list_display_links = ("id", "name")

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()


class ConnectionKeyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "key_type")
    list_display_links = ("id", "name")

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()


admin.site.register(Database, DatabaseAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(ConnectionKeys, ConnectionKeyAdmin)
admin.site.register(UploadStorageConfig, UploadStorageConfigAdmin)
