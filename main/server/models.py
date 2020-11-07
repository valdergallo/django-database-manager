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


class Database(models.Model):
    name = models.CharField(max_length=250)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    host = models.CharField(max_length=250)
    ssl_key = models.FileField(upload_to="ssh_keys")
    active_to_backup = models.BooleanField(default=True)
    active_to_retore = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    storage_type = models.CharField(choices=UploadServerProviderEnum.choices)

    def __str__(self):
        return f"{self.name} - {self.host}"


class Server(models.Model):
    name = models.CharField(max_length=250)
    host = models.CharField(max_length=250)
    connect_username = models.CharField(max_length=150, default="ubuntu")
    ssh_key = models.FileField(upload_to="ssh_keys")
    ssh_key_pass = models.CharField(max_length=250)
    databases = models.ManyToManyField(Database)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return f"{self.name} - {self.host}"