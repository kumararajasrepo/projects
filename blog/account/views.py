from django.http import HttpRequest
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .forms import AccountCreationForm

# Create your views here.


def signup(request: HttpRequest):
    form = AccountCreationForm()

    if request.method == "POST":
        form = AccountCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            image = request.FILES.get("image")

            if image is not None:
                user.image = image
            user.save()

            if user is not None:
                login(request, user)
                return redirect("url-welcome")

    errors = {field: errors for field, errors in form.errors.items()}
    context = {"form": form, "page": "register", "errors": errors}
    return render(request, "account/signup.html", context)


def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("url-welcome")
        else:
            return render(
                request,
                "account/signin.html",
                context={"error": "Invalid Credentials"},
            )
    return render(request, "account/signin.html")


def signout(request):
    logout(request)
    return redirect("url-signin")
