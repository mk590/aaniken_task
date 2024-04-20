from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password) 
        user.save(using=self._db) 
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()  

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
      verbose_name = 'Custom User'
      verbose_name_plural = 'Custom Users'

    def __str__(self):
        return self.name


class Player(models.Model):
    name=models.CharField(max_length=200)
    matches_played=models.IntegerField(default=200)
    runs=models.IntegerField(default=12000)
    average=models.IntegerField(default=50)
    strike_rate=models.IntegerField(default=100)
    team=models.ForeignKey('Team',on_delete=models.CASCADE,related_name='players',null=True,blank=True)
    role=models.CharField(max_length=200,default='player')

    def __str__(self):
        return self.name

class Team(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Match(models.Model):
    team1=models.ForeignKey(Team,on_delete=models.CASCADE,related_name='team1')
    team2=models.ForeignKey(Team,on_delete=models.CASCADE,related_name='team2')
    date=models.DateField()
    venue=models.CharField(max_length=500)
    status=models.CharField(max_length=200,default='upcoming')

    def __str__(self):
        return f'{self.team1} vs {self.team2}'
    
    class Meta:
        unique_together = ['team1', 'team2', 'date']