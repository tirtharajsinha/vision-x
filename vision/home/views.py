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
    if request.user.is_anonymous:
        return render(request, "index.html")
    return redirect("/dashboard")


def dashboard(request):
    if request.user.is_anonymous:
        return redirect("/login")
    username = request.user.username
    loaded = Upload.objects.all().filter(username=username)
    used = len(list(loaded))
    if used > 10:
        imageids = loaded.values_list("id", flat=True)
        print(imageids)
        for i in imageids:
            image = Upload.objects.get(id=i)
            image.delete()
    loaded = Upload.objects.all().filter(username=username)
    used = len(list(loaded))
    return render(request, "dashboard.html", {"used": used})


def service(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request, "service.html")


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
        loaded = Upload.objects.all().filter(username=username)
        used = len(list(loaded))
        if(used >= 10):
            messages.add_message(request, messages.INFO,
                                 "You are out of freespace. last upload not saved. for more info visit dashboard.")
        return render(request, "upload.html", {"p": p})

    return render(request, "upload.html")


def loginuser(request):

    if request.method == "POST":
        username = request.POST.get('username')
        passward = request.POST.get('passward')
        user = authenticate(username=username, password=passward)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.INFO,
                                 "welcome back, " + str(request.user) + ". you are now logged in.")
            return redirect("/dashboard")
        else:
            messages.add_message(request, messages.INFO,
                                 "Wrong authentication details !! Try again.")
            return render(request, "login.html")
    return render(request, "login.html")


def logoutuser(request):
    if request.user.is_anonymous:
        return redirect("/")
    logout(request)
    return redirect("/")


def deluser(request):
    if request.user.is_anonymous:
        return redirect("/")

    if request.method == "POST":
        username = str(request.user)
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            user.delete()
            logout(request)
            userdata = Upload.objects.all().filter(username=username)
            userdata.delete()
            return redirect("/")
        else:
            messages.add_message(request, messages.ERROR,
                                 "authentication failed !!")
            return redirect("/")
    return render(request, "auth.html")


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


def about(request):
    return render(request, "about.html")


def auth(request):
    pass
