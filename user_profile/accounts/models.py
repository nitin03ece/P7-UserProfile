from django.db import models
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from django.contrib.auth.models import User


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    first_name = models.CharField("First Name", max_length=255, blank=True)
    last_name = models.CharField("Last Name", max_length=255, blank=True)
    dob = models.CharField("Date of Birth", max_length=255, blank=True)
    bio = models.TextField("Bio Data", blank=True)
    avatar = models.ImageField(upload_to='profile_image', blank=True)
    city = models.CharField("City", max_length=255, blank=True)
    favorite_pet = models.CharField("Favorite Pet", max_length=255, blank=True)
    hobbies = models.CharField("Hobbies", max_length=255, blank=True)

    def __str__(self):
        return str(self.user.first_name) + " " + str(self.user.last_name)

    def get_full_name(self):
        return self.user.first_name + " " + self.user.last_name

    @classmethod
    def create_profile(cls, user, dob=" ", bio=" ",
                       avatar=" ", city=" ", favorite_pet=" ", hobbies=" "):
        cls.objects.create(
            user=user,
            dob=dob,
            bio=bio,
            avatar=avatar,
            city=city,
            favorite_pet=favorite_pet,
            hobbies=hobbies
        )
