from google.appengine.ext import ndb


class BlogPost(ndb.Model):
    title = ndb.StringProperty()
    slug = ndb.StringProperty(default="none")
    text = ndb.TextProperty()
    author_name = ndb.StringProperty()
    author_id = ndb.IntegerProperty()
    cover_image = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)

    @property
    def get_id(self):
        return self.key.id()

    @classmethod
    def create(cls, title, slug, text, author_name, author_id, cover_image):
        post = cls(title=title,
                   slug=slug,
                   text=text,
                   author_name=author_name,
                   author_id=author_id,
                   cover_image=cover_image)
        post.put()

    @classmethod
    def update(cls, blog_post, title, slug, text, cover_image):
        blog_post.title = title
        blog_post.slug = slug
        blog_post.text = text
        blog_post.cover_image = cover_image
        blog_post.put()
        return blog_post