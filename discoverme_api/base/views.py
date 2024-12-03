from rest_framework import viewsets, status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from .models import Mood, MoodLog, JournalEntry, Suggestion, Goal, Insight, Task, UserProfile
from .serializers import (
    MoodSerializer, MoodLogSerializer, JournalEntrySerializer, 
    SuggestionSerializer, GoalSerializer, InsightSerializer, UserProfileSerializer,
    TaskSerializer
)


class MoodViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Mood objects.
    """
    serializer_class = MoodSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Mood.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class MoodLogViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing MoodLog objects.
    """
    serializer_class = MoodLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MoodLog.objects.filter(user=self.request.user).order_by('-date_logged')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class JournalEntryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing JournalEntry objects.
    """
    serializer_class = JournalEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SuggestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Suggestion objects.
    """
    serializer_class = SuggestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_moods = MoodLog.objects.filter(user=self.request.user).values_list('mood__mood_type', flat=True)
        return Suggestion.objects.filter(mood_trigger__in=user_moods)


class GoalViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Goal objects.

    """
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except Exception as e:
            print("Error in GoalViewSet.perform_create:", e)  # Debugging
            raise e


class InsightViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Insight objects.
    """
    serializer_class = InsightSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Insight.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserProfileView(RetrieveUpdateAPIView):
    """
    API endpoint for retrieving or updating the user's profile.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Task objects.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve tasks associated with the authenticated user's goals.
        """
        return Task.objects.filter(goal__user=self.request.user)

    def perform_create(self, serializer):
        """
        Save the task to the goal owned by the authenticated user.
        """
        goal_id = self.request.data.get('goal')
        try:
            goal = Goal.objects.get(id=goal_id, user=self.request.user)
            serializer.save(goal=goal)
        except Goal.DoesNotExist:
            raise ValidationError({'error': 'Goal not found or does not belong to the user.'})


@csrf_exempt
@api_view(['POST'])
def register_user(request):
    """
    API endpoint for user registration.

    Method: POST
    """
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

    # Generate JWT tokens for the user
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    return Response({
        'message': 'User registered successfully.',
        'access': str(access),
        'refresh': str(refresh)
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    """
    API endpoint to retrieve detailed information about the authenticated user.

    Method: GET
    """
    user = request.user
    profile = user.profile  # Assuming a OneToOneField relation to UserProfile

    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'occupation': profile.occupation,  # From UserProfile
        'city': profile.city,              # From UserProfile
        'state': profile.state,            # From UserProfile
        'pronouns': profile.pronouns,      # From UserProfile
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    API endpoint for authenticated users to change their password.

    Method: POST
    """
    user = request.user
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')

    # Validate that both fields are provided
    if not current_password or not new_password:
        return Response({'error': 'Both current and new passwords are required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the current password is correct
    if not user.check_password(current_password):
        return Response({'error': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

    # Validate the new password
    try:
        validate_password(new_password, user=user)
    except ValidationError as e:
        return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)

    # Update the password
    user.set_password(new_password)
    user.save()
    return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_details(request):
    """
    API endpoint to update user details (except username).
    Method: PUT
    """
    user = request.user
    profile = user.profile

    # Data from the request
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    email = request.data.get('email')
    occupation = request.data.get('occupation')
    city = request.data.get('city')
    state = request.data.get('state')
    pronouns = request.data.get('pronouns')

    # Validate email
    if email and User.objects.exclude(pk=user.pk).filter(email=email).exists():
        return Response({'error': 'This email is already in use.'}, status=status.HTTP_400_BAD_REQUEST)

    # Update User fields
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if email:
        user.email = email

    # Update UserProfile fields
    if occupation:
        profile.occupation = occupation
    if city:
        profile.city = city
    if state:
        profile.state = state
    if pronouns:
        profile.pronouns = pronouns
    user.save()
    profile.save()

    return Response({'message': 'User details updated successfully.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def check_email(request):
    email = request.data.get('email')
    is_available = not User.objects.filter(email=email).exists()
    return Response({'isAvailable': is_available})
