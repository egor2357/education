#!/bin/bash
case $1 in
  dev)
    python3 manage.py runserver --settings=back.settings.dev $2
    ;;
  prod)
    python3 manage.py collectstatic --noinput
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py runserver --settings=back.settings.prod $2
    ;;
esac
