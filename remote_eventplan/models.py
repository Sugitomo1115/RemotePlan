from pyexpat import model
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
import uuid as uuid_lib
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    """ユーザーマネージャー."""
  
    use_in_migrations = True
  
    def _create_user(self, email, password, **extra_fields):
        """Create and save a user with the given username, email, and
        password."""
        if not email:
            raise ValueError('メールアドレスを入力してください')
        email = self.normalize_email(email)
  
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
  
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
  
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
  
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
  
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """ユーザー AbstractBaseUserを継承"""

    id = models.UUIDField(default=uuid_lib.uuid4,
                            primary_key=True, editable=False)
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'ユーザー名は150文字以内 記号は @/./+/-/_ のみ可能です'),
        validators=[username_validator],
        error_messages={
            'unique': _("このユーザー名は既に使われています。"),
        },
    )

    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in
        between."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
  
    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

class Plan(models.Model):
    """企画テンプレート"""
    name = models.CharField(max_length=100, default="名無し")
    target = models.CharField(max_length=20, default="誰でも")
    person = models.CharField(max_length=20, default="指定なし")
    category1 = models.CharField(max_length=30, default="その他")
    category2 = models.CharField(max_length=30, default="なし")
    time = models.CharField(max_length=100, default="指定なし")
    tools = models.CharField(max_length=100, default="指定なし")
    help = models.CharField(max_length=100, default="特になし")
    outline = models.CharField(max_length=200, default="特になし")
    posted_at = models.DateTimeField('date published')
    like_num = models.IntegerField(default=0)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE)

class Like(models.Model):
    """イイねモデル"""
    post_user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

class Category(models.Model):
    """カテゴリーモデル"""
    category_name = models.CharField(max_length=30, default="なし", unique=True)