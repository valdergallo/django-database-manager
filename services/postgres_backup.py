import time
from django.core.files.base import ContentFile
from jobs.models import Backup, JOB_STATUS
from services.ssh_connection import backup_connection
from tempfile import TemporaryFile
import os

DATE_NOW = time.strftime("%Y%m%d%H%M%S")

def create_name(job):
    if not job.name:
        fname = f"{DATE_NOW}.sql.gz"
    else:
        fname = f"{job.name}_{DATE_NOW}.sql.gz"
    return fname


def download_backup_in_django_file(con, fname, server):
    print("Start download backup from server")
    remote_name = os.path.join(server.backup_dir, fname)

    # create temp file to download
    local_file = TemporaryFile()
    con.get(remote_name, local_file)

    # convert temp file in one django content file
    content = ContentFile(local_file.read())
    content.name = fname

    return content


def dump_data_in_server(con, fname, database, server):
    remote_name = os.path.join(server.backup_dir, fname)
    print(f"Start pg_dump in server for {database.name} in {remote_name}")
    # postgres backup
    con.sudo(
        f'su - postgres -c "pg_dump -b -O -x -o -Z9 -h {server.host} -U {database.username} -d {database.name} -f {remote_name}"'
    )


@backup_connection
def create_backup_file(backup_job_id=None, con=None):
    "Create backup file in server and download file"
    backup_job = Backup.objects.get(id=backup_job_id)

    if not backup_job:
        print("Invalid backup_job_id: %s" % backup_job_id)
        return

    database = backup_job.database
    server = backup_job.server

    fname = create_name(backup_job)

    dump_data_in_server(con=con, fname=fname, database=database, server=server)

    content = download_backup_in_django_file(con=con, fname=fname, server=server)

    # save content file in backup_job
    backup_job.filename = content
    backup_job.status = JOB_STATUS.CREATED
    backup_job.save()

    print(f"Backup for {backup_job.id} done")
