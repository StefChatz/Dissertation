from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from multiselectfield import MultiSelectField

class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError("Users must have an email address")
		if not username:
			raise ValueError("Users must have an username")

		user  = self.model(
				email=self.normalize_email(email),
				username=username,
			)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user  = self.create_user(
				email=self.normalize_email(email),
				password=password,
				username=username,
			)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

CHOICES = (
	('games', 'GAMES'),
	('social', 'SOCIAL'),
	('music', 'MUSIC'),
	('news', 'NEWS'),
	('finance', 'FINANCE'),
	('movies', 'MOVIES'),
	('sports', 'SPORTS'),
	('travel', 'TRAVEL'),
	('automotive', 'AUTOMOTIVE'),
	('leisure', 'LEISURE'))
class Account(AbstractBaseUser):
	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
	username 				= models.CharField(max_length=30, unique=True)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)
	interests				= MultiSelectField(choices = CHOICES)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', ]

	objects = MyAccountManager()

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True

    # GAMES = 'GAMES'
    # SOCIAL = 'SOCIAL'
    # MUSIC = 'MUSIC'
    # NEWS = 'NEWS'
    # FINANCE = 'FINANCE'
    # MOVIES = 'MOVIES'
    # SPORTS = 'SPORTS'
    # TRAVEL = 'TRAVEL'
    # AUTOMOTIVE = 'AUTOMOTIVE'
    # LEISURE = 'LEISURE'



# COLOR_CHOICES = (
# 	('GAMES', 'Games'),
# 	('SOCIAL', 'Social Networking'),
# 	('MUSIC', 'Music'),
# 	('NEWS', 'Breaking News'),
# 	('FINANCE', 'Finance'),
# 	('MOVIES', 'Movies'),
# 	('SPORTS', 'Sports'),
# 	('TRAVEL', 'Travel'),
# 	('AUTOMOTIVE', 'Automotive'),
# 	('LEISURE', 'Leisure')
# )
