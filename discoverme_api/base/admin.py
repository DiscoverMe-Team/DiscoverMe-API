from django.contrib import admin
from .models import JournalEntry, Mood, MoodLog

admin.site.register(JournalEntry) #added by Zachary
admin.site.register(MoodLog)
admin.site.register(Mood)