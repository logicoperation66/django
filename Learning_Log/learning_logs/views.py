from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404


# Create your views here.

def index(request):
    """Strona główna aplikacji Learning Log."""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Wyświetlanie wszystkich teamtów"""
    topics =  Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Wyświetla pojędyńczy teamt i wszystkie powiązane z nim wpisy."""
    topic = Topic.objects.get(id=topic_id)
    #Upewniamy się że tamat należy do danego użytkownika.
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Dodaj nowy temat."""
    if request.method != 'POST':
        #Nie przekazano żadnych danych należy utworzuć pusty formularz.
        form = TopicForm()
    else:
        #Przekazano dane za pomoca żądania POST, należy je przetowrzyć.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')

    #Wyświetlenie pustego formularza
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Dodanie nowego wpisu dla określonego tematu."""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        #Nie przekazano żadnych danych, należy utworzyć pusty formularz.
        form = EntryForm()

    else:
        #Przekazano dane za pomocą żadania POST, należy je przetworzyć.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    #Wyświetlanie pustego formularza.
    context = {'topic':topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edycja instniejącego wpisu."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        #Żądanie początkowe, wypełnienie formularza aktualną trościa wpisu.
        form = EntryForm(instance=entry)

    else:
        #Przekazano dane za pomocą żądania POST, należy je przetworzyć.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    #Wyświetlanie pustego formularza.
    context = {'entry':entry, 'topic':topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
