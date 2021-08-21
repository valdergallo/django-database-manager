from rest_framework import serializers

from .models import Backup, RestoreJob


class BackupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backup
        fields = "__all__"
        read_only_fields = ["user"]


class RestoreJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestoreJob
        fields = "__all__"
        read_only_fields = ["user"]
