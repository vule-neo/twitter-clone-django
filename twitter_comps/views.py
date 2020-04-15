from django.shortcuts import render, redirect
from .forms import CreateUserForm, ProfileEditForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.db.models import Q


def landing(request):
	return render(request, "landing.html")

def home(request):
	current_profile = Profile.objects.get(user=request.user)
	all_posts = Post.objects.all().order_by("-date")
	all_retweets = Retweet.objects.all()

	# if post: create a new tweet with all the elements assigned
	if request.method == "POST":
		tweet_text = request.POST.get("tweet-text")
		new_post = Post(text=tweet_text, poster=current_profile)
		if new_post not in Post.objects.all():
			new_post.save()
			current_profile.posts.add(new_post)
			return redirect("twitter_comps:home")
		else:
			return redirect("twitter_comps:home")

	context = {
		"current_profile": current_profile,
		"all_posts": all_posts,
		"all_retweets":all_retweets,
	}
	return render(request, "home.html", context)

def registration_page(request):
	form = CreateUserForm()

	# if post: get all the input elements and stuff it into the form, creating a new user
	if request.method == "POST":
		username = request.POST.get("username")
		email = request.POST.get("email")
		password1 = request.POST.get("password1")
		password2 = request.POST.get("password2")
		user_info = {"username":username, "email":email, "password1":password1, "password2":password2}

		form = CreateUserForm(user_info)

		if form.is_valid():
			form.save()
			user = authenticate(username=username, password=password1)
			login(request, user)
			return redirect("/")

	return render(request, "register.html")

def login_page(request):
	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")
		if authenticate(username=username, password=password):
			user = authenticate(username=username, password=password)
			login(request, user)
		else:
			return redirect("twitter_comps:login_page")
		return redirect("twitter_comps:home")



	return render(request, "login.html")

def logout_page(request):
	logout(request)
	return redirect("twitter_comps:login_page")

def profile_view(request, id):
	# gets everything needed for profile page, and puts it into a dict
	retweets = Retweet.objects.all()
	profile = Profile.objects.get(id=id)
	users_posts = Post.objects.filter(poster=profile)
	current_profile = Profile.objects.get(user=request.user)
	all_followers = profile.followers.all()

	# check if current user is in followers, to later use it in the template with the
	# follow/unfollow mechanisam

	da = False

	if profile.followers.filter(user=request.user).exists():
		da = True
	else:
		da = False

	context = {
		"profile":profile,
		"users_posts":users_posts,
		"retweets": retweets,
		"all_followers":all_followers,
		"da":da
	}
	return render(request, "profile_page.html", context)

def edit_profile(request, id):
	# just the form used to edit your profile
	profile = Profile.objects.get(id=id)
	form = ProfileEditForm()
	if request.method == "POST":
		form = ProfileEditForm(request.POST, request.FILES, instance=profile)
		if form.is_valid:
			form.save()
			return redirect("twitter_comps:profile_view", profile.id)
		else:
			return redirect("twitter_comps:profile_view", profile.id)
	context = {
		"profile":profile,
		"form":form
	}
	return render(request, "edit_profile.html", context)

def delete_post(request, id):
	post = Post.objects.get(id=id)
	post.delete()
	return redirect("/")

def like_post(request, id):
	# adds a like to the selected post, checks if post is already liked by user, if so unlike
	post = Post.objects.get(id=id)
	all_post_likes = post.likes.all().values_list("liker", flat=True)
	current_profile = Profile.objects.get(user=request.user)
	
	like = Like(liker=current_profile)
	if like.liker.id not in all_post_likes:
		like.save()
		post.likes.add(like)
		return redirect("twitter_comps:home")
	else:
		already_liked = post.likes.get(liker=current_profile)
		post.likes.remove(already_liked)
		return redirect("twitter_comps:home")

def view_likes(request, id):
	# renders the page that shows everyone who liked the post
	post = Post.objects.get(id=id)
	post_likes = post.likes.all()
	context = {
		"post":post,
		"post_likes":post_likes,
	}
	return render(request, "view_likes.html", context)

def comment_post(request, id):
	# gets input from template and creates comment object, saves it to the db
	post = Post.objects.get(id=id)
	profile = Profile.objects.get(user=request.user)
	if request.POST.get("comment-input"):
		comment_text = request.POST.get("comment-input")
		new_comment = Comment(comment_text=comment_text, commenter=profile, for_post=post)
		new_comment.save()
		post.comments.add(new_comment)
		return redirect("twitter_comps:home")
	else:
		return redirect("twitter_comps:home")


def delete_comment(request, id):
	comment = Comment.objects.get(id=id)
	comment.delete()
	return redirect("twitter_comps:home")


def retweet(request, id):
	# gets the post, creates a retweet with the user that retweets it, and the post instance
	post = Post.objects.get(id=id)
	current_profile = Profile.objects.get(user=request.user)
	new_retweet = Retweet(reetweeter=current_profile, tweet=post, tweet_author=post.poster)
	# if post isn't already retweeted, save
	if new_retweet not in Retweet.objects.all():
		new_retweet.save()
		return redirect("twitter_comps:home")
	else:
		return redirect("twitter_comps:home")

def add_follower(request, id):
	# adds the current profile to the followers list of the profile, if current profile
	# already in followers, delete it from followers
	profile = Profile.objects.get(id=id)
	current_profile = Profile.objects.get(user=request.user)
	if current_profile not in profile.followers.all():
		profile.followers.add(current_profile)
		return redirect("twitter_comps:profile_view", id=profile.id)

	else:
		profile.followers.remove(current_profile)
		return redirect("twitter_comps:profile_view", id=profile.id)

def view_users(request):
	# renders a page with all the users, including a search mechanisam
	profiles = Profile.objects.all()
	context = {
		"profiles":profiles,
	}
	if request.method == "POST":
		# gets the searchbar input, creates search result queryset and adds it to the context
		search = request.POST.get("search")
		search_result = Profile.objects.filter(
				Q(user__username__icontains=search)
			)
		context["search_result"] = search_result
		context["search"] = search
	

		return render(request, "profiles_view.html", context)
	else:
		return render(request, "profiles_view.html", context)