from app.handlers.base import Handler


class MainHandler(Handler):
    def get(self):
        self.render_template("public/main.html")


class TempMainHandler(Handler):
    def get(self):
        self.render_template("public/main2.html")


class PublicCourseListHandler(Handler):
    def get(self):
        self.render_template("public/course_list.html")


class PublicPartnersHandler(Handler):
    def get(self):
        self.render_template("public/partners.html")


class PublicBlogHandler(Handler):
    def get(self):
        self.render_template("public/blog.html")


class PublicAboutHandler(Handler):
    def get(self):
        self.render_template("public/about.html")