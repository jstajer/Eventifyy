from django.contrib.auth.decorators import login_required
from django.shortcuts import *
from .forms import UserRegistrationForm, EventForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .models import Event


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # přesměruje na domovskou stránku po úspěšné registraci
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')  # přesměruje na domovskou stránku po úspěšném přihlášení
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def event_list(request):
    events = Event.objects.all().order_by('start_date')
    return render(request, 'event_list.html', {'events': events})


def event_detail(request, pk):
    event = Event.objects.get(pk=pk)
    return render(request, 'event_detail.html', {'event': event})


@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user  # Přiřazení organizátora události
            event.save()
            return redirect('event_detail', pk=event.pk)  # Přesměrování na detail vytvořené události
    else:
        form = EventForm()
    return render(request, 'event_create.html', {'form': form})


@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'event_form.html', {'form': form})


def home(request):
    return redirect('event_list')
