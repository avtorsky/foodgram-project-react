# Foodgram

[About](#about) /
[Changelog](#changelog) /
[Deploy](#deploy) /
[Testing](#testing) /
[Healthcheck](#healthcheck)

[![CI](https://github.com/avtorsky/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?branch=master)](https://github.com/avtorsky/foodgram-project-react/actions/workflows/foodgram_workflow.yml)

## About
Recipe networking service API.

## Changelog
Release 20220911:
* ci: nginx 443 port letsencrypt config
* ci: app production host setup
* ci(./github/workflows/foodgram_workflow.yml): production delivery pipeline setup
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
cd /foodgram-project-react/backend/
python -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
```

Create ./infra/.env file:

```bash
cd ../infra/
touch .env && nano .env
```

Specify variables according to the [template](https://github.com/avtorsky/foodgram-project-react/blob/master/infra/.env.template) and save modified variables to .env and initiate nginx_dev build:

```bash
docker-compose -f docker-compose.dev.yml up -d --build nginx_dev
```

Switch to backend directory, run migrations, create superuser and collect static:

```bash
cd ../backend/foodgram_api/
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py collectstatic --no-input
python3 manage.py runserver 0:8000
```

## Testing

To manually launch unit testing switch back to root backend directory

```bash
cd ../
pwd /foodgram-project-react/backend
pytest && python -m flake8
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


