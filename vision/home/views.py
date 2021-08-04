from django.shortcuts import render, HttpResponse, redirect
from .models import Upload
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from django.contrib import messages
# superuser username-admin /  passward-tirtha098
# Create your views here.


def index(request):
    return redirect("/upload")


def upload(request):
    if request.user.is_anonymous:
        return redirect("/login")
    if request.method == "POST":
        img = request.FILES['image']
        orgimage = request.FILES['image']
        action = request.POST.get("option")
        username = request.user.username
        print(img)
        user = Upload(image=img, orgimage=orgimage,
                      action=action, username=username)
        user.save()
        # img_obj=user.instance
        # print(img_obj)
        users = Upload.objects.all()
        p = users[len(users)-1]
        return render(request, "upload.html", {"p": p})
    messages.add_message(request, messages.INFO,
                         "welcome !!, you are logged in.")
    return render(request, "upload.html")


def loginuser(request):

    if request.method == "POST":
        username = request.POST.get('username')
        passward = request.POST.get('passward')
        user = authenticate(username=username, password=passward)
        if user is not None:
            login(request, user)
            return redirect("/upload")
        else:
            messages.add_message(request, messages.INFO,
                                 "Wrong authentication details !! Try again.")
            return render(request, "upload.html")
    return render(request, "login.html")


def logoutuser(request):
    if request.user.is_anonymous:
        return redirect("/")
    logout(request)
    return redirect("/")


def deluser(request):
    pass


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        passward = request.POST.get('passward')

        try:
            user = User.objects.get(username=username)
            context = {
                'error': 'The username you entered has already been taken. Please try another username.'}
            return render(request, 'register.html', context)
        except User.DoesNotExist:
            User.objects.create_user(username, email, passward)
            return redirect("/login")

    else:
        return render(request, "register.html")


def showimg(request):
    if request.user.is_anonymous:
        return redirect("/")
    username = request.user.username
    users = Upload.objects.all().filter(username=username)
    # p=users[len(users)-1].pic.url

    return render(request, "view.html", {"users": users})


def delimage(request, id):
    if request.user.is_anonymous:
        return redirect("/")
    else:
        print("id....", id)
        image = Upload.objects.get(id=id)
        image.delete()
        return redirect("/showimg")


def profile(request):
    if request.user.is_anonymous:
        return redirect("/")
    thisuser = str(request.user)
    user = User.objects.get(username=thisuser)

    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")

        username = request.user
        user = User.objects.get(username=username)
        user.first_name = firstname
        user.last_name = lastname
        if user.email == "":
            user.email = email
        user.save()

        return redirect("/profile")

    return render(request, "profile.html")
