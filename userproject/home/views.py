from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout,login
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from home.models import Contact
from django.contrib import messages
# Create your views here.
#superuser data/username-admints/passward-admin098
#user data/username-tirtha/passward-admin098

def index(request):
   
    
    if request.user.is_anonymous:
         messages.add_message(request,messages.INFO,"You are not logged-in.Please log-in to access all contents.")
         return render(request,"index.html")
        
    return render(request,"index.html")

def loginuser(request):
    logout(request)
    if request.method=="POST":
        username=request.POST.get('username')
        passward=request.POST.get('passward')
        user = authenticate(username=username, password=passward)
        if user is not None:
            login(request,user)
            return redirect("/")
        else:
            messages.add_message(request,messages.INFO,"Wrong authentication details !! Try again.")
            return render(request,"login.html")  


    return render(request,"login.html")

def logoutuser(request):
    if request.user.is_anonymous:
        return redirect("/")
    logout(request)
    return redirect("/")      


def about(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return HttpResponse("about me") 
def services(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return HttpResponse("we provides a lot of services")  
def contact(request):
    if request.user.is_anonymous:
        return redirect("/login")
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        comment=request.POST.get('comment')
        contact=Contact(name=name,email=email,phone=phone,comment=comment,date=datetime.today())
        contact.save()
        
        messages.success(request, 'Thank you:your data has been updated !')

    return render(request,"contact.html")
def portfolio(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return HttpResponse("view portf")



def register(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        passward=request.POST.get('passward')
        try:
            user= User.objects.get(username=username)
            context= {'error':'The username you entered has already been taken. Please try another username.'}
            return render(request, 'register.html', context)
        except User.DoesNotExist:
            User.objects.create_user(username,email,passward)
            return redirect("/login")
        
        
    else:
        return render(request,"register.html") 


def profile(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request, 'profile.html')    

def del_user(request):
    if request.user.is_anonymous:
        return redirect("/login")
    username=request.user.username        
    try:
        user= User.objects.get(username=username)
        user.delete()
        logout(request)
        messages.success(request, "The user is deleted")            

    except User.DoesNotExist:
        messages.error(request, "User doesnot exist")    
        return render(request, 'index.html')

    except Exception as e: 
        return render(request, 'index.html',{'err':e})

    return render(request, 'index.html') 