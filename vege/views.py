from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail


@login_required(login_url="/login/")
def receipes(request):
    # Frontend to Backend
    if(request.method == "POST"):
        data=request.POST

        receipe_name=data.get('receipe_name')
        receipe_desc=data.get('receipe_desc')
        receipe_image=request.FILES.get('receipe_image')

        Receipe.objects.create(
            receipe_name=receipe_name,
            receipe_desc=receipe_desc,
            receipe_image=receipe_image
        )

        return redirect('/receipes/')
    
    queryset = Receipe.objects.all()

    if request.GET.get('search'):
          queryset = queryset.filter(receipe_name__icontains=request.GET.get('search'))

    # Backend to Frontend
    context = {'receipes': queryset}
    return render(request, 'receipes.html', context)


@login_required(login_url="/login/")
def update_receipe(request, id):
        queryset = Receipe.objects.get(id=id)

        if(request.method == "POST"):
            data=request.POST

            receipe_name=data.get('receipe_name')
            receipe_desc=data.get('receipe_desc')
            receipe_image=request.FILES.get('receipe_image')

            queryset.receipe_name=receipe_name
            queryset.receipe_desc=receipe_desc

            if receipe_image:
                  queryset.receipe_image=receipe_image

            queryset.save()
            return redirect('/receipes/')

        context = {'receipe': queryset}
        return render(request, 'update_receipes.html', context)



@login_required(login_url="/login/")
def delete_receipe(request, id):
        queryset = Receipe.objects.get(id=id)
        queryset.delete()
        return redirect('/receipes/')



def login_page(request):
      if request.method=='POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user_obj = User.objects.filter(username=username).first()

            if user_obj is None:
                  messages.error(request, 'User not found!')
                  return redirect('/login')

            profile_obj = Profile.objects.filter(user=user_obj).first()
            if not profile_obj.is_verified:
                  messages.error(request, 'Your profile is not verified check your mail.')
                  return redirect('/login')

            user = authenticate(username=username, password=password)

            if user is None:
                  messages.error(request, 'Invalid Password')
                  return redirect('/login')

            login(request, user)
            return redirect('/receipes/')
                  
                  
      return render(request, 'login.html')



def logout_page(request):
      logout(request)
      return redirect('/login/')



def register(request):
      if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')

            try:
                  user_obj = User.objects.filter(username=username)
                  if user_obj.exists():
                        messages.info(request, 'Username already taken!')
                        return redirect('/register/')

                  user_obj = User.objects.create(
                        first_name = first_name,
                        last_name = last_name,
                        username = username,
                        email = email
                  )

                  user_obj.set_password(password)
                  user_obj.save()

                  auth_token = str(uuid.uuid4())

                  profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token)
                  send_verification_email(email, auth_token)
                  messages.success(request, 'Account created Successfully! Please check your email to verify your account.')
                  return redirect('/register/')
            except Exception as e:
                  print(e)

      return render(request, 'register.html')


def verify(request, auth_token):
      try:
            profile_obj = Profile.objects.filter(auth_token=auth_token).first()
            if profile_obj:
                  if profile_obj.is_verified:
                        messages.success(request, 'Your Account is already verified!')
                        return redirect('/login/')
                  profile_obj.is_verified=True
                  profile_obj.save()
                  messages.success(request, 'Your Account has been verified!')
                  return redirect('/login/')
            else:
                  return redirect('/error')
      except Exception as e:
            print(e)

      return redirect('/login/') 



def error_page(request):
      return render(request, 'error.html')




def send_verification_email(email, token):
      subject = 'Your account needs to be verified.'
      message = f'Please click the link to verify your email: http://127.0.0.1:8000/verify/{token}/'
      from_email = settings.EMAIL_HOST_USER
      recipient_list = [email]

      send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
      )
