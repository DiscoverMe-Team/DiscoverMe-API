from django.contrib import admin
from .models import Goal, Insight, JournalEntry, Mood, MoodLog, Suggestion

admin.site.register(JournalEntry) #added by Zachary
admin.site.register(MoodLog)
admin.site.register(Mood)
admin.site.register(Insight) #added by Anisa
admin.site.register(Goal) #added by Anisa
admin.site.register(Suggestion) #added by Anisa
