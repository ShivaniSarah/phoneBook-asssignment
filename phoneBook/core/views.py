import re

from core.models import SpamReport, AuthToken, User, SpamStats, Contact
from core.serializers import (
    RegistrationSerializer,
    LoginSerializer,
    SearchResultSerializer,
    SpamReportSerializer
)
from core.validators import Validator
from django.contrib.postgres.search import TrigramSimilarity
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


def get_authenticated_user(request):
    auth = request.headers.get('Authorization')
    if not auth or not auth.startswith('Bearer '):
        return None
    token_value = auth.split(' ')[1]
    try:
        token = AuthToken.objects.get(token=token_value, expires_at__gt=timezone.now())
        return token.user
    except AuthToken.DoesNotExist:
        return None


class RegisterView(APIView):
    def post(self, request):
        data = request.data.copy()
        phone = data.get('phone_number', '').strip()
        email = data.get('email', None)

        if not Validator.validate_phone(phone):
            return Response({"error": "Invalid phone number format. Use +91XXXXXXXXXX."},
                            status=status.HTTP_400_BAD_REQUEST)

        if email and not Validator.validate_email_format(email):
            return Response({"error": "Invalid email format."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = RegistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class ProfileView(APIView):
    def get(self, request):
        user = get_authenticated_user(request)
        if not user:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            "name": user.name,
            "phone_number": user.phone_number,
            "email": user.email
        })


class SpamMarkView(APIView):
    def post(self, request):
        user = get_authenticated_user(request)
        if not user:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = SpamReportSerializer(data=request.data)
        if serializer.is_valid():
            target_phone = serializer.validated_data['target_phone']

            if not Validator.validate_phone(target_phone):
                return Response({"error": "Invalid phone number format. Use +91XXXXXXXXXX."},
                                status=status.HTTP_400_BAD_REQUEST)

            if SpamReport.objects.filter(reporter=user, target_phone=target_phone).exists():
                return Response({"message": "Already marked as spam"}, status=status.HTTP_200_OK)

            SpamReport.objects.create(
                reporter=user,
                target_phone=target_phone,
                reported_at=timezone.now()
            )

            return Response({"message": f"{target_phone} marked as spam"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchByNameView(APIView):
    def get(self, request):
        user = get_authenticated_user(request)
        if not user:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        query = request.query_params.get('q', '').strip()
        if not query:
            return Response({"error": "Missing search query"}, status=status.HTTP_400_BAD_REQUEST)

        starts_with = User.objects.filter(name__istartswith=query)
        contains_fuzzy = (
            User.objects
            .annotate(similarity=TrigramSimilarity('name', query))
            .filter(similarity__gt=0.3)
            .exclude(id__in=starts_with.values_list('id', flat=True))
            .order_by('-similarity')
        )

        all_results = list(starts_with) + list(contains_fuzzy)
        data = []

        for result in all_results:
            spam_stats = SpamStats.objects.filter(target_phone=result.phone_number).first()
            report_count = spam_stats.report_count if spam_stats else 0
            is_contact = Contact.objects.filter(user=result, contact_phone=user.phone_number).exists()
            email_visible = is_contact

            data.append({
                "name": result.name,
                "phone_number": result.phone_number,
                "is_registered_user": True,
                "spam_report_count": report_count,
                "email": result.email if email_visible else None,
                "show_email": email_visible
            })

        return Response(SearchResultSerializer(data, many=True).data)


class SearchByPhoneView(APIView):
    def get(self, request):
        user = get_authenticated_user(request)
        if not user:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        phone = request.query_params.get('q', '').strip()
        if not phone:
            return Response({"error": "Missing phone number"}, status=status.HTTP_400_BAD_REQUEST)

        phone = Validator.normalize_phone(phone)
        if not Validator.validate_phone(phone):
            return Response({"error": "Invalid phone number format. Use +91XXXXXXXXXX."},
                            status=status.HTTP_400_BAD_REQUEST)

        results = []

        registered_user = User.objects.filter(phone_number=phone).first()
        if registered_user:
            spam_stats = SpamStats.objects.filter(target_phone=phone).first()
            report_count = spam_stats.report_count if spam_stats else 0

            is_contact = Contact.objects.filter(user=registered_user, contact_phone=user.phone_number).exists()
            email_visible = is_contact

            results.append({
                "name": registered_user.name,
                "phone_number": registered_user.phone_number,
                "is_registered_user": True,
                "spam_report_count": report_count,
                "email": registered_user.email if email_visible else None,
                "show_email": email_visible
            })

            return Response(SearchResultSerializer(results, many=True).data)

        contacts = Contact.objects.filter(contact_phone=phone)
        for c in contacts:
            spam_stats = SpamStats.objects.filter(target_phone=phone).first()
            report_count = spam_stats.report_count if spam_stats else 0

            results.append({
                "name": c.contact_name,
                "phone_number": c.contact_phone,
                "is_registered_user": False,
                "spam_report_count": report_count,
                "email": None,
                "show_email": False
            })

        return Response(SearchResultSerializer(results, many=True).data)
