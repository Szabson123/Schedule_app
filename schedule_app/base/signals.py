from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from base.models import Profile, Company, InvitationCode


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    user  = user.instance
    if created:
        profile = Profile.objects.create(user=user)
        inv_code = getattr(instance, '_inv_code', None)
        
        if inv_code:
            invitation_code = InvitationCode.objects.get(code=inv_code)
            profile.inv_code = invitation_code
            profile.save()
            
            invitation_code.is_used = True
            invitation_code.save()
            
        
    user_group, _ = Group.objects.get_or_create(name='User')
    user_group.user_set.add(instance)


@receiver(post_save, sender=Company)
def create_company_user_profile(sender, instance, created, **kwargs):
    user = instance.owner
    if created:
        profile = Profile.objects.get_or_create(user=user)
        
        inv_code = getattr(instance, '_inv_code', None)
        if inv_code:
            invitation_code = InvitationCode.objects.get(code=inv_code)
            profile.inv_code = invitation_code
            profile.save()
            
            invitation_code.is_used = True
            invitation_code.save()

    boss_group, _ = Group.objects.get_or_create(name='Boss')
    boss_group.user_set.add(user)
