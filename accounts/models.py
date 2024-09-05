from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password =None):
        if not email:
            raise ValueError('User must have an email address')
        
        if not username:
            raise ValueError('User must have a username')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user 
    def create_superuser(self, first_name, last_name, email, username,password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            password=password
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using = self._db)
        return user

# Create your models here.
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=11)
    amount = models.FloatField(default=0, blank=True,null=True)
    request_amount = models.FloatField(default=0, blank=True,null=True)
    accept_request = models.BooleanField(default=False)

    #required
    date_join = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if self.accept_request and self.request_amount > 0:
            self.amount += self.request_amount
            
          
            mail_subject = 'Request Accepted'
            message = render_to_string('email_template.html', {
                'user': self,
                'request_amount': self.request_amount,
            })
            to_email = self.email

            send_email = EmailMessage(mail_subject, message, from_email=settings.EMAIL_HOST_USER, to=[to_email])
            send_email.content_subtype = 'html'  
            send_email.send()
            self.request_amount = 0
            self.accept_request = False

        super(Account, self).save(*args, **kwargs)

        
       

    


