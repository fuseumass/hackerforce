from contacts.models import Contact
from faker import Faker

fake = Faker()

print("Generating contacts...")
contacts = []
for i in range(20):
    contact = Contact(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        company=fake.company(),
        position=fake.job(),
        email=fake.email(),
        phone_number=fake.phone_number(),
        is_warm_contact=fake.boolean(),
    )
    contact.save()
    contacts.append(contact)

print("\nContact:")
for a in Contact.objects.all():
    print(a)

