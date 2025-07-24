import random
import string
import uuid
from datetime import timedelta
from django.utils import timezone
from core.models import User, Contact, SpamReport, SpamStats, AuthToken
from django.contrib.auth import get_user_model

UserModel = get_user_model()

NUM_USERS = 50
CONTACTS_PER_USER = 10
NUM_SPAM_REPORTS = 50
NUM_TOKENS = 5

# -------------------- Helpers --------------------
def random_phone():
    return "+91" + ''.join(random.choices(string.digits, k=10))

def random_name():
    return random.choice(['Aman', 'Riya', 'Vikram', 'Neha', 'Rahul', 'Divya', 'Kabir']) + \
           random.choice([' Singh', ' Sharma', ' Kumar', ' Kapoor', ' Raj'])

def random_email(name):
    return name.replace(' ', '').lower() + str(random.randint(10, 99)) + "@example.com"


# -------------------- Create Users --------------------
print("Creating users...")
users = []
for _ in range(NUM_USERS):
    name = random_name()
    phone = random_phone()
    email = random_email(name)
    try:
        user = UserModel.objects.create_user(name=name, phone_number=phone, email=email, password="password")
        users.append(user)
    except:
        pass  # Skip duplicates

# -------------------- Create Contacts --------------------
print("Creating contacts...")
for user in users:
    for _ in range(CONTACTS_PER_USER):
        contact_phone = random_phone()
        contact_name = random_name()
        if contact_phone != user.phone_number:
            Contact.objects.get_or_create(
                user=user,
                contact_phone=contact_phone,
                defaults={'contact_name': contact_name}
            )

# -------------------- Create Spam Reports --------------------
print("Creating spam reports...")
# Get all users or a subset to act as reporters
reporters = User.objects.order_by('?')[:NUM_SPAM_REPORTS]
for reporter in reporters:
    target_phone = random_phone()
    try:
        SpamReport.objects.create(
            reporter=reporter,
            target_phone=target_phone
        )
    except:
        pass  # Ignore duplicates

# -------------------- Create Auth Tokens --------------------
print("Generating auth tokens...")
token_users = random.sample(users, k=min(len(users), NUM_TOKENS))
for user in token_users:
    AuthToken.objects.create(
        token=uuid.uuid4(),
        user=user,
        created_at=timezone.now(),
        expires_at=timezone.now() + timedelta(days=7)
    )

print("Dummy data inserted successfully!")
