from django.db import models
from django.contrib.auth.models import User
from server.models import Server, Database
from django.db.models.signals import post_save
from jobs.tasks import create_backup_task
from django.dispatch import receiver


class JOB_STATUS(models.TextChoices):
    REQUEST = "REQUEST"
    QUEUE = "QUEUE"
    CREATED = "CREATED"
    ERROR = "ERROR"


def user_directory_path(instance, filename):
    return f"backups/user_{instance.user.id}/{instance.server.name}/{instance.database.name}_{filename}"


class Backup(models.Model):
    name = models.CharField(max_length=150)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=JOB_STATUS.choices,
        max_length=10,
        default=JOB_STATUS.REQUEST,
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, null=True, blank=True
    )
    database = models.ForeignKey(
        Database,
        on_delete=models.CASCADE,
    )
    server = models.ForeignKey(
        Server,
        on_delete=models.CASCADE,
    )
    description = models.CharField(max_length=500, null=True, blank=True)
    filename = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    error_logs = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.status}) | {self.server}"

    def create_task(self):
        create_backup_task.apply_async([self.id])


class Restore(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=JOB_STATUS.choices,
        max_length=10,
        default=JOB_STATUS.REQUEST,
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, null=True, blank=True
    )
    database = models.ForeignKey(
        Database,
        on_delete=models.CASCADE,
    )
    server = models.ForeignKey(
        Server,
        on_delete=models.CASCADE,
    )
    backup = models.ForeignKey(
        Backup,
        on_delete=models.CASCADE,
    )
    logs = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.id} ({self.status})"


@receiver(post_save, sender=Backup, dispatch_uid="create_backup_task")
def create_backup_post_save(sender, instance, **kwargs):
    if instance.status == JOB_STATUS.REQUEST:
        instance.create_task()