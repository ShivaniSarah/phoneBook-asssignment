from core.views import RegisterView, LoginView, ProfileView, SpamMarkView
from core.views import SearchByNameView, SearchByPhoneView
from django.urls import path

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('spam/mark/', SpamMarkView.as_view()),
    path('search/name/', SearchByNameView.as_view()),
    path('search/phone/', SearchByPhoneView.as_view()),
]
