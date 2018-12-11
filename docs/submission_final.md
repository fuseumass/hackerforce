#HackerForce

##Team Queue - Fall 2018

**Cory Lanza, Ishan Khatri, Kevin Fredericks, Nicholas Williams**

##Overview

##User Interface

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

###Profiles

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

##Data Model

##URL Routes

##Authentication

##Team Choice

##Conclusion
