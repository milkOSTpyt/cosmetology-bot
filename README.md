# Cosmetology bot with Django admin

![](https://i.ibb.co/wWYKv46/screen-20230530-160655-2-7-I6s-W08s-1.gif)

### Deploy project ( docker-compose )
Install docker and docker-compose and next run command:

#### If necessary on the host machine:
`sudo sysctl vm.overcommit_memory=1`

#### Copy and fill env file:
`cp example.env .env`

#### After update variables:
`docker compose up -d --build`

#### Create superuser:
`docker compose run --rm django_admin python start_admin.py createsuperuser`

#### Load fixtures:
`docker compose run --rm django_admin python start_admin.py loaddata admin/fixtures/filling_database.json`

### Update project (docker-compose):
For update project you need pull latest changes from git, and run next command:\
`docker compose up -d --build`