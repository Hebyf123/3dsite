from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Пользователь должен иметь адрес электронной почты")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  
    name = models.CharField(max_length=80, verbose_name=_("Имя"), blank=True, null=True)
    surname = models.CharField(max_length=80, verbose_name=_("Фамилия"), blank=True, null=True)
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True, verbose_name=_("Фото"))
    telegram_id = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Telegram ID"))
    country = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Страна"))
    city = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Город"))
    address = models.CharField(max_length=255, blank=True, db_index=True, null=True, verbose_name=_("Адрес"))
    phone = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Телефон"))
    oauth_provider = models.CharField(max_length=50, blank=True, null=True)
    oauth_uid = models.CharField(max_length=255, blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)
    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = []  
    objects = CustomUserManager()  

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        elif not self.email:
            self.email = self.username
        
        super().save(*args, **kwargs)
