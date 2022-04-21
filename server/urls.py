from django.urls import include
from django.urls import path
from rest_framework import routers

from server.views import (
    UploadStorageConfigModelViewSet,
    ConnectionKeyModelViewSet,
    DatabaseModelViewSet,
    ServerModelViewSet,
)

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"upload_storages", UploadStorageConfigModelViewSet)
router.register(r"connection_keys", ConnectionKeyModelViewSet)
router.register(r"databases", DatabaseModelViewSet)
router.register(r"servers", ServerModelViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
