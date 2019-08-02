# Submission 2 Documentation

## Overview of project

`Project` is a tool created to help hackathon organizers manage their sponsorship leads and keep track of contacts, emails and more. Every year hackathon organizers need to contact hundreds of contacts who work at hundreds of companies to request sponsorship. The process for this usually involves various rounds of customized emails to various groupings of companies. This tool aims to create a user friendly interface to see the status of various companies, store the details of certain contacts and overall manage the information required for hackathon sponsorship.

Many aspects of the application are similar to the CRM tool known as SalesForce and the project idea can be simply summed up as a subset of SalesForce features that is open-source and extensible for use by hackathon organizers or anyone else who desires an open-source, free CRM tool.

## Team Members
    Ishan Khatri
    Cory Lanza
    Nick Williams
    Itamer Levy-Or
    Kevin Fredericks

## Data Model

![](imgs/data_model.jpg)

## Implemented Views
    We created views to create contacts, companies, emails, and users. We added full table views for contacts, companies, and emails. There is now a login, logout page that works as intended. All models are fully functional in the Django administration page, and have browser views for their creation.
    
    Relevant Urls:
    \contacts
    \companies
    \emails

## Problems/Successes
    One problem we encountered was an integration error with jinja, because when we converted our templates to jinja it interfered with our javascript that we had in the html templates themselves. This has caused some of our javascript to be non-functional, however it currently does not interfere with any of the functionality of our application. Our successes have put us ahead of the submission, since we now have a working user interface, with sign-up and login being fully functional. We also have browser views for creating, and editing our different models.

## Video
Check it out [here](https://youtu.be/p0cZxPLVxxg)!
