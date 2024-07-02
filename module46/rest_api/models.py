from django.db import models # type: ignore
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser # type: ignore

# class User(models.Model):
#     first_name= models.CharField(max_length=255)
#     last_name=models.CharField(max_length=255)
#     userName= models.CharField(max_length=255,unique=True)
#     email=models.EmailField(max_length=255, unique=True)
#     mobile_no=models.IntegerField(unique=True)
#     password=models.CharField(max_length=10)


   
# class userManager(BaseUserManager):
#     def create_user(self,username,password,**extra_fields):
#         if not username:
#             raise ValueError("Username should be provided")
#         user = self.model(username=username,**extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
        

   
           
#     # always create superuser through cmd alone- python manahe.py createsuperuser
#     # don't create end point(API) for creating superuser because then anyone will create and 
#     # cause issue- so always create super user only through terminal cmd
    
    
#     def create_superuser(self,username,password,**extra_fields):
#         extra_fields.setdefault('is_staff',True)
#         extra_fields.setdefault('is_superuser',True)
#         return self.create_user(username,password,**extra_fields)
     
# class UserModel (AbstractBaseUser): # This is polymorphism concept
#     id = models.AutoField (primary_key=True)
#     name = models.CharField(max_length=100,default="default_username")
#     email = models.CharField (max_length=60)
#     password = models.CharField (max_length=200)
#     username = models.CharField(max_length=255, unique=True,default="default_username")
#     is_active=models.BooleanField(default=False)
#     is_staff=models.BooleanField(default=False)
#     is_superuser=models.BooleanField(default=False)

#     USERNAME_FIELD = 'username'

#     objects = userManager()
    
#     #These 2 are not mentioned in lms, by b67 recordings - to avoid permission error in django
#     # web access( www.localhost:8000/admin/)
    

#     def has_perm(self,param,obj=None):
#         return self.is_superuser
    
#     def has_module_perms(self,app_label):
#         return self.is_superuser


  
class UserManager (BaseUserManager):

    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError("Email is not set")
        email= self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
        
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        return self.create_user(email,password,**extra_fields) #again calls above create_user method
    
class UserModel (AbstractBaseUser):
    id = models.AutoField (primary_key=True)
    name = models.CharField(max_length=100,default="default_username")
    email = models.CharField (max_length=60)
    password = models.CharField (max_length=300)
    username = models.CharField(max_length=255, unique=True,default="default_username")
#     is_active=models.BooleanField(default=False)
#     is_staff=models.BooleanField(default=False)
#     is_superuser=models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = UserManager()
    
    
#     #These 2 are not mentioned in lms, by b67 recordings - to avoid permission error in django
#     # web access( www.localhost:8000/admin/)
    


    def has_perm(self,param,obj=None):
        return self.is_superuser
    
    def has_module_perms(self,app_label):
        return self.is_superuser


class Invoice(models.Model):
    invoice_id=models.IntegerField()
    client_name = models.CharField(max_length=255)
    date = models.DateField()
    
class Item(models.Model):

    invoice=models.ForeignKey(Invoice,on_delete=models.CASCADE,related_name="items") # one to many relationship- to invoice
    # related_name = items- > items is array name in data.py
    desc=models.TextField()
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=10,decimal_places=2)
    