from __future__ import absolute_import
from fabric import task
from fabric import Connection
import os
import io
import time
import glob
from pprint import pprint
from server.models import Server
from jobs.models import Backup
from django.core.files.base import ContentFile

DATE_NOW = time.strftime("%Y%m%d%H%M%S")

def get_connection(server):
    return Connection(
            host=server.host,
            user=server.connect_username,
            port=server.connect_port,
            connect_kwargs=server.get_keys(),
        )

def backup_server(server_name=None, name_backup=None, backup_job=None):
    server = Server.objects.filter(name=server_name)
    if not server:
        print("Invalid server name")

    print(f"Start Backup in {server_name}")

    with get_connection(server) as con:
        print(f"change user to postgres")
        for database in server.databases:
            create_backup_file(
                con,
                server,
                database,
                name_backup,
                backup_job,
            )
    print("Backup finished")


def create_backup_file(
    con,
    server=None,
    database=None,
    name_backup=None,
    backup_job=None,
):
    "Create backup file in server and download file"

    if not name_backup:
        fname = f"{database.name}_{DATE_NOW}.sql.gz"
    else:
        fname = f"{database.name}_{name_backup}_{DATE_NOW}.sql.gz"

    if not backup_job:
        backup_job = Backup.objects.create(
            name=name_backup, user=server.user, database=database, server=server
        )

    print(f"Start pg_dump in server for {database.name} in {server.backup_dir}{fname}")

    con.sudo(
        f'su - postgres -c "pg_dump -b -O -x -o -Z9 -h {server.host} -U {database.username} -d {database.name} -f {server.backup_dir}{fname}"'
    )

    remote_name = server.backup_dir + fname

    print(f"Start download backup from server")

    local_file = ContentFile()
    con.get(remote_name, local_file)

    backup_job.filename.save(fname, local_file, save=False)
    backup_job.save()

    print(f"Backup for {database.name} done")


def _generate_sql_to_drop_database(database_name, database_user, con, backup_dir):
    """"""
    filename = f"disconect_database_{database_name}.sql"
    disconect_file = f"/tmp/{filename}"

    with open(disconect_file, "w") as sqls:
        sqls.write(
            f"UPDATE pg_database SET datallowconn = 'false' WHERE datname = '{database_name}';\n"
        )
        sqls.write(f"ALTER DATABASE {database_name} CONNECTION LIMIT 1;\n")
        sqls.write(
            f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{database_name}';\n"
        )
        sqls.write(f"DROP DATABASE {database_name};\n")
        sqls.write(f"CREATE DATABASE {database_name};\n")
        sqls.write(
            f"GRANT ALL PRIVILEGES ON DATABASE {database_name} TO {database_user};\n"
        )

    con.put(disconect_file, backup_dir)
    con.local(f"rm {disconect_file}")

    return f"{backup_dir}{filename}"


def _generate_backup_filename(backup_name, database.name, server_name, backup_dir):
    filename = f"{database.name}_{backup_name}.sql"

    local_backup_name = os.path.join(DIRNAME, server_name, filename)
    remote_backup_name = os.path.join(backup_dir, filename)

    if not os.path.exists(local_backup_name):
        return None, None

    return local_backup_name, remote_backup_name


def _search_backup_file(backup_name, server_name, backup_dir):
    files = glob.glob(f"./{server_name}/*.*")
    local_backup_name = [i for i in files if backup_name in i]
    remote_backup_name = [
        i.replace(f"./{server_name}/", backup_dir) for i in local_backup_name
    ]

    return local_backup_name, remote_backup_name


def _remove_database.name_from_remote_backup_names(database.name, remote_backup_names):
    key = None
    for key, name in enumerate(remote_backup_names):
        if database.name in name:
            print("Remove from restore file: %s" % name)
            break
    if key is not None:
        remote_backup_names.pop(key)
    return remote_backup_names


@task(
    help={
        "env-name": "- Server to restore backup -",
        "name-backup": "Backup date or point name",
        "database-name": "Set only one database to be updated",
        "database-user": "Set only one database user",
        "target-name": "Server to restore backup. If null target-name will be the same that env-name",
        "ignore-black-list": "Remove protection from restore ",
    }
)
def restore(
    con,
    server_name=None,
    name_backup=None,
    database_name=None,
    database_user="nic",
    target_name=None,
    ignore_black_list=None,
):
    """Create backup from database
    Example:
        fab restore -e qas -n mexico
        # or send database to another instance
        fab restore -e qas -n mexico -t dev
    """
    try:
        from_db = ENVS[server_name]
    except KeyError:
        print("Invalid environment keyname, check your constants")

    if not database_name:
        database_names = from_db["databases"]
    else:
        database_names = [database_name]

    if target_name:
        target_db = ENVS[target_name]
    else:
        target_db = from_db

    for host in target_db["hosts"]:
        with Connection(
            host=host, user="ubuntu", connect_kwargs=target_db["keys"]
        ) as con:
            local_backup_names, remote_backup_names = _search_backup_file(
                name_backup, server_name, target_db["backup_dir"]
            )

            if not local_backup_names or not remote_backup_names:
                print(f"No backup file for {name_backup} from {server_name}")
                continue

            upload_all_files(local_backup_names, target_db, con)

            # delete all tables
            for db_index, database.name in enumerate(database_names):

                from_database.name = from_db["databases"][db_index]
                to_database.name = target_db["databases"][db_index]
                to_db_host = target_db["db_host"]
                to_db_username = target_db["db_username"]
                from_db_username = from_db["db_username"]

                if (
                    database.name in RESTORE_BLACK_LIST
                    or from_database.name in RESTORE_BLACK_LIST
                    or to_database.name in RESTORE_BLACK_LIST
                ):

                    print("-" * 80)
                    print(f"Restored bypass {database.name}")
                    remote_backup_names = _remove_database.name_from_remote_backup_names(
                        database.name, remote_backup_names
                    )
                    print("-" * 80)
                    continue

                print(f"Start reset database {database.name}")

                disconect_file = _generate_sql_to_drop_database(
                    database.name, database_user, con, target_db["backup_dir"]
                )

                # restore all files
                for remote_backup_name in remote_backup_names:
                    if database.name in remote_backup_name:
                        database_restore_actions(
                            con,
                            from_database.name,
                            to_database.name,
                            remote_backup_name,
                            database.name,
                            disconect_file,
                            to_db_host,
                            to_db_username,
                            from_db_username,
                        )

            # restart all services
            print(f"Start reload services")
            con.run("source reset-service")

            # delete backup in remote diretory
            # con.run(f'rm {remote_backup_name}')


@task(
    help={
        "env-name": "Server to restore backup",
        "limit": "Limit files",
    }
)
def list_backups(arg, server_name, limit=10):
    "List backup files"
    files = glob.glob(f"./{server_name}/*.*")
    files.sort(key=os.path.getmtime)
    for file in files[:limit][::-1]:
        last_update = time.ctime(os.path.getmtime(file))
        print(f"{last_update} | {file}")


@task(
    help={
        "env-name": "Server to restore backup",
    }
)
def list_hosts(con, server_name=None):
    "List config hosts"
    if server_name:
        env = ENVS[server_name]
        pprint(env)
        print("")
    else:
        for i in ENVS.keys():
            print(f"- {i}")


@task(
    help={
        "env-name": "Name of the server which needs to be updated",
    }
)
def config(arg, server_name=None):
    """
    Create backup from database
    Example:
        fab config -e dev
        or
        fab config --env-name=dev
    """
    env = ENVS[server_name]

    print(f"Start config in {server_name}")

    for host in env["hosts"]:
        with Connection(host=host, user="ubuntu", connect_kwargs=env["keys"]) as con:
            print(f"Config backup directory")
            con.sudo("mkdir -p %s" % env["backup_dir"])
            con.sudo("chmod 777 %s" % env["backup_dir"])

    print("Backup finished")


@task(
    help={
        "host-name": "Name of the server which needs to be tested",
    }
)
def test(arg, host_name):
    """
    Test database backup connection
    Example:
        fab test huru-demo
    """
    print(f"Start test in host: {host_name}")

    env = ENVS[host_name]

    for host in env["hosts"]:
        with Connection(host=host, user="ubuntu", connect_kwargs=env["keys"]) as con:
            con.run("uname -a")
            con.run("echo $DATABASE_HOST")
            con.run("echo $DATABASE_USER")

    print("Test finished")


@task(
    help={
        "group": "Name of the server which needs to be tested",
    }
)
def deploy(arg, group="core"):
    "roda comando em todos os cores"
    env = GROUP_ENVS[group]
    for host in env["hosts"]:
        with Connection(host=host, user="ubuntu", connect_kwargs=env["keys"]) as con:
            print("-" * 80)
            print("Start deploy in HOST: ", host)
            con.run("docker-compose pull || true")
            con.run(
                "docker stack deploy -c docker-compose.yml ubuntu --with-registry-auth || true"
            )
            con.run(
                'docker rmi $(docker images --filter "dangling=true" -q --no-trunc) || true'
            )
            print("-" * 80)

    print("Deploy finished")


def upload_all_files(local_backup_names, target_db, con):
    # upload all files
    for local_backup_name in local_backup_names:
        remote_file = os.path.join(
            target_db["backup_dir"], os.path.basename(local_backup_name)
        )
        print(f"Check if file exists: {remote_file}")
        if con.run(f"test -f {remote_file}", warn=True).failed:
            print(f"Start upload backup in {local_backup_name}")
            con.put(local_backup_name, target_db["backup_dir"])
        else:
            print("OK")


def database_restore_actions(
    con,
    from_database.name,
    to_database.name,
    remote_backup_name,
    database.name,
    disconect_file,
    to_db_host,
    to_db_username,
    from_db_username,
):
    print(f"RESTORE BACKUP {remote_backup_name} in {database.name}")

    if from_database.name != to_database.name:
        print(f"Rename database {from_database.name} to {to_database.name} in {disconect_file}")
        # rename database name
        con.sudo(f'sed -i "s/{from_database.name}/{to_database.name}/g" {disconect_file}')

    print(f"DELETE DATABASE {database.name}")
    print(
        f"Load {disconect_file} SQL in {to_db_host} with use: {to_db_username} to {to_database.name}"
    )

    # load database
    con.sudo(
        f"cat {disconect_file} | psql -d postgres -U {to_db_username} -h {to_db_host}",
        hide=HIDE_OUTPUT,
    )

    print(
        f"Load {remote_backup_name} SQL in {to_db_host} with use: {to_db_username} to {to_database.name}"
    )
    # load database
    con.sudo(
        f"gunzip -k -c {remote_backup_name} | psql -U {to_db_username} -h {to_db_host} -d {to_database.name}",
        hide=HIDE_OUTPUT,
    )
