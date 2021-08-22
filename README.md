# DBuddy

DBuddy offers cost-effective open-source, cloud-based database backup, and disaster recovery solutions

# Using SSH

https://hackertarget.com/ssh-examples-tunnels/

# Using Fabric

https://docs.fabfile.org/en/2.5/getting-started.htm

# DEVELOP

# Start run RabbitMQ server

> docker-compose up -d

# Start django project

> python -m venv .venv
> source .venv/bin/activate
> pip install -r requirements.txt

# Run server

> python manage.py runserver

or

> make runserver

# Run Celery Worker

> celery -A main worker -l INFO

or

> make worker