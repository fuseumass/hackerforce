import random
import pytz
from faker import Faker

from profiles.models import User
from contacts.models import Contact
from companies.models import Company, Industry
from emails.models import Email
from hackathons.models import Hackathon, Tier, Perk, Sponsorship, Lead

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
    )
    user.save()
    user.set_password(username)
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
for i in range(50):
    company = Company(
        name=fake.company(),
        location=fake.address(),
        size=random.choice(Company.SIZES)[0],
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
for i in range(150):
    contact = Contact(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        company=random.choice(companies),
        position=fake.job(),
        primary=bool(random.getrandbits(1)),
        email=fake.email(),
        phone_number=fake.phone_number(),
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

print("Generating hackathons...")
hackathons = []
for i in range(3):
    hackathon = Hackathon(
        name="Hack " + fake.state(),
        date=fake.future_date(end_date="+30d", tzinfo=None),
        fundraising_goal=random.randint(5000, 20000),
    )
    hackathon.save()
    hackathons.append(hackathon)

print("Generating tiers...")
tiers = []
for i in range(10):
    tier = Tier(name=fake.color_name(), hackathon=random.choice(hackathons))
    tier.save()
    tiers.append(tier)

print("Generating perks...")
perks = []
for i in range(20):
    perk = Perk(
        name=fake.currency_name(),
        description=fake.text(max_nb_chars=200, ext_word_list=None),
        hackathon=random.choice(hackathons),
    )
    perk.save()
    perks.append(perk)

print("Generating sponsorships...")
sponsorships = []
for c in companies:
    sponsorship = Sponsorship(
        hackathon=random.choice(hackathons),
        company=c,
        tier=random.choice(tiers),
        contribution=random.randint(0, 1000),
        status=random.choice(Sponsorship.STATUSES)[0],
    )
    sponsorship.save()
    for s in random.sample(perks, random.randint(1, 5)):
        sponsorship.perks.add(s)
    sponsorship.save()
    sponsorships.append(sponsorship)

print("Generating leads...")
leads = []
for s in sponsorships:
    contacts = s.company.contacts.all()
    if contacts:
        lead = Lead(
            sponsorship=s,
            contact=random.choice(contacts),
            status=random.choice(Lead.STATUSES)[0],
            role=random.choice(Lead.ROLES)[0],
        )
        lead.save()
        leads.append(lead)


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

print("\nHackathons:")
for a in hackathons:
    print(a)

print("\nTiers:")
for a in tiers:
    print(a)

print("\nPerks:")
for a in perks:
    print(a)

print("\nSponsorships:")
for a in sponsorships:
    print(a)

print("\nLeads:")
for a in leads:
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
  username: admin
  password: admin
  email: admin@326.edu
  """
)
