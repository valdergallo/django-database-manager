from server.models import (
    UploadStorageConfig,
    ConnectionKeys,
    Database,
    Server,
)
from server.serializers import (
    UploadStorageConfigSerializer,
    ConnectionKeySerializer,
    DatabaseSerializer,
    ServerSerializer,
)
from rest_framework import viewsets


class UploadStorageConfigModelViewSet(viewsets.ModelViewSet):
    queryset = UploadStorageConfig.objects.all()
    serializer_class = UploadStorageConfigSerializer


class ConnectionKeyModelViewSet(viewsets.ModelViewSet):
    queryset = ConnectionKeys.objects.all()
    serializer_class = ConnectionKeySerializer


class DatabaseModelViewSet(viewsets.ModelViewSet):
    queryset = Database.objects.all()
    serializer_class = DatabaseSerializer


class ServerModelViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
