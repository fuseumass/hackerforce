import random
from faker import Faker

from profiles.models import User
from contacts.models import Contact
from companies.models import Company, Industry

fake = Faker()

print("Generating industries...")
industries = []
colors = {
    "Web Dev": "blue",
    "ML": "green",
    "Software": "purple",
    "Systems": "orange",
    "Data": "yellow",
}
for t in colors.keys():
    industry = Industry(name=t, color=colors[t])
    industry.save()
    industries.append(industry)

print("Generating companies...")
companies = []
statuses = ["U", "C", "D"]
sizes = ["L", "M", "S"]
for i in range(10):
    company = Company(
        name=fake.company(),
        location=fake.address(),
        status=random.choice(statuses),
        size=random.choice(sizes),
        donated=random.randint(0, 10000),
        updated=fake.date_this_year(before_today=True, after_today=False),
    )
    company.save()
    for s in random.sample(industries, random.randint(1, 3)):
        company.industries.add(s)
    company.save()
    companies.append(company)


print("Generating contacts...")
contacts = []
for i in range(20):
    contact = Contact(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        company=random.choice(companies),
        position=fake.job(),
        email=fake.email(),
        phone_number=fake.phone_number(),
        is_warm_contact=fake.boolean(),
    )
    contact.save()
    contacts.append(contact)

print("\nContacts:")
for a in Industry.objects.all():
    print(a)

print("\nCompanies:")
for a in Company.objects.all():
    print(a)

print("\nContacts:")
for a in Contact.objects.all():
    print(a)

username = "admin"
password = "admin"
email = "admin@326.edu"

adminuser = User.objects.create_user(username, email, password)
adminuser.save()
adminuser.is_superuser = True
adminuser.is_staff = True
adminuser.save()

print(
    """
The database has been setup with the following credentials:
  username: {username}
  password: {password}
  email: {email}
  """
)
