# HackerForce

## Team Queue - Fall 2018

**Cory Lanza, Ishan Khatri, Kevin Fredericks, Nicholas Williams**

## Overview

## User Interface

### Base Templates

**menu.html.j2**

Navigation bar for moving around the site, available on all pages. Also shows the current logged in user.

![menu](imgs/final/menu.png)

**footer.html.j2**

Footer available on all pages. Contains miscellaneous links.

![footer](imgs/final/footer.png)

**404.html.j2**

404 page for urls that aren't mapped.

![404](imgs/final/404.png)

### Dashboard

**dashboard.html.j2**

Home page that contains stats for your current hackathon (funding, sponsorships, company information) and links for hackathons and sponsorships.

![dashboard](imgs/final/dashboard.png)

### Login/Signup

**login.html.j2**

Basic login page.

![login](imgs/final/login.png)

**register.html.j2**

Basic registration page.

![register](imgs/final/register.png)

**After Registration**

After registering you're redirected back to the login page with the below popup.

![registered](imgs/final/registered.png)

**activation.html.j2**

This email is sent to you after you register so that you can confirm your registration.

![activation](imgs/final/login_activation.png)

**After Activation**

After clicking the link in the email you're redirected to the login page with the below popup.

![activated](imgs/final/login_activated.png)

### Profiles

**profile_edit.html.j2**

Page for editing your profile information.

![profile_edit](imgs/final/profile_edit.png)

**settings.html.j2**

Old static page that we didn't have time to revamp, but is still reachable. This would normally hold account settings like email preferences.

![profile_settings](imgs/final/profile_settings.png)

### Hackathons

**hackathons.html.j2**

Hackathon show page that lists all hackathons. Contains links to create new hackathons, tiers and perks. Also has links to each edit page and clicking on a tier or perk links to the respective edit page.

![hackathons](imgs/final/hackathons.png)

**hackathon_new.html.j2**

Form for creating a new hackathon.

![hackathon_new](imgs/final/hackathon_new.png)

**hackathon_edit.html.j2**

Form for editing an existing hackathon.

![hackathon_edit](imgs/final/hackathon_edit.png)

**sponsorships.html.j2**

Sponsorship show page containing links to edit each sponsorship (rightmost icon in the table).

![sponsorships](imgs/final/sponsorships.png)

**sponsorship_new.html.j2**

Form for creating a new sponsorship.

![sponsorship_new](imgs/final/sponsorship_new.png)

**sponsorship_edit.html.j2**

Form for editing an existing sponsorship.

![sponsorship_edit](imgs/final/sponsorship_edit.png)

**tier_new.html.j2**

Form for creating a new tier.

![tier_new](imgs/final/tier_new.png)

**tier_edit.html.j2**

For for editing an existing tier.

![tier_edit](imgs/final/tier_edit.png)

**perk_new.html.j2**

Form for creating a new perk.

![perk_new](imgs/final/perk_new.png)

**perk_edit.html.j2**

Form for editing an existing perk.

![perk_edit](imgs/final/perk_edit.png)

### Companies

**companies.html.j2**

Company show page that contains links to respective edit pages, and a link to create a new company.

![companies](imgs/final/companies.png)

**company_new.html.j2**

Form for creating a new company.

![company_new](imgs/final/company_new.png)

**company_edit.html.j2**

Form for editing an existing company.

![company_edit](imgs/final/company_edit.png)

### Contacts

**contacts.html.j2**

Contact show page that contains links to each respective edit page (scroll to the right in the table) and a link for creating new contacts.

![contacts](imgs/final/contacts.png)

**contact_new.html.j2**

Form for creating new contacts.

![contact_new](imgs/final/contact_new.png)

**contact_edit.html.j2**

Form for editing existing contacts.

![contact_edit](imgs/final/contact_edit.png)

### Emails

**emails.html.j2**

Page for creating and scheduling a new email.

![emails](imgs/final/emails.png)

**drafts.html.j2**

Show page for email drafts (unscheduled).

![drafts](imgs/final/email_drafts.png)

**outbox.html.j2**

Show page for scheduled but unsent emails.

![outbox](imgs/final/email_outbox.png)

**sent.html.j2**

Show page for emails that have already been sent.

![sent](imgs/final/email_sent.png)

**emails_edit.html.j2**

Edit page for scheduled but unsent emails.

![email_edit](imgs/final/email_edit.png)

**sent_view.html.j2**

Show page for emails that have already been sent.

![sent_view](imgs/final/email_sent_view.png)

## Data Model

## URL Routes

### Dashboard

**/** -> *dashboard.html.j2*

Routes to the dashboard page. It loads the hackathon it displayed based on the logged in user and their profile settings. Additionally the menu bar displays the current user's name with a dropdown only accessable if one is logged in, otherwise it shows a login button.

**404/** -> *404.html.j2*

404 for pages/routes that don't exist.

### Login/Signup

**login/** -> *login.html.j2*

Routes to the login page. Available to unauthenticated users. Additionally unauthenticated users are redirected to this page if they try access any page other than login/register/404.

**register/** -> *register.html.j2*

Routes to the registration page. Available to unauthenticated users. Additionally this view sends an authorization email to the user upon post.

**logout/** -> *login.html.j2*

Logs out current user and directs to login page.

### Profiles

**settings/** -> *settings.html.j2*

Routes to statis settings page.

**settings/edit** -> *profile_edit.html.j2*

Routes to profile edit page. Content depends on logged in user and is pulled from the user model.

### Hackathons

**hackathons/** -> *hackathons.html.j2*

Route to hackathons show page.

**hackathons/new** -> *hackathon_new.html.j2*

Route to hackathon creation page.

**hackathons/\<id\>/edit** -> *hackathon_edit.html.j2*

Route to hackathon edit page.

**hackathons/\<id\>sponsorships** -> *sponsorships.html.j2*

Route to sponsorships show page, for a given hackathon.

**hackathons/sponsorships/new** -> *sponsorship_new.html.j2*

Route to sponsorship creation page.

**hackathons/sponsorships/\<id\>/edit** -> *sponsorship_edit.html.j2*

Route to sponsorship edit page.

**hackathons/tiers/new** -> *tier_new.html.j2*

Route to tier creation page.

**hackathons/tiers/\<id\>/edit** -> *tier_edit.html.j2*

Route to tier edit page.

**hackathons/perks/new** -> *perk_new.html.j2*

Route to perk creation page.

**hackathons/perks/\<id\>/edit** -> *perk_edit.html.j2*

Route to perk edit page.

### Companies

**companies/** -> *companies.html.j2*

Route to companies show page.

**companies/new** -> *company_new.html.j2*

Route to company creation page.

**companies/\<id\>/edit** -> *company_edit.html.j2*

Route to company edit page.

### Contacts

**contacts/** -> *contacts.html.j2*

Route to contacts show page.

**contacts/new** -> *contact_new.html.j2*

Route to contact creation page.

**contacts/\<id\>/edit** -> *contact_edit.html.j2*

Route to contact edit page.

### Emails

**emails/** -> *emails.html.j2*

Route to email creation/scheduling page. When an email is created the person who created it is set to the current user.

**emails/drafts** -> *drafts.html.j2*

Route to email drafts show page.

**emails/outbox** -> *outbox.html.j2*

Route to email outbox show page.

**emails/sent** -> *sent.html.j2*

Route to sent emails show page.

**emails/\<id\>/edit** -> *emails_edit.html.j2*

Route to email editing page.

**emails/\<id\>/sent_view** -> *sent_view.html.j2*

Route to already sent email show page.


## Authentication

## Team Choice

## Conclusion
