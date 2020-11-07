from django.db import models
from django.contrib.auth.models import User


class UploadServerProviderEnum(models.TextChoices):
    AMAZON_S3 = "AMS3", "Amazon S3"
    APACHE_LIBCLOUD = "ACLD", "Apache Libcloud"
    AZURE_STORAGE = "ASTG", "Azure Storage"
    DIGITAL_OCEAN = "DGON", "Digital Ocean"
    DROPBOX = "DRPB", "Dropbox"
    FTP = "FTP"
    GOOGLE_CLOUD_STORAGE = "GCTG", "Google Cloud Storage"
    SFTP = "SFTP"


class UploadStorageConfig(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, null=True, blank=True
    )
    storage_type = models.CharField(
        choices=UploadServerProviderEnum.choices, max_length=5
    )
    config_vars = models.TextField(max_length=500)

    def __str__(self):
        return self.storage_type


class Database(models.Model):
    name = models.CharField(max_length=250)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200, null=True, blank=True)
    host = models.CharField(max_length=250, default="localhost")
    ssl_key = models.FileField(upload_to="ssh_keys", null=True, blank=True)
    active_to_backup = models.BooleanField(default=True)
    active_to_retore = models.BooleanField(default=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, null=True, blank=True
    )
    storage_type = models.ForeignKey(
        UploadStorageConfig,
        on_delete=models.CASCADE,
        editable=False,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name} - {self.host}"


class Server(models.Model):
    name = models.CharField(max_length=250)
    host = models.CharField(max_length=250, default="localhost")
    connect_username = models.CharField(max_length=150, default="ubuntu")
    ssh_key = models.FileField(upload_to="ssh_keys", null=True, blank=True)
    ssh_key_pass = models.CharField(max_length=250, null=True, blank=True)
    databases = models.ManyToManyField(Database, blank=True)
    backup_dir = models.CharField(max_length=100, default="/backups/")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, null=True, blank=True
    )

    def __str__(self):
        return f"{self.name} - {self.host}"


class ServerGroup(models.Model):
    name = models.CharField(max_length=250)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, null=True, blank=True
    )
    servers = models.ManyToManyField(Server, blank=True)

    def __str__(self):
        return f"{self.name}"
