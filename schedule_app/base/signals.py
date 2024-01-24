from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from base.models import Profile, Company


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)



@receiver(post_save, sender=Company)
def create_company_user_profile(sender, instance, created, **kwargs):
    user = instance.owner
    if created:
        Profile.objects.create(user=user)

    boss_group, _ = Group.objects.get_or_create(name='Boss')
    boss_group.user_set.add(user)
