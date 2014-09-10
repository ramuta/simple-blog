import unittest

from google.appengine.ext import ndb

from ndbtestcase import AppEngineTestCase
from blog.models import BlogPost


class Thing(ndb.Model):
    stuff = ndb.StringProperty()


class ATestCase(AppEngineTestCase):
    """Example App Engine testcase"""

    def test_thing_exists(self):
        self.thing = Thing(stuff="Hi")
        self.thing.put()
        self.assertEquals(Thing.query().count(), 1)

    def test_blog_post_create(self):
        post = BlogPost.create(title="test", content="testing", author="test@test.si")
        self.assertEquals(post.title, "test")


if __name__ == '__main__':
    unittest.main()
