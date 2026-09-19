from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import LoginHistory


def get_client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    return xff.split(',')[0].strip() if xff else request.META.get('REMOTE_ADDR')


@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    LoginHistory.objects.create(
        user=user,
        action='login',
        ip_address=get_client_ip(request),
    )


@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    if user:
        LoginHistory.objects.create(
            user=user,
            action='logout',
            ip_address=get_client_ip(request),
        )