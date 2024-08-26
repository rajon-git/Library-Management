from django.shortcuts import render,redirect, get_object_or_404
from .forms import RegistrationForm, UserForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .forms import AddAmountForm

# Create your views here.
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

            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number = phone_number
            user.is_active=True
            user.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    context={
        'form':form
    }
    return render(request, 'author/register.html',context)


def user_login(request):
    if request.method == 'POST':
        email= request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are logged in.')
            return redirect('dashobard')
        else:
            messages.error(request, 'Invalid login creadentials')
            return redirect('login')
    return render(request, 'author/login.html')


def user_logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out successfull')
    return redirect('login')

def dashobard(request):
    
    return render(request, 'author/dashboard.html')

@login_required
def add_amount(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if amount:
            try:
                amount = float(amount)
                user = request.user
                
                # Initialize user.amount if it's None
                if user.amount is None:
                    user.amount = 0
                
                user.amount += amount
                user.save()
                messages.success(request, f'Amount of {amount} added successfully!')
            except ValueError:
                messages.error(request, 'Invalid amount entered.')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
        else:
            messages.error(request, 'Amount cannot be empty.')
        return redirect('dashobard')
    return redirect('dashobard')
