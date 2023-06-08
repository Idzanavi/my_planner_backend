from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from my_planner.range_integer_field import RangeIntegerField

class User(AbstractUser):
    GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Female'),
        (0, ''),
    )
    gender = models.IntegerField(choices=GENDER_CHOICES, verbose_name="Gender", null=True)
    birthdate = models.DateField(verbose_name="BirthDate", null=True)

    def _getGenderName(self):
        if self.gender == 1:
            return "Male"
        elif self.gender == 2:
            return "Female"
        else:
            return ""

    def __str__(self):
        return "[{id}] {name} [{firstname} {lastname}] ({email}): {birthdate}/{gender}".format(
                                                                                          id=self.pk,
                                                                                          name=self.username,
                                                                                          firstname=self.first_name,
                                                                                          lastname=self.last_name,
                                                                                          email=self.email,
                                                                                          birthdate=self.birthdate,
                                                                                          gender=self._getGenderName())


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):

        if not username:
            raise ValueError('Users must have a name')
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.save(using=self._db)
        return user


class PlannerItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='planner_items')
    week_no = models.IntegerField(verbose_name="WeekNo", null=True)
    day_no = RangeIntegerField(min_value=0, max_value=6, verbose_name="DayNo", null=True)
    slot_no = RangeIntegerField(min_value=0, max_value=15, verbose_name="SlotNo", null=True)
    title = models.CharField(max_length=128, verbose_name="Title", null=True)
    text = models.TextField(verbose_name="Text", null=True)
    color = models.CharField(max_length=16, verbose_name="Color", null=True)

    class Meta:
            constraints = [
                models.UniqueConstraint(fields=['user', 'week_no', 'day_no', 'slot_no'], name="Item should be unique")
            ]

    def __str__(self):
        return "[{pk} {week_no}: {day_no}/{slot_no}]: {title} ({color})".format(
                                                                           pk = self.pk,
                                                                           week_no=self.week_no,
                                                                           day_no=self.day_no,
                                                                           slot_no=self.slot_no,
                                                                           title=self.title,
                                                                           color=self.color)


