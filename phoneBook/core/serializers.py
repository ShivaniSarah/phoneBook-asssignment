
from core.models import User, AuthToken
from django.utils import timezone
from datetime import timedelta
from core.models import SpamReport
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'phone_number', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        phone = data['phone_number']
        password = data['password']
        from django.contrib.auth import authenticate
        user = authenticate(phone_number=phone, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        # Create and return AuthToken
        token = AuthToken.objects.create(
            user=user,
            expires_at=timezone.now() + timedelta(days=7)
        )
        return {'token': str(token.token), 'user_id': user.id, 'name': user.name}

class SpamReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpamReport
        fields = ['target_phone']




class SearchResultSerializer(serializers.Serializer):
    name = serializers.CharField()
    phone_number = serializers.CharField()
    is_registered_user = serializers.BooleanField()
    spam_report_count = serializers.IntegerField()
    show_email = serializers.BooleanField()
    email = serializers.CharField(allow_null=True)

