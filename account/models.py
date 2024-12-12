from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    
    def __str__(self) -> str:
        x=str(self.email).index("@")

        return self.email[:x]
    


class PageSettings(models.Model):
    title = models.CharField( max_length=50)

