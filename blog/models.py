from django.utils.datetime_safe import datetime
from google.appengine.ext import ndb


class BlogPost(ndb.Model):
	title = ndb.StringProperty()
	content = ndb.TextProperty()
	author = ndb.StringProperty()
	datetime = ndb.DateTimeProperty(auto_now_add=True)
	changed = ndb.DateTimeProperty(auto_now=True)

	@property
	def get_id(self):
		return self.key().id

	@classmethod
	def create(cls, title, content, author):
		post = cls(title=title,
		           content=content,
		           author=author)
		post.put()

	@classmethod
	def edit(cls, post_id, title, content):
		post = BlogPost.get_by_id(int(post_id))
		post.title = title
		post.content = content
		post.changed = datetime.now()
		post.put()