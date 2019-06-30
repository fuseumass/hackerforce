#!/bin/bash
python manage.py shell -c'from profiles.models import User; User.objects.get(username="admin")';
if [[ "$?" == "1" ]]; then
  echo Empty database. Running init script...
  chmod +x init.sh
  ./init.sh
else
  echo Admin user exists. Running migrate...
  python manage.py migrate
fi
