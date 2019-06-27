python manage.py shell -c'from profiles.models import User; User.objects.get(username="admin")';
if [[ "$?" == "1" ]]; then
  echo Running init script
  chmod +x init.sh
  ./init.sh
else
  echo Admin user exists
fi
