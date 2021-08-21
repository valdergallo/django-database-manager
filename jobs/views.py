from jobs.models import Backup, Restore
from jobs.serializers import BackupSerializer, RestoreSerializer
from rest_framework import viewsets


class BackupModelViewSet(viewsets.ModelViewSet):
    queryset = Backup.objects.all()
    serializer_class = BackupSerializer


class RestoreModelViewSet(viewsets.ModelViewSet):
    queryset = Restore.objects.all()
    serializer_class = RestoreSerializer
