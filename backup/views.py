from backup.models import Backup, RestoreJob
from backup.serializers import BackupSerializer, RestoreJobSerializer
from rest_framework import viewsets


class BackupModelViewSet(viewsets.ModelViewSet):
    queryset = Backup.objects.all()
    serializer_class = BackupSerializer

class RestoreJobModelViewSet(viewsets.ModelViewSet):
    queryset = RestoreJob.objects.all()
    serializer_class = RestoreJobSerializer
