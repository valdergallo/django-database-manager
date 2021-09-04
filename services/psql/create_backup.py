import time
from django.core.files.base import ContentFile
from jobs.models import Backup, JOB_STATUS
from services.ssh_connection import inject_job_connection
from tempfile import TemporaryFile
import os

DATE_NOW = time.strftime("%Y%m%d%H%M%S")


def get_job_by_id(job_id):
    "Method used in @inject_job_connection"
    return Backup.objects.get(id=job_id)


def create_name(job):
    if not job.name:
        fname = f"{DATE_NOW}.sql.gz"
    else:
        fname = f"{job.name}_{DATE_NOW}.sql.gz"
    return fname


def dump_data_in_server(con, fname, database, server):
    remote_name = os.path.join(server.backup_dir, fname)
    print(f"Start pg_dump in server for {database.name} in {remote_name}")
    # postgres backup
    con.sudo(
        f'su - postgres -c "pg_dump -b -O -x -o -Z9 -h {server.host} -U {database.username} -d {database.name} -f {remote_name}"'
    )


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


@inject_job_connection
def create_backup_file(job_id=None, con=None, job=None):
    "Create backup file in server and download file"
    if not job:
        print("Invalid job_id: %s" % job_id)
        return

    database = job.database
    server = job.server

    fname = create_name(job)

    dump_data_in_server(con=con, fname=fname, database=database, server=server)

    content = download_backup_in_django_file(con=con, fname=fname, server=server)

    # save content file in job
    job.filename = content
    # update job status
    job.status = JOB_STATUS.DONE
    job.save()

    print(f"Backup for {job.id} done")
