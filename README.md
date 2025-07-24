# 📱 PhoneBook Assignment

A Django-based REST API backend for a mobile app that helps users identify spam callers and search contacts by name or phone number — inspired by apps like Truecaller.

---

## 📦 Overview

This backend system enables:

- ✅ User Registration & JWT Authentication  
- 🔎 Global Contact Search (by name or phone number)  
- 🚨 Spam Reporting on phone numbers  
- 🔐 Conditional Access to Emails (based on contact relationship)  

Contacts may be either:
- Registered users, or  
- Unregistered entries pulled from users' contact books.

Spam likelihood is determined through community reporting and auto-managed using PostgreSQL triggers.

---

## 🏗️ Project Structure

```
phoneBook-assignment/
├── manage.py
├── phoneBook/           # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── core/                # App with models, logic, views
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── tests/
│       └── test_views.py
├── populate_data.py     # Sample data loader
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## 🚀 Getting Started

### 📦 1. Setup Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 🔧 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install django djangorestframework psycopg2-binary
pip install pytest pytest-django
pip install djangorestframework-simplejwt django-cors-headers
```

---

### 🗄️ 3. Database Setup

Requires PostgreSQL.

```bash
# Install PostgreSQL (on macOS)
brew install postgresql
brew services start postgresql

# Create superuser
createuser -s postgres
psql -U postgres
```

---

### 🧱 4. Run Migrations

```bash
python manage.py makemigrations core
python manage.py makemigrations core --empty --name enable_pg_trgm
python manage.py makemigrations core --empty --name add_spam_trigger
python manage.py migrate
```

---

### 📥 5. Load Sample Data

```bash
python manage.py shell < populate_data.py
```

---

### 🧪 6. Running Tests

Make sure `pytest` is installed and `pytest.ini` exists with:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = phoneBook.settings
python_files = tests.py test_*.py *_tests.py
```

Then run:

```bash
pytest core/tests/
```

---

### ⚙️ 7. Run the Development Server

```bash
python manage.py runserver
```

---

## 📡 API Endpoints & Curl Examples

🔐 **Register User**
```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Rahul Kapoor",
        "phone_number": "+919999999999",
        "password": "securepass",
        "email": "rahul@example.com"
      }'
```

🔍 **Search by Phone Number**
```bash
curl -X GET "http://127.0.0.1:8000/api/search/phone/?q=+919999999999" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json"
```

🔍 **Search by Name**
```bash
curl -X GET "http://127.0.0.1:8000/api/search/name/?q=Rahul" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json"
```

🚨 **Mark a Number as Spam**
```bash
curl -X POST http://127.0.0.1:8000/api/spam/mark/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"target_phone": "+919999999999"}'
```

---

## 🔐 Authentication

- Use auth tokens from the samples created in core_authtoken table using populate_data file
- All sensitive endpoints require the `Authorization: Bearer <token>` header

---

## Commands ran

phoneBook Hey there!

python3 -m venv venv 
source venv/bin/activate 
deactivate
pip3 install django djangorestframework 
pip3 install djangorestframework-simplejwt django-cors-headers 
django-admin startproject phoneBook 
cd phoneBook 
python3 manage.py startapp core 
pip3 install psycopg2-binary 
brew install postgresql 
brew services start 
postgresql createuser -s postgres psql -U postgres 
\l 
\c 
postgres 
\dt 
TRUNCATE TABLE core_user CASCADE; 
exit 
cd /Users/shivaniagrawal/PycharmProjects/phoneBook-asssignment/phoneBook 
python3 manage.py makemigrations core 
python3 manage.py makemigrations core --empty --name add_spam_trigger 
python3 manage.py makemigrations core --empty --name enable_pg_trgm 
python3 manage.py migrate 
python3 manage.py inspectdb 
python3 manage.py shell < populate_data.py 
pip3 install pytest 
pip3 install pytest-django 
pip3 freeze > requirements.txt
cd /Users/shivaniagrawal/PycharmProjects/phoneBook-asssignment/phoneBook 
pytest core/tests/test_views.py 
python3 manage.py runserver




------

## 📬 Contact

Shivani Agrawal

[ganpshiva@gmail.com]


---

## 🧾 License

MIT License — use it freely, just don’t spam! 😄
