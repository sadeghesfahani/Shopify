from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, user_type, password=None, ):
        if not email:
            raise ValueError('Students must have email')
        user = self.model(email=self.normalize_email(email),
                          first_name=first_name,
                          last_name=last_name,
                          user_type=user_type,
                          username=email,
                          )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, user_type, password=None):
        if not email:
            raise ValueError('Students must have email')
        user = self.model(email=self.normalize_email(email),
                          first_name=first_name,
                          last_name=last_name,
                          user_type=user_type,
                          )
        user.set_password(password)
        user.username = user.email
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    CUSTOMER = 0
    ADMIN = 1
    DEPARTMENT_ADMIN = 2
    MAIN_DEPARTMENT = 3
    first_name = models.CharField(max_length=60,null=True, blank=True)
    last_name = models.CharField(max_length=100,null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True)
    last_login = models.DateTimeField(auto_now=True)
    email = models.EmailField(max_length=255, unique=True)
    TYPES = [(CUSTOMER, 'costumer'), (ADMIN, 'admin'), (DEPARTMENT_ADMIN, 'department admin')]
    user_type = models.PositiveSmallIntegerField(choices=TYPES, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_department_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_type']
    objects = CustomUserManager()

    def __str__(self):
        return self.first_name

    def save(self, *args, **kwargs):
        if self.user_type == User.ADMIN:
            self.promoteUserToAdmin()
        elif self.user_type == User.DEPARTMENT_ADMIN:
            self.promoteUserToDepartmentAdmin()
        super(User, self).save(*args, **kwargs)

    def promoteUserToAdmin(self):
        self.is_superuser = True
        self.is_staff = True
        self.is_admin = True

    def promoteUserToDepartmentAdmin(self):
        self.is_staff = True
        self.is_department_admin = True


class Address(models.Model):
    address = models.CharField(max_length=400, blank=False, null=False)
    postal_code = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_address')
