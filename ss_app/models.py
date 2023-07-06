from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The email field must be set')
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    name = models.CharField(max_length=60, default='')
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number', 'gender', 'dob']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff
    

class chat_history(models.Model):
    sender = models.ForeignKey(User , related_name="message_sender", null=True, on_delete=models.SET_NULL)
    reciever = models.ForeignKey(User , related_name="message_reciever",null=True, on_delete=models.SET_NULL)


class Chat(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    chat_history_id = models.ForeignKey(chat_history, on_delete=models.CASCADE)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()

    def __unicode__(self):
        return self.message


