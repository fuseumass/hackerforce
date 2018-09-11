# COMPSCI 326 Web Programming

This is the project repository template that your COMPSCI 326 team
will `fork` and use to begin your semester project work. Please follow
the instructions carefully in each of the project submission
requirements for your team to be successful. This is the structure of
this repository:

* `docs` - this folder is used to store all documents that are
  requested as part of the submission.
* `src` - this folder is used for your project code.

Please read the [markdown
cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
to help you author documents using markdown.

## Deployment to Heroku

    $ git init
    $ git add -A
    $ git commit -m "Initial commit"

    $ heroku create
    $ git push heroku master

    $ heroku run python manage.py migrate

See also, a [ready-made application](https://github.com/heroku/python-getting-started), ready to deploy.


## License: MIT

## Further Reading

- [Gunicorn](https://warehouse.python.org/project/gunicorn/)
- [WhiteNoise](https://warehouse.python.org/project/whitenoise/)
- [dj-database-url](https://warehouse.python.org/project/dj-database-url/)
