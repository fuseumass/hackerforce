# COMPSCI 326 Web Programming

This is the project repository template that your COMPSCI 326 team
will `fork` and use to begin your semester project work. Please follow
the instructions carefully in each of the project submission
requirements for your team to be successful. This is the structure of
this repository:

* `docs` - this folder is used to store all documents that are
  requested as part of the submission.
* `src` - this folder is used for your project code.

Please read the [markdown cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) to help you author documents using markdown.

## Environment Setup

### Setup the VM after installing Virtualbox and Vagrant

```sh
# install vm via vagrantfile
git clone https://github.com/umass-cs-326/326_progenv.git && cd 326_progenv
vagrant up
vagrant ssh
# start in local /vagrant folder by default
echo "cd /vagrant" >> ~/.bashrc
```

### Installing Python 3.6 with Pyenv and installing Pyenv
```sh
# Anaconda comes with python3.6, so using the latest Anaconda distro will also work in place of pyenv

# MacOS
brew install pyenv

# Linux
git clone https://github.com/yyuu/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile

# install python3.6
pyenv install 3.6.6

# install pipenv
pip install --user pipenv
```

### Installing dependencies
``` sh
pip install django-heroku django-jinja django-bootstrap4 django-tabler django-widget-tweaks phonenumbers django-phonenumber-field faker
```

### Installing the project

``` sh
cd /vagrant
git clone https://github.com/326-queue/project.git && cd project
pipenv install
pipenv shell
python manage.py migrate
python manage.py runserver
```

## Creating new models (or changing existing models)
Make sure you run the following commands if you do any of the following:
* Edit a model (ie. change the database schema)
    * This includes **any** changes you make including: adding a field, removing a field, and renaming a field
* Delete a model
* Add a model

``` sh
rm -f db.sqlite3 # optional, if you need to run this you've
                 # made breaking changes to the database schema
python manage.py makemigrations # optional add the name of your 
                                # app as an additional arg 
                                # for example: python manage.py makemigrations profiles
python manage.py migrate
python manage.py runserver
```

**It should be obvious but one of the above commands deletes the developement database! Only run it in a dev environment and remember that any objects you've created for development purposes will be deleted!**

## Deployment to Heroku
Install heroku-cli if you don't have it
```
# linux
curl https://cli-assets.heroku.com/install.sh | sh

# mac
brew install heroku/brew/heroku
```

Deploy
```sh
heroku create
git push heroku master

heroku run python manage.py migrate
```

See also, a [ready-made application](https://github.com/heroku/python-getting-started), ready to deploy.


## License: MIT

## Further Reading

- [Gunicorn](https://warehouse.python.org/project/gunicorn/)
- [WhiteNoise](https://warehouse.python.org/project/whitenoise/)
- [dj-database-url](https://warehouse.python.org/project/dj-database-url/)
