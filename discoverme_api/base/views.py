from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view,  permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from .models import Mood, MoodLog, JournalEntry, Suggestion, Goal, Insight
from .serializers import MoodSerializer, MoodLogSerializer, JournalEntrySerializer, SuggestionSerializer, GoalSerializer, InsightSerializer
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt

class MoodViewSet(viewsets.ModelViewSet):
    serializer_class = MoodSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Mood.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()
        

class MoodLogViewSet(viewsets.ModelViewSet):
    serializer_class = MoodLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return mood logs for the authenticated user
        return MoodLog.objects.filter(user=self.request.user).order_by('-date_logged')

    def perform_create(self, serializer):
        # Automatically associate the created mood log with the logged-in user
        serializer.save(user=self.request.user)

class JournalEntryViewSet(viewsets.ModelViewSet):
    serializer_class = JournalEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return journal entries for the authenticated user
        return JournalEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically associate the created journal entry with the logged-in user
        serializer.save(user=self.request.user)

class SuggestionViewSet(viewsets.ModelViewSet):
    serializer_class = SuggestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_moods = MoodLog.objects.filter(user=self.request.user).values_list('mood', flat=True)
        return Suggestion.objects.filter(mood_trigger__in=user_moods)

class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class InsightViewSet(viewsets.ModelViewSet):
    serializer_class = InsightSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Insight.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@csrf_exempt
@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        validate_password(password)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already registered.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    })