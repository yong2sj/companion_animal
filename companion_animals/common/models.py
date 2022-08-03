from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image

# User 객체 하나와 매칭되는 Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # 별명
    nickname = models.CharField(max_length=30, default="익명의 집사")
    # 연락처
    phone = models.CharField(max_length=30)
    # 반려동물 종
    species = models.CharField(max_length=30)
    # 반려동물 이름
    pet_name = models.CharField(max_length=30)
    # 이미지
    image = models.ImageField(upload_to="profile/", default="profile/default.png")

    def __str__(self) -> str:
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)

        # 이미지 리사이징
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
