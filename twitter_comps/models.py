from django.db import models
from django.contrib.auth.models import User

DEFAULT_PROFILEIMG_URL = "https://cdn.business2community.com/wp-content/uploads/2017/08/blank-profile-picture-973460_640.png"

class Profile(models.Model):
	user = models.OneToOneField(User, related_name="user_profile", on_delete=models.CASCADE)
	first_name = models.CharField(max_length=100, blank=True, null=True)
	last_name = models.CharField(max_length=100, blank=True, null=True)
	description = models.CharField(max_length=200, blank=True, null=True)
	profile_picture = models.ImageField(default = DEFAULT_PROFILEIMG_URL, blank=True, null=True)
	followers = models.ManyToManyField("Profile", blank=True)
	posts = models.ManyToManyField("Post", blank=True)

	def __str__(self):
		return self.user.username

class Post(models.Model):
	text = models.CharField(max_length=200)
	poster = models.ForeignKey(Profile, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	likes = models.ManyToManyField("Like", blank=True)
	comments = models.ManyToManyField("Comment", blank=True)

	def __str__(self):
		return self.text


class Like(models.Model):
	liker = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return self.liker.user.username


class Comment(models.Model):
	comment_text = models.CharField(max_length=200, blank=True, default="")
	commenter = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
	for_post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
	commented_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)

	class Meta:
		ordering = ['-commented_on']

	def __str__(self):
		return self.commenter.user.username


class Retweet(models.Model):
	reetweeter = models.ForeignKey(Profile, related_name="reetweeter", on_delete=models.CASCADE, null=True, blank=True)
	caption = models.CharField(max_length=200, blank=True)
	tweet = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
	tweet_author = models.ForeignKey(Profile, related_name="tweet_author", on_delete=models.CASCADE, null=True, blank=True)
	date_of_retweet = models.DateTimeField(auto_now_add=True, null=True, blank=True)

	class Meta:
		ordering = ['-date_of_retweet']
	
	def __str__(self):
		return  "retweeted by: " + self.reetweeter.user.username + ", tweet: " + self.tweet.text