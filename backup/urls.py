from django.urls import include
from django.urls import path
from rest_framework import routers

from .views import BackupModelViewSet, RestoreJobModelViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'backups', BackupModelViewSet)
router.register(r'restore_jobs', RestoreJobModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
