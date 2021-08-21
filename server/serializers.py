from rest_framework import serializers

from server.models import (
    UploadStorageConfig,
    ConnectionKeys,
    Database,
    Server,
)


class UploadStorageConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadStorageConfig
        fields = "__all__"
        read_only_fields = ["user"]


class ConnectionKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionKeys
        fields = "__all__"
        read_only_fields = ["user"]


class DatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Database
        fields = "__all__"
        read_only_fields = ["user"]


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = "__all__"
        read_only_fields = ["user"]
