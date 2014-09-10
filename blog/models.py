from google.appengine.ext import ndb


class BlogPost(ndb.Model):
	title = ndb.StringProperty()
	content = ndb.TextProperty()
	author = ndb.StringProperty()
	datetime = ndb.DateTimeProperty(auto_now_add=True)

	@property
	def get_id(self):
		return self.key().id

	@classmethod
	def create(cls, title, content, author):
		post = cls(title=title,
		           content=content,
		           author=author)
		post.put()