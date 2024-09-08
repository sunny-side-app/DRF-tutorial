#!/bin/bash
./wait-for-it.sh db:3306 -t 0
python3 manage.py makemigrations clothes_shop
python3 manage.py migrate
python3 manage.py test
exec "$@"