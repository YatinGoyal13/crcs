from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import Profile, Society
from .models import Grievance
from django.contrib.auth import authenticate
from phonenumber_field.formfields import PhoneNumberField



class GrievanceForm(forms.ModelForm):
    complain_soc = forms.ModelChoiceField(queryset=Society.objects.all())
    class Meta:
        model = Grievance
        fields = ['name', 'email', 'mob_no', 'complain_type', 'complain_soc', 'complainXfeedback']



class RegistrationForm(UserCreationForm):
    email = forms.CharField(widget=forms.TextInput)
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Society Name'}))
    registered_address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '1234 Main St'}))
    area_of_operation = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Locality'}))
    pan_no = forms.CharField(widget=forms.TextInput)
    tan_no = forms.CharField(widget=forms.TextInput)
    officer_authorized = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Officer Name'}))
    #mobile_no = forms.CharField(widget=forms.TextInput)
    service_tax_no = forms.CharField(widget=forms.TextInput)

    mobile_no = PhoneNumberField(region='IN')
    state = forms.CharField(widget=forms.Select(choices=[]))
    designation = forms.CharField(widget=forms.Select(choices=[]))
    district = forms.CharField(widget=forms.Select(choices=[]))
    society_type = forms.CharField(widget=forms.Select(choices=[]))
    

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['state'].widget.attrs['onchange'] = 'updateDistricts()'
        
        for field_name, field in self.fields.items():
            field.required = True

    class Meta:
        model = Profile
        fields = ['email','username', 'state','district','society_type','registered_address','area_of_operation', 'pan_no', 'tan_no','officer_authorized', 'designation','mobile_no', 'service_tax_no', 'password1', 'password2']
    



class AccountAuthenticateForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ['email', 'password']
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Login")


class AccountUpdateForm(forms.ModelForm):
    designation = forms.CharField(widget=forms.Select(choices=[]))

    class Meta:
        model = Profile
        fields = ['email', 'username','officer_authorized', 'designation','mobile_no']

    def __init__(self, *args, **kwargs):
        super(AccountUpdateForm, self).__init__(*args, **kwargs)


    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = Profile.objects.exclude(pk=self.instance.pk).get(email=email)
            except Profile.DoesNotExist:
                return email
            raise forms.ValidationError('Email "%s" is already in use.' % account.email) 


