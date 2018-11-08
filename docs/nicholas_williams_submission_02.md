# Nicholas Williams

## Contact Model

I created a Contacts model with needed fields. I made it so that the contacts page
dynamically renders using contacts from the database. The contact model
also has a special phonenumber field using an external package that allows for
easier validation and comes with some handy widgets. I also created CRUD forms
for the contacts model that function and have links on the contacts page.

## Foreign Keys

I added association between the models and updated some of the templates to
use those associations.

## Init.py

I wrote the init.py script that generates data for all of the models to populate
the ui.

## Misc Cleanup

Created a base form template that makes creating forms easier.

Fixed a bug where the spacing on our pages was inconsistent.

Made some minor changes to other peoples work to keep styling consistent.

Abstracted project out into multiple apps to keep file structure cleaner.

## Carryover from Part 1

Base templates for header, body, footer, etc.

Implementing url mappings.

Adding static files for css and js libraries we're using.

Various config things like changing our templating engine to jinja2 and heroku integration.

Hosting the website on a heroku server.
