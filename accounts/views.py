from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
import requests

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split("@")[0]

            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password
            )
            user.phone_number = phone_number
            user.save()

            messages.success(
                request,
                'Thank you for registering with us. We have sent you a verification email to your email address. Please verify it.'
            )
            return redirect('login')  # Replace 'success_url' with the name of the URL you want to redirect to
    else:
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'author/register.html', context)


def user_login(request):
    if request.method == 'POST':
        email= request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are logged in.')
        else:
            messages.error(request, 'Invalid login creadentials')
            return redirect('login')
    return render(request, 'author/login.html')
