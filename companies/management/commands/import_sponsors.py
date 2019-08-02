import csv
import os
import sys

from datetime import datetime

from companies.models import Company, Industry
from contacts.models import Contact

from django.core.management.base import BaseCommand
from django.db.models import Q

class Command(BaseCommand):
    help = "Import sponsor data from CSV."

    def add_arguments(self, parser):
        parser.add_argument('--pretend', action='store_true', dest='pretend', default=False)
        parser.add_argument('--csv', type=str, dest='csv_file', default='import.csv', help='Import CSV file')
        parser.add_argument('--dataset-name', type=str, dest='dataset_name', default='CSV', help='Name of dataset (e.g. HackUMass VI Sponsorship Tracking)')
        parser.add_argument('--dataset-event', type=str, dest='dataset_event', default='imported event', help='Name of event for this dataset (e.g. HackUMass VI). Will be used for importing archived information.')
    
    def ask(self, q):
        return input("{} [Yy]: ".format(q)).lower() == "y"

    def prompt(self, q):
        if not self.ask(q):
            self.abort("")
            
    def abort(self, msg):
        self.stdout.write(f"Abort. {msg}")
        sys.exit()
    
    def chk(self, q, test):
        if test:
            self.stdout.write(f"OK: {q}")
        else:
            self.abort(f"ERROR: {q}")
    
    def company_obj(self, name):
        name = name.strip()
        c = Company.objects.filter(name__icontains=name)
        if c.count() != 1:
            return None
        c = c.first()
        dist = abs(len(c.name) - len(name))
        if dist > 1 and dist < 5:
            if not self.ask(f"Are these companies the same?\nCSV company: {name}\nDB company:  {c.name}\n"):
                return None
        elif dist >= 5:
            return None
        
        return c

    def contact_obj(self, company_obj, name):
        name = name.strip()
        names = name.split(' ')
        q = Q()
        for a in names:
            for b in names:
                q = q | Q(first_name__icontains=a, last_name__icontains=b)
        c = company_obj.contacts.filter(q)
        if c.count() != 1:
            return None
        c = c.first()
        dist = abs(len(c.name()) - len(name))
        if dist > 1:
            if not self.ask(f"Are these names the same?\nCSV name: {name}\nDB name:  {c.name}\n"):
                return None

        return c
    
    pretend = True
    dataset_name = None
    dataset_event = None
    auto_industry = None

    def contact_note(self):
        date = datetime.now().date()
        return f"Contact imported from {self.dataset_name} on {date}<br />"
    
    def company_note(self, existing, only_notes=False):
        date = datetime.now().date()
        notes_or_company = "<br />Notes" if only_notes else "Company"
        s = f"{notes_or_company} imported from {self.dataset_name} on {date}<br />"
        if existing:
            s += f"Notes from {self.dataset_event}: {existing}"
        return s

    def add_contact(self, company_obj, cname, cemail):
        names = cname.split(" ")
        if self.pretend:
            print("Would create contact:", [names[0], " ".join(names[1:]), cemail, self.contact_note()])
            return
        Contact.objects.create(
            company=company_obj,
            first_name=names[0],
            last_name=" ".join(names[1:]),
            email=cemail,
            notes=self.contact_note())
    
    def add_company(self, company):
        name = company["Company Name"]
        notes = self.company_note(company["Notes"])
        if self.pretend:
            print("Would create company:", [name, "U", notes, self.auto_industry])
            return None
        c = Company.objects.create(
            name=name,
            size="U",
            notes=notes)
        c.industries.add(self.auto_industry)
        c.save()
        return c
    
    def handle(self, *args, **options):
        csv_file = options["csv_file"]
        self.pretend = options["pretend"]
        self.dataset_name = options["dataset_name"]
        self.dataset_event = options["dataset_event"]

        if self.pretend:
            print("In pretend mode, will not update database")

        companies = {}
        with open(csv_file, 'r') as csv_open:
            csv_reader = csv.reader(csv_open)
            next(csv_reader)
            rows = "Status,Company Name,Contact Name,Contact Email,Notes".split(",")
            for row in csv_reader:
                row_dict = {rows[i]: row[i].strip() for i in range(len(row))}
                companies[row_dict["Company Name"]] = row_dict
        
        print("Companies:", companies.keys())

        if not self.pretend:
            self.auto_industry = Industry.objects.get_or_create(name="Imported Data", color="yellow")[0]

        for name, company in companies.items():
            company_obj = self.company_obj(name)
            if company_obj:
                print("Company exists:", name, "\n", company_obj)
                company_exists = True
                notes = company["Notes"]
                if notes:
                    new_notes = self.company_note(notes, only_notes=True)
                    print("Existing notes:", company_obj.notes)
                    if new_notes in company_obj.notes:
                        print("Notes already exist! Not appending.")
                    else:
                        print("Appending company notes:", new_notes)
                        if not self.pretend:
                            company_obj.notes += new_notes
                            company_obj.save()

            else:
                print("New company:", name)
                company_obj = self.add_company(company)
                company_exists = False
            contact_names = company["Contact Name"].splitlines()
            contact_emails = company["Contact Email"].splitlines()
            for cname, cemail in zip(contact_names, contact_emails):
                cobj = self.contact_obj(company_obj, cname) if company_exists else None
                if cobj:
                    print("\tContact exists:", cname, cemail, "\nDB match:", cobj, cobj.email if cobj else None)
                else:
                    print("\tAdding new contact", cname, cemail)
                    self.add_contact(company_obj, cname, cemail)
            print("="*100)
            