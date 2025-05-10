from django.db import models

class Profile(models.Model):
    telegram_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    city = models.CharField(max_length=30)
    description = models.TextField(max_length=400, blank=True, null=True)
    gender = models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=6)
    prefer_gender = models.CharField(choices=[('male', 'male'), ('female', 'female'), ('anyone', 'anyone')], max_length=6)

    def __str__(self):
        return f"{self.name}: {self.telegram_id}"
    
    
class Photo(models.Model):
    photo_id = models.AutoField(primary_key=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='photos/')
    
    def __str__(self):
        return f"{self.profile.name}: {self.profile.telegram_id}, {self.photo_id}" 
    