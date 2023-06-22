from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, AccountAuthenticateForm, AccountUpdateForm, GrievanceForm
from .models import Society, Grievance, Profile
from datetime import datetime
from decimal import Decimal
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from urllib.parse import urlencode
from .models import Request

import uuid
from django.urls import reverse
from django.shortcuts import redirect


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            mymodel=Society()
            mymodel.username=form.cleaned_data.get('username')
            mymodel.registered_address=form.cleaned_data.get('registered_address')
            mymodel.date_joined = datetime.now()
            mymodel.society_type=form.cleaned_data.get('society_type')
            mymodel.area_of_operation=form.cleaned_data.get('area_of_operation')
            mymodel.state=form.cleaned_data.get('state')
            mymodel.district=form.cleaned_data.get('district')
            mymodel.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            user = authenticate(email=email, password=password)
            messages.success(request, f'Account created for {email}! Please log in.')
            #login(request, user)
            return redirect('login')
        else:
          print(form.errors)
    else:
        form=RegistrationForm()
    return render(request, 'user/register.html', {'form': form})

from .forms import GrievanceForm

def grievances_view(request):
    societies = Society.objects.all()
    if request.method == 'POST':
        form = GrievanceForm(request.POST)
        if form.is_valid():
            grievance = form.save(commit=False)
            messages.success(request, 'Your complaint/feedback has been recorded.')
            grievance.save()  # Save the grievance object to the database
            return redirect('home')
        else:
            print(form.errors)  # Print the form errors to the console for debugging purposes
    else:
        form = GrievanceForm()
    return render(request, 'user/grievances.html', {'form': form, 'societies': societies})


def login_view(request):
    user = request.user
    if request.method == 'POST':
        form = AccountAuthenticateForm(data=request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(email=email,password=password)
            if user:
                login(request, user) 
                messages.success(request, f'You are logged in.')
                return render(request,'user/profile.html')
            else:
                form = AccountAuthenticateForm()
    else:
        form = AccountAuthenticateForm()
    return render(request, 'user/login.html',{'form': form})

from datetime import date, timedelta

@login_required 
def profile(request):
    return render(request, 'user/profile.html')
    

@login_required
def payment_page(request):
    host = request.get_host()
    id = request.user.id

    paypal_dict = {
                'business': settings.PAYPAL_RECEIVER_EMAIL,
                'amount': '300.50',
                'item_name': 'Annual Fee Payment',
                'invoice': str(uuid.uuid4()),
                'currency_code': 'USD',
                'notify_url': f'http:/{host}{reverse("paypal-ipn")}',
                'return_url': f'http://{host}{reverse("payment_done")}?{urlencode({"id": id})}',
                'cancel_return': f'http:/{host}{reverse("payment_cancelled")}',
            }
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {'form': form}  
    return render(request, 'user/payment_page.html', context)

from django.views.decorators.csrf import csrf_exempt
#######===== PROCESS PAYMENT=====########
@csrf_exempt
def payment_done(request):
    if request.method == 'GET':
        context = request.GET
        profile = Profile.objects.get(id=context['id'])
        profile.is_paid = True
        profile.save()
        messages.success(request, 'Payment was successful.')
        return redirect('profile')
    elif request.method == 'POST':
        context = request.POST
        profile = Profile.objects.get(id=context['id'])
        profile.is_paid = True
        profile.save()
        messages.success(request, 'Payment was successful.')
        return redirect('profile')
    messages.warning(request, 'Payment was successful.')
    return redirect('profile')



@csrf_exempt
def payment_cancelled(request):
    messages.warning(request, 'Payment was cancelled.')
    return redirect('profile')


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been updated.')
            return render(request,'user/profile.html')
    else:
        form = AccountUpdateForm(instance=request.user)
    return render(request, 'user/update_profile.html', {'form': form})


@login_required
def view_profile(request):
    return render(request, 'user/view_profile.html', {'user': request.user})

@login_required
def submit_request(request):
    if request.method == 'POST':
        request_text = request.POST.get('request_text')
        
        # Create a new Request object and save it to the database
        new_request = Request.objects.create(user=request.user, request_text=request_text)
        
        # Set the request number and status accordingly
        new_request.request_number = new_request.id  # Assuming request_number is the ID of the request object
        new_request.status = 'Pending'
        new_request.save()
        
        return redirect('profile') 
    
    return render(request, 'user/submit_request.html')