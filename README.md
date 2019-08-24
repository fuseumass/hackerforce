# <img src="https://github.com/hackumass/hackerforce/raw/master/website/static/hackerforce-logo.png" height=32 alt="HackerForce Logo" /> HackerForce

<a href="https://www.youtube.com/watch?v=2RprLpSDjKU"><img src="https://i.imgur.com/NwLoofi.png" alt="HackerForce Demo Video" width=400></a>


`HackerForce` is a tool created to help hackathon organizers manage their sponsorship leads and keep track of contacts, emails and more. Every year hackathon organizers need to contact hundreds of contacts who work at hundreds of companies to request sponsorship. The process for this usually involves various rounds of customized emails to various groupings of companies. This tool aims to create a user friendly interface to see the status of various companies, store the details of certain contacts and overall manage the information required for hackathon sponsorship.

Many aspects of the application are similar to the CRM tool known as SalesForce and the project idea can be simply summed up as a subset of SalesForce features that is open-source and extensible for use by hackathon organizers or anyone else who desires an open-source, free CRM tool.

For set up see below. For more documentation, see the wiki.

## Docker Setup
1. Install Docker on your machine. For non-Linux hosts, open the Docker application as well.
2. Build: `$ docker build -t hacker-force .`
3. Runserver: ```$ docker run -v `pwd`:/app -p 8080:8080 -it hacker-force```
4. Shell: ```$ docker exec -it `docker ps --format '{{.ID}}' -f 'ancestor=hacker-force'` /bin/bash```
5. Log in as `admin` `admin`. You should be able to navigate through the application and interact with dummy data!

## Custom Environment Setup

These instructions shouldn't be necessary, as Docker is the preferred setup.

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
pip install django-heroku django-bootstrap4 django-tabler django-widget-tweaks phonenumbers django-phonenumber-field faker django-extensions django-ckeditor django-multiselectfield
```

### Installing the project

``` sh
git clone https://github.com/hackumass/hackerforce.git && cd hackerforce
pipenv install
pipenv shell
init.sh

# Or on windows
init.bat
```

## Creating new models (or changing existing models)
Make sure you run the following commands if you do any of the following:
* Edit a model (ie. change the database schema)
    * This includes **any** changes you make including: adding a field, removing a field, and renaming a field
* Delete a model
* Add a model

``` sh
init.sh # deletes db.sqlite3
# Or on windows
init.bat # deletes db.sqlite3

# For all platforms
python manage.py runserver
```

**It should be noted that the above commands will delete your developement database! Only run it in a dev environment and remember that any objects you've created for development purposes will be deleted!**

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

## License: MIT
