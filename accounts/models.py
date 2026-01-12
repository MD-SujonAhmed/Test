import random
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.core.exceptions import ValidationError
# from django.contrib.
# Create your models here.

def validate_image(file):
    max_size_mb= 5 
    # size max 
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Image size should not exceed {max_size_mb}MB.")
    validate_extensions=['.jpg','.png','.gif']
    import os
    ext=os.path.splitext(file.name)[1].lower()
    if ext not in validate_extensions:
        raise ValidationError("Unsupported file extension. Only JPG,PNG,GIF are allowed ")
    
    
# EAAe60J8jX3EBQQx1YxrurptvAb8gsmBn3ks6vGQ4ZBe2CCzZBMAdLNxRXgnOBSpsnHBc2BrjzKGjekiWunvt6hGARB1xvcBbOj3ZApf1EBSaLLpOy9KiFDyqnaUUeYOTK2YWM9xt4XMQRLUdnjZA6J63yO2e6CxR9beZABBHufI1rdHOqKrWrmRNSkIBvKrZB46jUBwQZDZD
class AccountManager(BaseUserManager):
    def create_user(self, Email, password=None, **extra_fields):
        if not Email:
            raise ValueError("Email must be set")

        Email = self.normalize_email(Email)
        user = self.model(Email=Email, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.otp=str(random.randint(10000,99999))
        user.save(using=self._db)
        return user

    def create_superuser(self, Email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(Email, password, **extra_fields)


class Account(AbstractBaseUser,PermissionsMixin):
    FirstName=models.CharField(max_length=50)
    LastName=models.CharField(max_length=50)
    Email=models.EmailField(unique=True)
    otp=models.CharField(max_length=5,blank=True,null=True)
    Updated_Photo=models.ImageField(upload_to='images/', validators=[validate_image], blank=True, null=True)
    Business_Name=models.CharField(max_length=50,blank=True)
    website_Url=models.URLField(max_length=200,blank=True)
    USERNAME_FIELD='Email'
    REQUIRED_FIELDS=['FirstName','LastName']
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    objects=AccountManager()
    def __str__(self):
        return self.Email
    
    
    
    
    
    
    
    
    