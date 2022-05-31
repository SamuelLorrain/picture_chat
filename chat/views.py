from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.admin import UserCreationForm, User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from .models import Room, Message

def register(request):
    form = UserCreationForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user = User.objects.create_user(
                form.cleaned_data['username'],
                form.cleaned_data['password1'],
            )
            user.save()
            return redirect(reverse('login'))
    return render(request, 'register.html', {'form': form})

def loginView(request):
    if request.user.is_authenticated:
        return redirect(request.GET.get('next') or reverse('index'))

    authentication = AuthenticationForm(data=request.POST or None)
    if authentication.is_valid():
        user = authenticate(
            request,
            username=authentication.cleaned_data['username'],
            password=authentication.cleaned_data['password'])
        if user is not None:
            login(request, user)
            return redirect(reverse('index'))

    return render(request, 'login.html', {'form': authentication})

# class ?
@login_required
def indexChatRoom(request):
    rooms = Room.objects.all()
    return render(request, 'rooms/index.html', {'rooms': rooms})

@login_required
def showChatRoom(request, pk):
    room = get_object_or_404(Room, id=pk)
    messages = room.message_set.all()
    return render(request, "rooms/show.html", {'room': room, 'messages':messages})

@login_required
def createChatRoom(request, pk):
    return HttpResponse("create")

@login_required
def sendMessage(request, pk):
    return HttpResponse("send")
