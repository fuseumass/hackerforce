# Team Name
Team Queue

# Application Name
[`Project`](https://github.com/326-queue/project/issues/1)

# Team Overview

| | Name | GitHub |
| ------------- | ------------- | ------------- |
| ![](https://avatars2.githubusercontent.com/u/6403666?s=60&v=4) | Ishan Khatri | [ikhatri](https://github.com/ikhatri) |
| ![]() | Kevin Fredericks | [kjfredericks](https://github.com/kjfredericks) |
| ![]() | Nicholas Williams| [nawilliams](https://github.com/nawilliams) |
| ![](https://avatars3.githubusercontent.com/u/24576321?s=60&v=4) | Cory Lanza | [corylanza](https://github.com/nawilliams) |
| ![]() | Itamar Levy-Or | [itamarlevyor](https://github.com/ItamarLevyOr) |

# Innovative Idea

`Project` is a tool created to help hackathon organizers manage their sponsorship leads and keep track of contacts, emails and more. Every year hackathon organizers need to contact hundreds of contacts who work at hundreds of companies to request sponsorship. The process for this usually involves various rounds of customized emails to various groupings of companies. This tool aims to create a user friendly interface to see the status of various companies, store the details of certain contacts and overall manage the information required for hackathon sponsorship.

Many aspects of the application are similar to the CRM tool known as SalesForce and the project idea can be simply summed up as a subset of SalesForce features that is open-source and extensible for use by hackathon organizers or anyone else who desires an open-source, free CRM tool.

# Important Data

There are 6 main data objects that the application needs to manage. Users, Hackathons, Companies, Sponsorships, Contacts, and Emails. These data objects will be specified below.

## Users
Users represent users of the tool. There need to be various permission sets for all of the users, and they should be able to edit their own basic settings such as their email, password, avatar and so on.

## Hackathons
Hackathons represent a hackathon event. If your event is annual, you would create a new hackathon object for each year. This object stores the following information:
* Fundraising goal
* Total funds raised till now
    * Some breakdowns & stats of this (which companies gave the most etc.)
* Fundraising deadline
* Hackathon event date
* Companies that sponsored
    * The tier level & perks/contract of a companies sponsorship of this particular event
    * The contacts who facilitated this event's sponsorship for the company
* PDF files of the various sponsorship packets for this year's event
* The sponsorship perks and tiers for this year's event (in a digital representation, picklist or something)

## Companies
Companies represent companies that can sponsor a hackathon. They should have fields that describe the following features:
* Their current status in the sponsorship pipeline
* Their size
* Their industry
* Their location
* A relational connection to all the contacts that work at this company

## Sponsorships
The sponsorship object is a relation between a company and a hackathon event. It represents the sponsorship of company A with a specific hackathon event (Hackathon 2017 for example). This object should include:
* The tier at which they've sponsored
* The amount of money that they paid for this tier
* The perks they recieved
* The contract as a PDF file
* The main point of contact for this sponsorship
* Any other contacts who were relevant to making this sponsorship happen

## Contacts
The contact object represents a person who works at a company and should have the following fields:
* Name
* Phone
* Email
* Warm or cold contact
* Position
* Company
* Sponsorships they've been involved in

## Emails
The email objects are slightly different from the others. For context a lot of hackathon sponsorships involve customized blast emailing contacts/companies depending on their sponsorship status and other factors. The email objects should be designed to handle this.

Each email should have the the following:
* A subject
* A body
* Attachments (optional)
    * These will be the 1 of the sponsorship packets that belong to a hackathon object
* A date & time at which it will be sent out (optional)
* Some kind of list/filter on companies or contacts that determines who it gets sent to

The idea with this is that a user should be able to perform any of the following example selections
* All warm contacts from companies who haven't sponsored a hackathon
* All contacts at companies in a particular stage of outreach for this hackathon
* All contacts involved in the finalized sponsorships for a this hackathon
* etc.

and then send an email with attachments to that selection at a scheduled date/time.

# User Interface

Provide a description and images of the user interface your
application will intend on supporting.

![example image](imgs/chick.jpg)
