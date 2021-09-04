from jobs.models import Restore, Database, Backup, JOB_STATUS, Server
from services.ssh_connection import inject_job_connection
from tempfile import NamedTemporaryFile
import os


def get_job_by_id(job_id):
    "Method used in @inject_job_connection"
    return Restore.objects.get(id=job_id)


def generate_sql_to_drop_database(database:Database, con, remote_backup_dir="/backups/"):
    # create temp file to download
    disconect_file = NamedTemporaryFile(delete=False, suffix=f'_{database.name}.sql', prefix='disconect_file_')

    # get temporary filename
    filename = disconect_file.name

    # write sql to disconect connections in database to be restored
    with open(disconect_file, "w") as sqls:
        sqls.write(
            f"UPDATE pg_database SET datallowconn = 'false' WHERE datname = '{database.name}';\n"
        )
        sqls.write(f"ALTER DATABASE {database.name} CONNECTION LIMIT 1;\n")
        sqls.write(
            f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{database.name}';\n"
        )
        sqls.write(f"DROP DATABASE {database.name};\n")
        sqls.write(f"CREATE DATABASE {database.name};\n")
        sqls.write(
            f"GRANT ALL PRIVILEGES ON DATABASE {database.name} TO {database.username};\n"
        )

    # upload disconect file to server
    con.put(disconect_file, remote_backup_dir)

    # Remove the file
    os.unlink(filename)

    # get filename without diretories
    base_name = os.path.basename(filename)

    return f"{remote_backup_dir}{base_name}"


def rename_database_name_in_file(restore_job:Restore, target_file, con):
    if restore_job.backup.database.name != restore_job.database.name:
        # rename database name
        print(f"Rename database {restore_job.backup.database.name} to {restore_job.database.name} in {target_file}")
        con.sudo(f'sed -i "s/{restore_job.backup.database.name}/{restore_job.database.name}/g" {target_file}')


def load_sqlfile_in_database(backup_file, database: Database, server: Server, con, hide_output=False):
    print(
        f"Load {backup_file} SQL in {database.username} with use: {server.host}"
    )
    # load database
    con.sudo(
        f"cat {backup_file} | psql -d postgres -U {database.username} -h {server.host}",
        hide=hide_output,
    )


def load_ziped_sqlfile_in_database(backup_file, database: Database, server: Server, con, hide_output=False):
    print(
        f"Load {backup_file} SQL in {database.username} with use: {server.host} to {database.name}"
    )
    # load database
    con.sudo(
        f"gunzip -k -c {backup_file} | psql -U {database.username} -h {server.host} -d {database.name}",
        hide=hide_output,
    )


def upload_backup_file_to_server(backup, con, remote_backup_dir='/backups/', hide_output=False):
    print(
        f"Upload backup file to server"
    )
    # upload disconect file to server
    con.put(backup.filename.path, remote_backup_dir)
    base_name = os.path.basename(backup.filename.path)
    return os.path.join(remote_backup_dir, base_name)


@inject_job_connection
def restore_backup_file(job_id=None, con=None, job=None):
    "Restore backup file in server and download file"
    if not job:
        print("Invalid job_id: %s" % job_id)
        return

    database = job.database
    server = job.server
    backup = job.backup

    drop_database_filename = generate_sql_to_drop_database(database, con)
    backup_filename = upload_backup_file_to_server(backup=backup, con=con)

    load_sqlfile_in_database(backup_file=drop_database_filename, database=database, server=server)
    load_ziped_sqlfile_in_database(backup_file=backup_filename, database=database, server=server)

    # update job status
    job.status = JOB_STATUS.DONE
    job.save()

    print(f"Restore for {job.id} done")