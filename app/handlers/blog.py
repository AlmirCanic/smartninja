import os
import sys
from google.appengine.api import users
from app.handlers.base import Handler
from app.models.auth import User
from app.models.blog import BlogPost
from app.utils.decorators import admin_required

sys.path.append(os.path.join(os.path.dirname(__file__), '../../libs'))

import markdown2


class PublicBlogHandler(Handler):
    def get(self):
        posts = BlogPost.query(BlogPost.deleted == False).order(-BlogPost.created).fetch()

        # convert markdown to html
        posts2 = []
        markdowner = markdown2.Markdown()

        for post in posts:
            post.text = post.text[:500] + "..."
            post.text = markdowner.convert(post.text)
            posts2.append(post)

        params = {"posts": posts2}
        self.render_template("public/blog.html", params)


class AdminBlogListHandler(Handler):
    @admin_required
    def get(self):
        posts = BlogPost.query(BlogPost.deleted == False).order(-BlogPost.created).fetch()
        params = {"posts": posts}
        self.render_template("admin/blog_list.html", params)


class AdminBlogAddHandler(Handler):
    @admin_required
    def get(self):
        self.render_template("admin/blog_add.html")

    @admin_required
    def post(self):
        title = self.request.get("title")
        slug = self.request.get("slug")
        image = self.request.get("image")
        text = self.request.get("text")
        user = User.get_by_email(users.get_current_user().email())
        if title and slug and image and text:
            BlogPost.create(title=title, slug=slug, cover_image=image, text=text, author_id=user.get_id, author_name=user.get_full_name)
        self.redirect_to("admin-blog-list")


class AdminBlogDetailsHandler(Handler):
    @admin_required
    def get(self, post_id):
        post = BlogPost.get_by_id(int(post_id))

        # markdown
        markdowner = markdown2.Markdown()
        post.text = markdowner.convert(post.text)

        params = {"post": post}
        self.render_template("admin/blog_post_details.html", params)


class AdminBlogEditHandler(Handler):
    @admin_required
    def get(self, post_id):
        post = BlogPost.get_by_id(int(post_id))
        params = {"post": post}
        self.render_template("admin/blog_post_edit.html", params)

    @admin_required
    def post(self, post_id):
        title = self.request.get("title")
        slug = self.request.get("slug")
        image = self.request.get("image")
        text = self.request.get("text")
        if title and slug and image and text:
            post = BlogPost.get_by_id(int(post_id))
            BlogPost.update(blog_post=post, title=title, slug=slug, cover_image=image, text=text)
        self.redirect_to("admin-blog-details", post_id=post_id)


class AdminBlogDeleteHandler(Handler):
    @admin_required
    def get(self, post_id):
        post = BlogPost.get_by_id(int(post_id))
        params = {"post": post}
        self.render_template("admin/blog_post_delete.html", params)

    @admin_required
    def post(self, post_id):
        post = BlogPost.get_by_id(int(post_id))
        post.deleted = True
        post.put()
        self.redirect_to("admin-blog-list")