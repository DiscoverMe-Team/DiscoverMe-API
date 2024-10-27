from django.contrib import admin
from .models import MoodLog, Mood

admin.site.register(MoodLog)
admin.site.register(Mood)

from .models import JournalEntry #added by Zachary
admin.site.register(JournalEntry) #added by Zachary