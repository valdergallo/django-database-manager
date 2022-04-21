from celery import shared_task


@shared_task
def create_backup_task(backp_instance_id):
    from services.psql.create_backup import create_backup_file

    print("backp_instance_id ", backp_instance_id)
    create_backup_file(backp_instance_id)


@shared_task
def retore_backup_task(x, y):
    return x * y
