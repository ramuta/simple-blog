from google.appengine.ext import ndb


class BlogPost(ndb.Model):
	title = ndb.StringProperty()
	text = ndb.TextProperty()
	author = ndb.StringProperty()
	datetime = ndb.DateTimeProperty(auto_now_add=True)

	@property
	def get_id(self):
		return self.key().id

	@classmethod
	def create(cls, title, text):
		post = cls(title=title,
		           text=text,
		           author="Matt Ramuta")
		post.put()