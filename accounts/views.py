from django.shortcuts import render,redirect, get_object_or_404
from .forms import RegistrationForm, UserForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .forms import AddAmountForm
from books.models import BorrowBook

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
        amount_str = request.POST.get('amount')
        
        if not amount_str:
            messages.error(request, 'Amount cannot be empty.')
            return redirect('dashobard')
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Amount must be positive.")
            
            user = request.user
            if user.request_amount is None:
                user.request_amount = 0
            user.request_amount += amount
            user.accept_request = False
            user.save()
            messages.success(request, f'Request to Add {amount} sent successfully!')
        except ValueError as ve:
            messages.error(request, f'Invalid amount entered: {ve}')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
        return redirect('dashobard')
    return redirect('dashobard')

def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)

            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password updated successfully')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request,'Password does not match!')
            return redirect('change_password')
    return render(request, 'author/change_password.html')




