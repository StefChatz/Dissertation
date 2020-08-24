from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from multiselectfield import MultiSelectField

def upload_location(instance, filename):
	file_path = 'blog/{author_id}/{title}-{filename}'.format(
				author_id=str(instance.author.id),title=str(instance.title), filename=filename)
	return file_path

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
class BlogPost(models.Model):
	title 					= models.CharField(max_length=50, null=False, blank=False)
	body 					= models.TextField(max_length=500, null=False, blank=False)
	image		 			= models.ImageField(upload_to=upload_location, null=True, blank=True)
	date_published 			= models.DateTimeField(auto_now_add=True, verbose_name="date published")
	date_updated 			= models.DateTimeField(auto_now=True, verbose_name="date updated")
	author 					= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	slug 					= models.SlugField(blank=True, unique=True)
	interests				= MultiSelectField(choices = CHOICES, default = "news")
	post_score				= models.IntegerField(default = 0)
	bad_words				= models.IntegerField(default = 0)

	# interest				= models.CharField(max_length=50, null=False, blank=False)
	# category_interest = models.CharField(
	# 	max_length=20,
	# 	choices=INTEREST_CHOICES,
	# 	        default='GAMES',
	# 			)
	#
	def __str__(self):
		return self.title

@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)

def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.author.username + "-" + instance.title)

pre_save.connect(pre_save_blog_post_receiver, sender=BlogPost)
