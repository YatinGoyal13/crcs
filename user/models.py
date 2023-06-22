from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


    def __str__(self):
        return self.name

class Profile(AbstractBaseUser):
    email = models.EmailField(verbose_name="email",max_length=60, unique=True)
    username = models.CharField(verbose_name="society name",max_length=100, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    registered_address = models.CharField(max_length=200, null=True, blank=True)
    area_of_operation = models.CharField(max_length=200, null=True, blank=True)
    pan_no = models.CharField(max_length=10, null=True, blank=True)
    tan_no = models.CharField(max_length=10, null=True, blank=True)
    officer_authorized = models.CharField(max_length=100, null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    mobile_no = PhoneNumberField(null=True, blank=True)
    service_tax_no = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=40, null=True, blank=True)
    district = models.CharField(max_length=40, null=True, blank=True)
    society_type = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return "{}:{}:{}".format(self.id, self.email, self.username)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
    
    @property
    def next_payment_date(self):
        if not self.is_paid:
            return self.date_joined
        return self.date_joined + timezone.timedelta(days=365)

    @property
    def payment_status(self):
        if self.is_paid:
            return "Paid"
        return "Dues"

    def make_payment(self):
        self.is_paid = True
        self.save()



    
class Society(models.Model):
    username = models.CharField(max_length=100)
    registered_address = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=40, null=True, blank=True)
    district = models.CharField(max_length=40, null=True, blank=True)
    date_joined = models.DateTimeField(verbose_name='date joined', default=timezone.now,null=True,blank=True)
    area_of_operation = models.CharField(max_length=200, null=True, blank=True)
    society_type = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.username
    
class Grievance(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    mob_no = models.CharField(max_length=10)
    complain_type = models.CharField(max_length=100)
    complain_soc = models.CharField(max_length=100)
    complainXfeedback = models.CharField(max_length=100)
    complain_date= models.DateTimeField(verbose_name='date of complain', auto_now_add=True)

    def __str__(self):
        return self.name
    
class Request(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    )
    
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='requests')
    #request_number = models.PositiveIntegerField()
    request_number = models.PositiveIntegerField(default=0)
    request_text = models.TextField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "Request {}: {}".format(self.request_number, self.status)