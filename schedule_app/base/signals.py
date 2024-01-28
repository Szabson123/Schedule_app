from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from base.models import Profile, Company, InvitationCode


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        pass
    user_group, _ = Group.objects.get_or_create(name='User')
    user_group.user_set.add(instance)


@receiver(post_save, sender=Company)
def create_company_user_profile(sender, instance, created, **kwargs):
    user = instance.owner
    if created:
        pass
    boss_group, _ = Group.objects.get_or_create(name='Boss')
    boss_group.user_set.add(user)
