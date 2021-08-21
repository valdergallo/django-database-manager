from rest_framework import serializers

from jobs.models import Backup, Restore


class BackupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backup
        fields = "__all__"
        read_only_fields = ["user"]


class RestoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restore
        fields = "__all__"
        read_only_fields = ["user"]
