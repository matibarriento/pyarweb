from django.db import models
from django.utils import timezone
from django.conf import settings
from allauth.account.signals import user_signed_up
from waliki.models import ACLRule
from django.contrib.auth.models import Permission
from waliki.settings import get_slug
from django.dispatch import receiver


@receiver(user_signed_up)
def create_acl_for_user_wiki_own_page(sender, **kwargs):
    user = kwargs['user']
    perms = Permission.objects.filter(content_type__app_label='waliki',
                                      codename__in=('add_page', 'change_page')).values_list(
        'id', flat=True)

    rule, created = ACLRule.objects.get_or_create(name='pagina propia {}'.format(str(user)),
                                                  slug='miembros/{}'.format(
                                  get_slug(user.username)),
                              apply_to=ACLRule.TO_EXPLICIT_LIST,
                              as_namespace=True
                              )
    if created:
        rule.permissions.add(*perms)
        rule.users.add(user)


def is_active_default():
    # Use True if we don't want to moderate.
    # If we want to, set to False and wait a moderator to put it in True
    return not settings.TELEGRAM_MODERATION


class ModerateModel(models.Model):

    is_active = models.BooleanField(default=is_active_default)
    ts_moderate = models.DateTimeField(null=True, blank=True)
    user_moderate = models.TextField(null=True, blank=True)

    def moderate(self, approved, user_moderate):
        self.approved = approved
        self.user_moderate = user_moderate
        self.ts_moderate = timezone.now()
        self.save()

    class Meta:
        abstract = True
