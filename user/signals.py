from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])
        user_profile.save()


@receiver(valid_ipn_received)
def valid_ipn_received(sender, **kwargs):
    ipn=sender
    if ipn.payment_status == 'Completed':
        profile = Profile.objects.get(email=ipn.payer_email)
        profile.is_paid = True
        profile.save()

@receiver(invalid_ipn_received)
def invalid_ipn_received(sender, **kwargs):
    ipn=sender
    if ipn.payment_status == 'Completed':
        profile = Profile.objects.get(email=ipn.payer_email)
        profile.is_paid = True
        profile.save()
