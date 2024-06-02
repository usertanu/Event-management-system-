# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Event, Attendee
from .forms import EventForm
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages


def event_list(request):
    events = Event.objects.all()
    return render(request, 'event/event_list.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    attendees = Attendee.objects.filter(event=event)
    return render(request, 'event/event_detail.html', {'event': event, 'attendees': attendees})

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm()
    return render(request, 'event/event_form.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'You have successfully registered! You can now log in and view events.')
            return redirect('home_view')  # redirect to events page
        else:
            error_message = "invalid details!! check properly and reenter."
    else:
        form = RegistrationForm()
        error_message = ""
    return render(request, 'registration/register.html', {'form': form, 'error_message': error_message, })

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('home_view')
        else:
            error_message = "Invalid username or password"
            return render(request, 'registration/login.html', {'error_message': error_message})
    else:
        return render(request, 'registration/login.html')
   

def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def home_view(request):
    return render(request, 'event/home.html', {'greeting': 'Welcome to Event Management System!', 'introduction': 'This is a system for managing events.'})



