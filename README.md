# Cosmetology bot with Django admin

### Deploy project ( docker-compose )
Install docker and docker-compose and next run command:

#### Copy and fill env file:
`cp example.env .env`

#### After update variables:
`sudo docker-compose up -d --build`

#### Create superuser:
`sudo docker compose run --rm django_admin python start_admin.py createsuperuser`

#### Load fixtures:
`sudo docker compose run --rm django_admin python start_admin.py loaddata admin/fixtures/filling_database.json`

### Update project (docker-compose):
For update project you need pull latest changes from git, and run next command:
`sudo docker-compose up -d --build`