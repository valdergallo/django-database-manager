from fabric import Connection
from fabric import task


@task(
    help={
        "env-name": "Name of the server which needs to be updated",
    }
)
def config(arg, env_name=None):
    """
    Create backup from database
    Example:
        fab config -e dev
        or
        fab config --env-name=dev
    """
    env = ENVS[env_name]

    print(f"Start config in {env_name}")

    for host in env["hosts"]:
        with Connection(host=host, user="ubuntu", connect_kwargs=env["keys"]) as con:
            print(f"Config backup directory")
            con.sudo("mkdir -p %s" % env["backup_dir"])
            con.sudo("chmod 777 %s" % env["backup_dir"])

    print("Backup finished")
