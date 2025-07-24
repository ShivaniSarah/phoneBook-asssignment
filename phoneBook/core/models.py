from django.db import models
import uuid
from django.utils import timezone
from django.contrib.postgres.indexes import GinIndex
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# -------------------- Custom User Manager --------------------
class UserManager(BaseUserManager):
    def create_user(self, phone_number, name, password=None, email=None):
        if not phone_number or not name:
            raise ValueError("Name and phone number are required.")
        user = self.model(phone_number=phone_number, name=name, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user


# -------------------- User Model --------------------
class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=15, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    class Meta:
        indexes = [
            models.Index(fields=['phone_number']),
            models.Index(name='idx_user_name_prefix', fields=['name']),
            GinIndex(name='idx_user_name_trgm', fields=['name'], opclasses=['gin_trgm_ops']),
        ]

    def __str__(self):
        return f"{self.name} ({self.phone_number})"


# -------------------- Contact Model --------------------
class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts', db_index=True)
    contact_phone = models.CharField(max_length=15)
    contact_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'contact_phone')
        indexes = [
            models.Index(fields=['contact_phone']),
            models.Index(name='idx_contact_name_prefix', fields=['contact_name']),
            GinIndex(name='idx_contact_name_trgm', fields=['contact_name'], opclasses=['gin_trgm_ops']),
        ]

    def __str__(self):
        return f"{self.contact_name} ({self.contact_phone})"


# -------------------- Spam Report Model --------------------
class SpamReport(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    target_phone = models.CharField(max_length=15, db_index=True)
    reported_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('reporter', 'target_phone')
        indexes = [
            models.Index(fields=['target_phone']),
        ]

    def __str__(self):
        return f"{self.target_phone} reported by {self.reporter}"


# -------------------- Spam Stats Model --------------------
class SpamStats(models.Model):
    target_phone = models.CharField(max_length=15, primary_key=True)
    report_count = models.IntegerField(default=0)
    last_reported_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.target_phone}: {self.report_count} spam reports"


# -------------------- Auth Token Model --------------------
class AuthToken(models.Model):
    token = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"Token for {self.user.phone_number}"
