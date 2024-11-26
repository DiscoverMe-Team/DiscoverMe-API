from django.contrib import admin
from .models import Goal, Insight, JournalEntry, Mood, MoodLog, Suggestion

admin.site.register(JournalEntry)
admin.site.register(MoodLog)
admin.site.register(Mood)
admin.site.register(Insight)
admin.site.register(Goal)
admin.site.register(Suggestion) 
