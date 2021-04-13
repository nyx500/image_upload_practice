from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *

# Create your views here.

def display(request):
    if request.method == "GET":
        Images = Image.objects.all()
        return render(request, 'image/display.html', {
            'images': Images
        })

def index(request):
    if request.method == "POST":
        if request.user.is_authenticated:

                form = ImageForm(request.POST, request.FILES)

                if form.is_valid():
                    image = Image(
                        user = request.user,
                        image = form.cleaned_data['image']
                    )
                    image.save()
                    return redirect('success')
                else:
                    return render(request, "image/index.html", {
                        "message": "failure"
                    })
        else:
            return HttpResponseRedirect(reverse("login"))
    else:
        form = ImageForm()
        return render(request, 'image/index.html', {
            'form': form
        })

def success(request):
    return HttpResponse('successfully uploaded')

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "image/login.html", {
                "message": "Invalid email and/or password."
                })
    else:
        return render(request, "image/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "image/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "image/register.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "image/register.html")