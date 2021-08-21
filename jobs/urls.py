from django.urls import include
from django.urls import path
from rest_framework import routers

from jobs.views import BackupModelViewSet, RestoreModelViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'backups', BackupModelViewSet)
router.register(r'restores', RestoreModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
