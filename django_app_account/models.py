import importlib.util
import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

from django_app_core.models import CommonDateAndSafeDeleteMixin

DJANGO_APP_ROLE_INSTALLED = importlib.util.find_spec("django_app_role") is not None
if DJANGO_APP_ROLE_INSTALLED:
    from django_app_role import ProtectedRole
    from django_app_role.models import Role


class UserManager(BaseUserManager):
    pass


class User(CommonDateAndSafeDeleteMixin, AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    endpoint = models.CharField(max_length=10, db_index=True, blank=True, null=True)
    email = models.EmailField(
        verbose_name="email address", max_length=255, unique=False, db_index=True
    )
    username = models.CharField(max_length=255, db_index=True)
    email_verified = models.BooleanField(default=False)

    if DJANGO_APP_ROLE_INSTALLED:
        roles = models.ManyToManyField(Role)

    objects = UserManager()

    _safedelete_policy = SOFT_DELETE_CASCADE

    USERNAME_FIELD = "email"

    class Meta:
        db_table = "app_account_user"
        index_together = (
            ("endpoint", "email"),
            ("endpoint", "username"),
        )
        ordering = ["email"]

    def __str__(self):
        return str(self.id)

    @property
    def is_hq_user(self) -> bool:
        if DJANGO_APP_ROLE_INSTALLED:
            return self.roles.filter(slug=ProtectedRole.HQUser).exists()
        else:
            return False

    @property
    def is_admin(self) -> bool:
        if DJANGO_APP_ROLE_INSTALLED:
            return self.roles.filter(slug=ProtectedRole.Admin).exists()
        else:
            return False

    @property
    def is_collaborator(self) -> bool:
        if DJANGO_APP_ROLE_INSTALLED:
            return self.roles.filter(slug=ProtectedRole.Collaborator).exists()
        else:
            return False

    @property
    def is_customer(self) -> bool:
        if DJANGO_APP_ROLE_INSTALLED:
            return self.roles.filter(slug=ProtectedRole.Customer).exists()
        else:
            return False

    @property
    def is_manager(self) -> bool:
        if DJANGO_APP_ROLE_INSTALLED:
            return self.roles.filter(slug=ProtectedRole.Manager).exists()
        else:
            return False

    @property
    def is_member(self) -> bool:
        if DJANGO_APP_ROLE_INSTALLED:
            return self.roles.filter(slug=ProtectedRole.Member).exists()
        else:
            return False

    @property
    def is_owner(self) -> bool:
        if DJANGO_APP_ROLE_INSTALLED:
            return self.roles.filter(slug=ProtectedRole.Owner).exists()
        else:
            return False

    @property
    def is_partner(self) -> bool:
        if DJANGO_APP_ROLE_INSTALLED:
            return self.roles.filter(slug=ProtectedRole.Partner).exists()
        else:
            return False

    @property
    def is_staff(self) -> bool:
        if DJANGO_APP_ROLE_INSTALLED:
            return self.roles.filter(slug=ProtectedRole.Staff).exists()
        else:
            return False


class Profile(SafeDeleteModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, models.CASCADE)
    name = models.CharField(max_length=255, db_index=True, blank=True, null=True)
    mobile = models.CharField(max_length=255, db_index=True, blank=True, null=True)
    birth = models.DateField(null=True)

    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        db_table = "app_account_profile"


class PasswordReset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, models.CASCADE)
    token = models.CharField(max_length=255, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "app_account_password_reset"
        index_together = (("user", "token", "created_at"),)
        ordering = ["id"]

    def __str__(self):
        return str(self.id)
