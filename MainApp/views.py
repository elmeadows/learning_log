from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import * # . says look in same direction and * means all
from django.http import Http404

# Create your views here.
def index(request):
    return render(request, 'MainApp/index.html')

@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')

    context = {'topics':topics} # key represents var name used in template; value represents var name in view

    return render(request, 'MainApp/topics.html', context)

@login_required
def topic(request, topic_id):
    t = Topic.objects.get(id = topic_id)

    if t.owner != request.user:
        raise Http404

    entries = Entry.objects.filter(topic = t).order_by('-date_added')

    context = {'topic':t, 'entries':entries}

    return render(request, 'MainApp/topic.html', context)

@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)

        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()

            return redirect('MainApp:topics')
        
    context = {'form':form}
    return render(request, 'MainApp/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

    if topic.owner != request.user:
        raise Http404    
    
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)

        if form.is_valid():
            new_entry = form.save(commit=False) # FINAL:: commit = False means don't save this to the database
            new_entry.topic = topic
            new_entry.save()

            return redirect('MainApp:topic', topic_id=topic.id) # FINAL:: topic.id gets id attribute from topic; topic_id is a variable passes through:: both work here
        
    context = {'form':form, 'topic':topic}
    return render(request, 'MainApp/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry) # pulling up exact data to be edited, so instance = Entry
    else:
        form = EntryForm(data=request.POST, instance=entry)

        if form.is_valid():
            form.save()
            return redirect('MainApp:topic', topic_id=topic.id) # FINAL:: topic.id gets id attribute from topic; topic_id is a variable passes through:: both work here
        
    context = {'form':form, 'topic':topic, 'entry':entry}
    return render(request, 'MainApp/edit_entry.html', context)