from django import setup
from django.db.models.query import prefetch_related_objects
from django.shortcuts import redirect, render
from .forms import signupForm, notesForm
from .models import signup
from django.contrib.auth import logout
from django.core.mail import send_mail
from BatchProject import settings
import requests
import json
import random

# Create your views here.


def index(request):
    if request.method == 'POST':
        if request.POST.get("signup") == "signup":
            signupreq = signupForm(request.POST)
            if signupreq.is_valid():
                signupreq.save()
                print("Signup Sucessfully!")

                # send mail

                subject="Re:Signup Successfully!.."
                msg="Hello user, \nThank You for getting in touch! \nWelcome to our community. \nWe will keep your information safe. \nWe will respond to you soon. \nThanks, \nEdu@adv"
                from_mail=settings.EMAIL_HOST_USER
                #to_mail=["drashtipatel54@gmail.com","dippatel111@gmail.com"]
                to_mail=[request.POST["username"]]

                send_mail(subject,msg,from_mail,to_mail)

                return redirect('notes')
            else:
                print(signupreq.errors)
        elif request.POST.get("login") == "login":
            unm = request.POST["username"]
            pas = request.POST["password"]

            userid = signup.objects.get(username=unm)
            user = signup.objects.filter(username=unm, password=pas)
            if user:
                print("Login Successfully!")
                request.session["user"] = unm
                request.session["userid"] = userid.id

                # send SMS

                                # mention url
                url = "https://www.fast2sms.com/dev/bulk"

                otp=random.randint(1111,9999)

                # create a dictionary
                my_data = {
                    # Your default Sender ID
                    'sender_id': 'FSTSMS', 
                    
                    # Put your message here!
                    'message': 'Dear user, You have Successfully Logged in and your OTP is {otp}',
                    
                    'language': 'english',
                    'route': 'p',
                    
                    # You can send sms to multiple numbers
                    # separated by comma.
                    'numbers': '7405037344'    
                }
                
                # create a dictionary
                headers = {
                    'authorization': 'ec8FxTCSUNyWDYQV6uKPhA1ZLbgz5403X2tRpnsiO7klodajvIt1yaLZ03PpEW5zlUsSRqT6KXjmoCHk',
                    'Content-Type': "application/x-www-form-urlencoded",
                    'Cache-Control': "no-cache"
                }

                                # make a post request
                response = requests.request("POST",
                                            url,
                                            data = my_data,
                                            headers = headers)

                #load json data from source
                returned_msg = json.loads(response.text)

                #print the sed message
                print(returned_msg['message'])
                
                return redirect('notes')
            else:
                print("Login faild....Try again!")
        else:
            signupreq = signupForm()
    return render(request, 'index.html')


def notes(request):
    user = request.session.get("user")
    if request.method == 'POST':
        notesfrm = notesForm(request.POST, request.FILES)
        if notesfrm.is_valid():
            notesfrm.save()
            print("Your notes has been uploaded!")
        else:
            print(notesfrm.errors)
    else:
        notesfrm = notesForm()
    return render(request, 'notes.html', {'user': user})


def userlogout(request):
    logout(request)
    return redirect('/')


def updateprofile(request):
    user = request.session.get("user")
    userid = request.session.get("userid")
    if request.method == 'POST':
        signupfrm = signupForm(request.POST)
        id = signup.objects.get(id=userid)
        if signupfrm.is_valid():
            signupfrm = signupForm(request.POST, instance=id)
            signupfrm.save()
            return redirect('/')
    else:
        signupfrm = signupForm()
    return render(request, 'updateprofile.html', {'user': user, 'userid': signup.objects.get(id=userid)})

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')
