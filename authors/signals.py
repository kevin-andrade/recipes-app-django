from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

from authors.models import Profile


User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(created, instance, sender, *args, **kwargs):
    if created:
        profile = Profile.objects.create(author=instance)
        profile.save()
