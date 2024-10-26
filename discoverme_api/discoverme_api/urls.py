from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from base import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
router = DefaultRouter()
router.register(r'moodlogs', views.MoodLogViewSet, basename='moodlog')
router.register(r'journalentries', views.JournalEntryViewSet, basename='journalentry')
router.register(r'suggestions', views.SuggestionViewSet, basename='suggestion')
router.register(r'goals', views.GoalViewSet, basename='goal')


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    
]
