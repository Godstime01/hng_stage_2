import uuid

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from auth_core.models import UserModel


class Organisation(models.Model):
    orgId = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(UserModel)
    
    def __str__(self):
        return self.name


@receiver(post_save, sender=UserModel)
def organisation_created_handler(sender, instance, created, **kwargs):
    if created:
        name = f"{instance.firstName}'s Organisation"
        org = Organisation.objects.create(name=name)
        org.users.add(instance)
        org.save()
