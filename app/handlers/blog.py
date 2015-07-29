from google.appengine.api import users
from google.appengine.datastore.datastore_query import Cursor
from app.handlers.base import Handler
from app.models.auth import User
from app.models.blog import BlogPost
from app.models.franchise import Franchise
from app.models.instructor import Instructor
from app.models.manager import Manager
from app.utils.decorators import admin_required, instructor_required, manager_required
from app.utils.other import strip_tags, convert_markdown_to_html, logga


# PUBLIC
class PublicBlogHandler(Handler):
    def get(self):
        curs = Cursor(urlsafe=self.request.get('page'))
        posts, next_curs, more = BlogPost.query(BlogPost.deleted == False).order(-BlogPost.created).fetch_page(10, start_cursor=curs)

        # convert markdown to html
        posts2 = []

        for post in posts:
            post.text = convert_markdown_to_html(post.text)
            post.text = strip_tags(post.text)[:500] + "..."
            posts2.append(post)

        params = {"posts": posts2}

        if more and next_curs:
            params["next"] = next_curs.urlsafe()

        return self.render_template("public/blog.html", params)


class PublicBlogDetailsHandler(Handler):
    def get(self, post_slug):
        post = BlogPost.query(BlogPost.slug == str(post_slug)).get()
        posts = BlogPost.query(BlogPost.deleted == False).order(-BlogPost.created).fetch(5)
        post.text = convert_markdown_to_html(post.text)
        summary = strip_tags(post.text.replace('\"', ""))[:300]

        params = {"post": post, "posts": posts, "summary": summary}
        return self.render_template("public/blog_post.html", params)


# ADMIN
class AdminBlogListHandler(Handler):
    @admin_required
    def get(self):
        curs = Cursor(urlsafe=self.request.get('page'))
        posts, next_curs, more = BlogPost.query(BlogPost.deleted == False).order(-BlogPost.created).fetch_page(10, start_cursor=curs)

        params = {"posts": posts}

        if more and next_curs:
            params["next"] = next_curs.urlsafe()

        return self.render_template("admin/blog_list.html", params)


class AdminBlogAddHandler(Handler):
    @admin_required
    def get(self):
        authors = []
        current_user = User.get_by_email(users.get_current_user().email().lower())
        authors.append(current_user)
        instructors = Instructor.query().fetch()

        for instructor in instructors:
            some_user = User.get_by_id(instructor.user_id)
            authors.append(some_user)

        franchises = Franchise.query(Franchise.deleted == False).fetch()

        params = {"authors": authors, "franchises": franchises}
        return self.render_template("admin/blog_add.html", params=params)

    @admin_required
    def post(self):
        title = self.request.get("title")
        slug = self.request.get("slug")
        image = self.request.get("image")
        text = self.request.get("text")
        author_id = self.request.get("author")
        franchise_id = self.request.get("franchise")

        author = User.get_by_id(int(author_id))
        user = User.get_by_email(users.get_current_user().email().lower())

        franchise = Franchise.get_by_id(int(franchise_id))

        if title and slug and image and text:
            blogpost = BlogPost.create(title=title,
                                       slug=slug,
                                       cover_image=image,
                                       text=text,
                                       author_id=author.get_id,
                                       author_name=author.get_full_name,
                                       franchise=franchise)
            logga("Blog %s added by %s." % (blogpost.get_id, user.get_id))

        return self.redirect_to("admin-blog-list")


class AdminBlogDetailsHandler(Handler):
    @admin_required
    def get(self, post_id):
        post = BlogPost.get_by_id(int(post_id))
        post.text = convert_markdown_to_html(post.text)
        params = {"post": post}
        return self.render_template("admin/blog_post_details.html", params)


class AdminBlogEditHandler(Handler):
    @admin_required
    def get(self, post_id):
        post = BlogPost.get_by_id(int(post_id))

        authors = []
        current_user = User.get_by_email(users.get_current_user().email().lower())
        authors.append(current_user)
        instructors = Instructor.query().fetch()

        for instructor in instructors:
            some_user = User.get_by_id(instructor.user_id)
            authors.append(some_user)

        params = {"post": post, "authors": authors}
        return self.render_template("admin/blog_post_edit.html", params)

    @admin_required
    def post(self, post_id):
        title = self.request.get("title")
        slug = self.request.get("slug")
        image = self.request.get("image")
        text = self.request.get("text")
        author_id = self.request.get("author")

        author = User.get_by_id(int(author_id))
        user = User.get_by_email(users.get_current_user().email().lower())

        if title and slug and image and text:
            post = BlogPost.get_by_id(int(post_id))
            BlogPost.update(blog_post=post, title=title, slug=slug, cover_image=image, text=text)
            post.author_id = int(author_id)
            post.author_name = author.get_full_name
            post.put()
            logga("Blog %s edited by %s." % (post_id, user.get_id))

        return self.redirect_to("admin-blog-details", post_id=post_id)


class AdminBlogDeleteHandler(Handler):
    @admin_required
    def get(self, post_id):
        post = BlogPost.get_by_id(int(post_id))
        params = {"post": post}
        return self.render_template("admin/blog_post_delete.html", params)

    @admin_required
    def post(self, post_id):
        post = BlogPost.get_by_id(int(post_id))
        post.deleted = True
        post.put()
        logga("Blog %s deleted." % post_id)
        return self.redirect_to("admin-blog-list")


# MANAGER
class ManagerBlogListHandler(Handler):
    @manager_required
    def get(self):
        curr_user = users.get_current_user()
        manager = Manager.query(Manager.email == curr_user.email().lower()).get()

        curs = Cursor(urlsafe=self.request.get('page'))

        posts, next_curs, more = BlogPost.query(BlogPost.deleted == False,
                                                BlogPost.franchise_id == manager.franchise_id).order(-BlogPost.created).fetch_page(10, start_cursor=curs)

        params = {"posts": posts}

        if more and next_curs:
            params["next"] = next_curs.urlsafe()

        return self.render_template("manager/blog_list.html", params)


class ManagerBlogAddHandler(Handler):
    @manager_required
    def get(self):
        authors = []
        current_user = User.get_by_email(users.get_current_user().email().lower())
        authors.append(current_user)

        manager = Manager.query(Manager.email == current_user.email).get()

        instructors = Instructor.query(Instructor.franchises.franchise_id == manager.franchise_id).fetch()

        for instructor in instructors:
            some_user = User.get_by_id(instructor.user_id)
            authors.append(some_user)

        params = {"authors": authors}

        return self.render_template("manager/blog_add.html", params)

    @manager_required
    def post(self):
        title = self.request.get("title")
        slug = self.request.get("slug")
        image = self.request.get("image")
        text = self.request.get("text")

        manager = Manager.query(Manager.email == users.get_current_user().email().lower()).get()

        franchise = Franchise.get_by_id(manager.franchise_id)

        if title and slug and image and text:
            blogpost = BlogPost.create(title=title,
                                       slug=slug,
                                       cover_image=image,
                                       text=text,
                                       author_id=manager.user_id,
                                       author_name=manager.full_name,
                                       franchise=franchise)
            logga("Blog %s added." % blogpost.get_id)
        return self.redirect_to("manager-blog-list")


class ManagerBlogDetailsHandler(Handler):
    @manager_required
    def get(self, post_id):
        post = BlogPost.get_by_id(int(post_id))
        post.text = convert_markdown_to_html(post.text)
        params = {"post": post}
        return self.render_template("manager/blog_post_details.html", params)


class ManagerBlogEditHandler(Handler):
    @manager_required
    def get(self, post_id):
        post = BlogPost.get_by_id(int(post_id))

        manager = Manager.query(Manager.email == users.get_current_user().email().lower()).get()

        authors = []
        current_user = User.get_by_email(users.get_current_user().email().lower())
        authors.append(current_user)
        instructors = Instructor.query(Instructor.franchises.franchise_id == manager.franchise_id).fetch()

        for instructor in instructors:
            some_user = User.get_by_id(instructor.user_id)
            authors.append(some_user)

        params = {"post": post, "authors": authors}
        return self.render_template("manager/blog_post_edit.html", params)

    @manager_required
    def post(self, post_id):
        title = self.request.get("title")
        slug = self.request.get("slug")
        image = self.request.get("image")
        text = self.request.get("text")
        author_id = self.request.get("author")

        author = User.get_by_id(int(author_id))
        user = User.get_by_email(users.get_current_user().email().lower())

        manager = Manager.query(Manager.email == user.email).get()

        if title and slug and image and text:
            post = BlogPost.get_by_id(int(post_id))
            if manager.franchise_id == post.franchise_id:
                BlogPost.update(blog_post=post, title=title, slug=slug, cover_image=image, text=text)
                post.author_id = int(author_id)
                post.author_name = author.get_full_name
                post.put()
                logga("Blog %s edited by %s." % (post_id, user.get_id))

        return self.redirect_to("manager-blog-details", post_id=post_id)


class ManagerBlogDeleteHandler(Handler):
    @manager_required
    def get(self, post_id):
        post = BlogPost.get_by_id(int(post_id))
        params = {"post": post}
        return self.render_template("manager/blog_post_delete.html", params)

    @manager_required
    def post(self, post_id):
        manager = Manager.query(Manager.email == users.get_current_user().email().lower()).get()
        post = BlogPost.get_by_id(int(post_id))

        if manager.franchise_id == post.franchise_id:
            post.deleted = True
            post.put()
            logga("Blog %s deleted." % post_id)

        return self.redirect_to("manager-blog-list")


# INSTRUCTOR
class InstructorBlogListHandler(Handler):
    @instructor_required
    def get(self):
        curs = Cursor(urlsafe=self.request.get('page'))
        posts, next_curs, more = BlogPost.query(BlogPost.deleted == False).order(-BlogPost.created).fetch_page(10, start_cursor=curs)

        params = {"posts": posts}

        if more and next_curs:
            params["next"] = next_curs.urlsafe()

        return self.render_template("instructor/blog_list.html", params)


class InstructorBlogAddHandler(Handler):
    @instructor_required
    def get(self):
        instructor = Instructor.query(Instructor.email == users.get_current_user().email().lower()).get()
        params = {"instructor": instructor}
        return self.render_template("instructor/blog_add.html", params)

    @instructor_required
    def post(self):
        title = self.request.get("title")
        slug = self.request.get("slug")
        image = self.request.get("image")
        text = self.request.get("text")
        franchise_id = self.request.get("franchise")

        user = User.get_by_email(users.get_current_user().email().lower())

        franchise = Franchise.get_by_id(int(franchise_id))

        if title and slug and image and text:
            blogpost = BlogPost.create(title=title,
                                       slug=slug,
                                       cover_image=image,
                                       text=text,
                                       author_id=user.get_id,
                                       author_name=user.get_full_name,
                                       franchise=franchise)
            logga("Blog %s added." % blogpost.get_id)
        return self.redirect_to("instructor-blog-list")


class InstructorBlogDetailsHandler(Handler):
    @instructor_required
    def get(self, post_id):
        post = BlogPost.get_by_id(int(post_id))
        post.text = convert_markdown_to_html(post.text)
        can_edit = False
        user = User.get_by_email(users.get_current_user().email().lower())
        if post.author_id == user.get_id:
            can_edit = True
        params = {"post": post, "can_edit": can_edit}
        return self.render_template("instructor/blog_post_details.html", params)


class InstructorBlogEditHandler(Handler):
    @instructor_required
    def get(self, post_id):
        post = BlogPost.get_by_id(int(post_id))
        params = {"post": post}
        user = User.get_by_email(users.get_current_user().email().lower())
        if post.author_id == user.get_id:
            return self.render_template("instructor/blog_post_edit.html", params)
        else:
            return self.redirect_to("forbidden")

    @instructor_required
    def post(self, post_id):
        title = self.request.get("title")
        slug = self.request.get("slug")
        image = self.request.get("image")
        text = self.request.get("text")

        if title and slug and image and text:
            post = BlogPost.get_by_id(int(post_id))

            user = User.get_by_email(users.get_current_user().email().lower())
            if post.author_id == user.get_id:
                BlogPost.update(blog_post=post, title=title, slug=slug, cover_image=image, text=text)
                logga("Blog %s edited." % post_id)

        return self.redirect_to("instructor-blog-details", post_id=post_id)


class InstructorBlogDeleteHandler(Handler):
    @instructor_required
    def get(self, post_id):
        post = BlogPost.get_by_id(int(post_id))
        params = {"post": post}
        user = User.get_by_email(users.get_current_user().email().lower())
        if post.author_id == user.get_id:
            return self.render_template("instructor/blog_post_delete.html", params)
        else:
            return self.redirect_to("forbidden")

    @instructor_required
    def post(self, post_id):
        post = BlogPost.get_by_id(int(post_id))
        user = User.get_by_email(users.get_current_user().email().lower())
        if post.author_id == user.get_id:
            post.deleted = True
            post.put()
            logga("Blog %s deleted." % post_id)

        return self.redirect_to("instructor-blog-list")