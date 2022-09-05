# Foodgram

[About](#about) /
[Changelog](#changelog) /
[Deploy](#deploy) /
[Healthcheck](#healthcheck)

## About
Foodgram recipes review service API.

## Changelog
Release 20220905:
* feat(./backend/foodgram_api/): project settings, general routing && token based authentication setup
* feat(./backend/foodgram_api/api/): serializers, custom permissions, filters, views && API routing setup
* feat(./backend/foodgram_api/recipes/): models && admin panel setup
* feat(./backend/foodgram_api/users/): models && admin panel setup

## Deploy
Clone repository, init venv and install dependencies:

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

Specify variables according to the [template](https://github.com/avtorsky/foodgram_project_react/blob/master/infra/.env.template), save modified variables to .env and launch nginx container with frontend:

```bash
docker-compose up -d --build nginx
```

Switch to backend directory and launch backend app:

```bash
cd ../backend/foodgram_api/
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver 0.0.0.0:8000
```

## Healthcheck
* GUI host: http://localhost/signin
* API specs: http://localhost/api/docs/

