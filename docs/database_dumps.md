# Database dumps

To generate production DB fixtures:
```bash
$ heroku run -a sponsorship-app python manage.py dumpdata -- > dumpdata-prod-aug1.json
```

To load production DB fixtures locally:
```bash
$ ./docker-run.sh python manage.py migrate
$ ./docker-run.sh python manage.py loaddata dumpdata-prod-aug1.json -e contenttypes
$ ./docker-run.sh bash -c "echo \"
adminuser = User.objects.create_user('admin', 'admin@326.edu', 'admin')
adminuser.save()
adminuser.is_superuser = True
adminuser.is_staff = True
adminuser.save()
\" | python manage.py shell_plus --"
```

When importing a production dump, you MUST add the 'admin' user to prevent `docker-run.sh` from wiping and deleting the database!
