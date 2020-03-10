from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver

from backend import paths


class UserDetails(models.Model):
    """ User details model """
    user = models.OneToOneField(User, primary_key=True, related_name='details', on_delete=models.CASCADE)
    img = models.ImageField(blank=True, null=True, upload_to=paths.user_img_path)

    def __str__(self):
        return f'{self.pk} | {self.user.first_name} {self.user.last_name}'


@receiver(post_delete, sender=UserDetails)
def delete_user_img(sender, instance, **kwargs):
    """ Removes static asset for user img attribute when record is removed from DB """
    instance.img.delete(False)


class PQP(models.Model):
    headers = models.CharField(max_length=1000)
    body = models.CharField(max_length=1000)
    method = models.CharField(max_length=1000)
    content_type = models.CharField(max_length=1000)
    params = models.CharField(max_length=1000)
    get_data = models.CharField(max_length=1000)
    post_data = models.CharField(max_length=1000)
    cookies = models.CharField(max_length=1000)
