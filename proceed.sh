#!/bin/bash

git stash
git stash drop
git clean -f
git pull origin master
cp -f ../.env .env
python manage.py makemigrations
python manage.py migrate