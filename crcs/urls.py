"""crcs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from user.views import (
    register,
    profile,
    login_view,
    update_profile,
    view_profile,
    payment_page,
    payment_cancelled,
    payment_done,
    grievances_view,
    submit_request,
    
)
from home.views import (
    home,
    charts,
    info,
)
from filter_app.views import(
    reg_soc,
    get_districts_view,
    state_wise,
    cal_wise,
    bank_data,
)

urlpatterns = [
    path('admin/login/', auth_views.LoginView.as_view(template_name='user/admin_login.html'), name='admin_login'),
    path('admin/', admin.site.urls),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('charts/', charts, name='charts'),
    path('info/', info, name='info'),
    path('bank_data/',bank_data,name='bank_data'),
    path('grievances/', grievances_view, name='grievances'),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'), name='password_reset'),
    
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='user/password_change.html'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='user/password_change_done.html'), name='password_change_done'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name='password_reset_complete'),
    path('profile/', profile, name='profile'),
    path('update_profile/', update_profile, name='update_profile'),
    path('view_profile/', view_profile, name='view_profile'),
    path('get-districts/', get_districts_view, name='get-districts'),
    path('registeredsocities/',reg_soc,name='reg_soc'),
    path('statewise/',state_wise,name='state_wise'),
    path('calendaryearwise/',cal_wise,name='cal_wise'),
    path('payment_page/', payment_page, name='payment_page'),
    path('payment_cancelled/',payment_cancelled, name='payment_cancelled'),
    path('payment_done/', payment_done, name='payment_done'),
    path('submit-request/', submit_request, name='submit_request'),
    

]

admin.site.site_header = "CRCS Admin"
admin.site.site_title = "CRCS Admin Portal"  