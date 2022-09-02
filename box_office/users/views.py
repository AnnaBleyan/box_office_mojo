from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import UserLoginForm, UserProfileForm
from .models import Profile


def create_user(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            profile = Profile(user=user)
            profile.save()
            return redirect("welcome")
    context = {"form": form}
    return render(request, 'users/create_user.html', context=context)

def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            profile = Profile(user=user)
            profile.save()
            # messages.success(request, ("Registration successful!"))
            return redirect('welcome')
    else:
        form = UserCreationForm()
    return render(request, 'authenticate/register_user.html', {'form': form})


def user_login(request):
    form = UserLoginForm()
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data["username"]
            user_password = form.cleaned_data["password"]
            user = authenticate(request, username=user_name, password=user_password)
            if user:
                login(request, user)
                messages.success(request, f"{user.username} logged in successfully")
                return redirect("user_profile")
    context = {"form": form}
    return render(request, 'users/user_login.html', context=context)



def user_logout(request):
    logout(request)
    return redirect('welcome')


@login_required(login_url="user_login")
def profile_view(request):
    profile = Profile.objects.get(user_id=request.user.id)

    context = {"profile": profile}
    return render(request, "users/user_profile.html", context=context)


@login_required(login_url="user_login")
def local_user_profile_view(request):
    profile = Profile.objects.get(user_id=request.user.id)

    context = {"profile": profile}
    return render(request, "users/local_user_profile.html", context=context)
