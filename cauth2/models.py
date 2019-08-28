from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _


class ChatUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, is_staff):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password):
        return self._create_user(email=email, password=password, is_staff=False)

    def create_superuser(self, email, password):
        return self._create_user(email=email, password=password, is_staff=True)

# Create your models here.


class ChatUser(AbstractBaseUser):
    # email is going to be used as instead of username field
    email = models.EmailField(blank=False, max_length=255, null=False, unique=True)

    first_name = models.CharField(blank=True, max_length=255, null=True)
    last_name = models.CharField(blank=True, max_length=255, null=True)

    # Below two fields are required in order to access django admin
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = ChatUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name

    # Methods below are required to login super user from admin panel
    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff