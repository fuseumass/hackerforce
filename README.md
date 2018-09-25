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

### Installing latest python version and pipenv

```sh
# install python3.7 from source
sudo apt-get upgrade
sudo apt-get dist-upgrade -y
sudo apt-get install -y build-essential python-dev python-setuptools python-pip python-smbus libncursesw5-dev libgdbm-dev libc6-dev zlib1g-dev libsqlite3-dev tk-dev libssl-dev openssl libffi-dev
cd /usr/src
sudo git clone --single-branch -b 3.7 https://github.com/python/cpython.git && cd cpython
sudo ./configure
sudo make
sudo make altinstall

# update pip
pip3.7 install --user --upgrade pip

# install pipenv
pip3.7 install --user pipenv
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
