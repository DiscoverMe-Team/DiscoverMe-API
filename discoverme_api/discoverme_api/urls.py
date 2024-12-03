from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.shortcuts import redirect
from base import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Initialize DefaultRouter
router = DefaultRouter()
router.register(r'mood', views.MoodViewSet, basename='mood')
router.register(r'moodlogs', views.MoodLogViewSet, basename='moodlog')
router.register(r'journalentries', views.JournalEntryViewSet, basename='journalentry')
router.register(r'suggestions', views.SuggestionViewSet, basename='suggestion')
router.register(r'goals', views.GoalViewSet, basename='goal')
router.register(r'insights', views.InsightViewSet, basename='insight')
router.register(r'tasks', views.TaskViewSet, basename='task')  # Add the TaskViewSet

# Define URL patterns
urlpatterns = [
    path('', lambda request: redirect('admin/', permanent=True)),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Include router-generated URLs
    path('api/register/', views.register_user, name='register_user'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user-info/', views.get_user_info, name='user_info'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('api/auth/change-password/', views.change_password, name='change_password'),
    path('api/auth/update-user/', views.update_user_details, name='update_user_details'),
    path('api/auth/check-email/', views.check_email, name='check_email'),
]
