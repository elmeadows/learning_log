import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learning_log.settings")

import django
django.setup()

from MainApp.models import *

topics = Topic.objects.all()

#print(topics)

for topic in topics:
    print(topic)
    print(topic.date_added)

t = Topic.objects.get(id=2)

print(t.text)
print(t.date_added)

entries = Entry.objects.filter(topic=t)

for entry in entries:
    print(entry)
