# Foodgram

[About](#about) /
[Changelog](#changelog) /
[Deploy](#deploy) /
[Testing](#testing) /
[Healthcheck](#healthcheck)

[![CI](https://github.com/avtorsky/foodgram-project-react/actions/workflows/foodgram_api_dev.yml/badge.svg?branch=master)](https://github.com/avtorsky/foodgram-project-react/actions/workflows/foodgram_api_dev.yml)

## About
Recipe networking service API.

## Changelog
Release 20220916:
* ci: Nginx 443 port ssl config
* ci: Docker production host setup
* ci(./github/workflows/foodgram_api_dev.yml): foodgram_api_dev image delivery pipeline setup
* fix(./backend/foodgram_api/api/urls.py): swap router to SimpleRouter && switch default renderer to JSON
* fix(./infra/): Nginx and Docker config split to dev && production environments

Release 20220911:
* test(./backend/tests/): pytest for /auth && /users API endpoints setup
* fix(./README.md): development deploy specifications update
* fix(./infra/docker-compose.yml): split the deploy workflow for dev && production
* fix(./infra/nginx.conf): split the nginx config for dev && production
* fix(./backend/foodgram_api/api/views.py): current user patch for /users/me API endpoint corner case
* fix(./backend/foodgram_api/users/models.py): username regex patch to match API specs

Release 20220905:
* feat(./backend/foodgram_api/): project settings, general routing && token based authentication setup
* feat(./backend/foodgram_api/api/): serializers, custom permissions, filters, views && API routing setup
* feat(./backend/foodgram_api/recipes/): models && admin panel setup
* feat(./backend/foodgram_api/users/): models && admin panel setup

## Deploy
Clone repository and install all dependencies:

```bash
git clone https://github.com/avtorsky/foodgram_project_react.git
cd backend
python -m venv venv
source venv/bin/activate
cd foodgram_api
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
```

Create ./infra/.env file:

```bash
cd ../../infra
touch .env && nano .env
```

Specify variables according to the [template](https://github.com/avtorsky/foodgram-project-react/blob/master/infra/.env.template), save modified variables to .env then switch to backend directory, run migrations, create superuser and collect static:

```bash
cd ../backend/foodgram_api
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py collectstatic --no-input
python3 manage.py runserver 0:8000
```

Finally initiate nginx build:

```bash
cd ../../infra
docker-compose up -d --build nginx_dev_service
```

## Testing

Switch to testing rootdir

```bash
cd backend
python -m flake8
pytest
```

## Healthcheck
* GUI host: https://foodgram.avtorskydeployed.online
* Admin panel: https://foodgram.avtorskydeployed.online/admin/
* API specs: https://foodgram.avtorskydeployed.online/api/docs/

```
Reviewer credentials
email: review-admin@foodgram.fake
password: fo0dgr@mTest
``` 


