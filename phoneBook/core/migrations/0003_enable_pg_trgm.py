from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_add_spam_trigger'),
    ]

    operations = [
        migrations.RunSQL("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
    ]
