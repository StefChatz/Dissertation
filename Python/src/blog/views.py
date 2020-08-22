from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from django.db.models import F

from blog.models import BlogPost
from blog.forms import CreateBlogPostForm, UpdateBlogPostForm
from account.models import Account


def create_blog_view(request):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

	form = CreateBlogPostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		author = Account.objects.filter(email=request.user.email).first()
		obj.author = author
		obj.save()
		form = CreateBlogPostForm()
	context['choices_form'] = form
	context['form'] = form
	return render(request, 'blog/create_blog.html', context)



def detail_blog_view(request, slug):

	context = {}
	blog_post = get_object_or_404(BlogPost, slug=slug)
	context['blog_post'] = blog_post

	return render(request, 'blog/detail_blog.html', context)


def edit_blog_view(request, slug):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

	blog_post = get_object_or_404(BlogPost, slug=slug)

	if blog_post.author != user:
		return HttpResponse("You are not the author of that post.")

	if request.POST:
		form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			blog_post = obj

	form = UpdateBlogPostForm(
			initial={
					"title": blog_post.title,
					"body": blog_post.body,
					"image": blog_post.image,
					"interests": blog_post.interests,
				}
			)
	context['form'] = form
	if request.method == 'POST':
		form = UpdateBlogPostForm(request.POST, instance=request.user)
		if form.is_valid():
			choices = form.cleaned_data.get('interests')
			print(choices)
			# for choice in choices:

			form.initial = {
				"interests" : request.POST['interests']
			}
			print("test")
		else:
			form = UpdateBlogPostForm(
			instance=request.user
			)

	context['choices_form'] = form

	return render(request, 'blog/edit_blog.html', context)

def get_blog_queryset(user, query=None):
	base = 1

	queryset = []
	queries = query.split(" ")
	for q in queries:
		# BlogPost.objects.update(post_score=F('post_score') + 1)

		posts = BlogPost.objects.filter(
			Q(title__contains=q)|
			Q(body__icontains=q)
			).annotate(weight = F('date_published')).distinct()
		for post in posts:
			queryset.append(post)

	# Gets the list of penalized words.
	penalty_list = open('penalty_list.txt').read().splitlines()

	# Checks if the user is authenticated.
	if user.is_authenticated:
		for q in queryset:

			# A list of common interests.
			common_result = []
			# A list of non-common interests.
			non_common_result = []
			# Set's the score to the time a post is updated.
			q.post_score = q.date_updated.timestamp()

			for element in q.interests:
				# Updates based on common interests.
				if element in user.interests:
					common_result.append(element)
					q.post_score = q.post_score * (len(common_result) * 5)

				# Updates based on common interests.
				if element not in user.interests:
					non_common_result.append(element)
					q.post_score = q.post_score / (len(non_common_result) * 2)

				# Updates based on non-common interests.
				if q.title in profanity_list or q.body in profanity_list:
					for penalty in penalty_list:
						q.post_score = q.post_score / (len(penalty_list) * 5)

	return list(set(queryset))
