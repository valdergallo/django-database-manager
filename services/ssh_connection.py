from functools import wraps
from fabric import Connection
from jobs.models import JOB_STATUS


def get_connection(server):
    return Connection(
        host=server.host,
        user=server.connect_username,
        port=server.connect_port,
        connect_kwargs=server.get_keys(),
    )


def inject_job_connection(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        print("Starting connetion")
        if len(args):
            job_id = args[0]
        else:
            job_id = kwds.get("job_id")

        # Need implement one get_job_by_id before use this function
        job = get_job_by_id(job_id)

        if job:
            server = job.server
            con = get_connection(server)
            try:
                return f(*args, con=con, job=job, **kwds)
            except Exception as error:
                job.status = JOB_STATUS.ERROR
                job.error_logs = str(error)
                job.save()
                print("ERROR ", error)
            finally:
                con.close()

    return wrapper
