from functools import wraps
from fabric import Connection
from jobs.models import JOB_STATUS, Backup


def get_connection(server):
    return Connection(
        host=server.host,
        user=server.connect_username,
        port=server.connect_port,
        connect_kwargs=server.get_keys(),
    )


def backup_connection(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        print("Starting connetion")
        if len(args):
            backup_job_id = args[0]
        else:
            backup_job_id = kwds.get("backup_job_id")

        backup_job = Backup.objects.get(id=backup_job_id)

        if backup_job:
            server = backup_job.server
            con = get_connection(server)
            try:
                return f(*args, con=con, **kwds)
            except Exception as error:
                backup_job.status = JOB_STATUS.ERROR
                backup_job.error_logs = str(error)
                backup_job.save()
                print("ERROR ", error)
            finally:
                con.close()
    return wrapper

