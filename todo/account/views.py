from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .forms import CustomUserCreationForm

# Create your views here.


def signup(request):
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            if user is not None:
                login(request, user)
                return redirect("url-tasks")

    context = {"form": form, "page": "register"}
    return render(request, "account/signup.html", context)


def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("url-tasks")

    return render(request, "account/signin.html")


def signout(request):
    logout(request)
    return redirect("url-signin")
