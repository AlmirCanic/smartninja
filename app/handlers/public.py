import datetime
from app.handlers.base import Handler
from app.models.course import Course, CourseApplication


class MainHandler(Handler):
    def get(self):
        course_list = Course.query(Course.deleted == False, Course.start_date >= datetime.datetime.now()).order(Course.start_date).fetch(4)

        courses = []
        for course in course_list:
            try:
                course.price_min = str(course.price[0]).replace(".", ",0")
            except:
                course.price_min = course.prices[0].price_comma
            courses.append(course)

        params = {"courses": courses}
        self.render_template("public/main.html", params=params)


class PublicAboutHandler(Handler):
    def get(self):
        self.render_template("public/about.html")


class PublicFaqHandler(Handler):
    def get(self):
        self.render_template("public/faq.html")


class PublicCareersHandler(Handler):
    def get(self):
        self.render_template("public/careers.html")


class PublicComingSoonHandler(Handler):
    def get(self):
        self.render_template("public/coming_soon.html")


class PublicApplyThankYouHandler(Handler):
    def get(self):
        caid = self.request.get("caid")
        course_app = CourseApplication.get_by_id(int(caid))

        ts = str(course_app.created.month) + str(course_app.created.day) + str(course_app.created.microsecond)
        final_date = course_app.created + datetime.timedelta(days=8)
        price_str = str(course_app.price).replace(".0", ",00")

        params = {"course_app": course_app, "ts": ts, "final_date": final_date, "price_str": price_str}

        self.render_template("public/apply_thank_you.html", params=params)


class PublicNewsletterThankYouHandler(Handler):
    def get(self):
        self.render_template("public/newsletter_thank_you_1.html")


class PublicNewsletterThankYou2Handler(Handler):
    def get(self):
        self.render_template("public/newsletter_thank_you_2.html")