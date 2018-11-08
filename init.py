import random
import pytz
from faker import Faker

from profiles.models import User
from contacts.models import Contact
from companies.models import Company, Industry
from emails.models import Email

fake = Faker()

print("Generating users...")
users = []
for i in range(10):
    username = fake.user_name()
    user = User(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        username=username,
        password=username,
    )
    user.save()
    users.append(user)

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
        updated=fake.date_time_this_month(
            before_now=True, after_now=False, tzinfo=None
        ),
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

print("Generating emails...")
emails = []
for i in range(100):
    status = random.choice(["sent", "scheduled", "draft"])
    email = Email(
        subject=fake.sentences(nb=1, ext_word_list=None)[0],
        body=fake.text(max_nb_chars=200, ext_word_list=None),
        status=status,
        created_by=random.choice(users),
    )
    if status == "scheduled":
        email.time_scheduled = fake.date_time_this_month(
            before_now=False, after_now=True, tzinfo=pytz.UTC
        )
    elif status == "sent":
        email.time_sent = fake.date_time_this_month(
            before_now=True, after_now=False, tzinfo=pytz.UTC
        )
    email.save()
    emails.append(email)

print("\nUsers:")
for a in users:
    print(a)

print("\nContacts:")
for a in industries:
    print(a)

print("\nCompanies:")
for a in companies:
    print(a)

print("\nContacts:")
for a in contacts:
    print(a)

# ADMIN USER
adminuser = User.objects.create_user("admin", "admin@326.edu", "admin")
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
