import datetime
from app.models.auth import User
from app.models.course import Course
from app.utils.decorators import admin_required, partner_required
from app.handlers.base import Handler
from app.models.partner import Partner, PartnerUserCourse
from google.appengine.api import users


# ADMIN

class AdminPartnersListHandler(Handler):
    @admin_required
    def get(self):
        partners = Partner.query(Partner.deleted == False).fetch()
        params = {"partners": partners}
        self.render_template("admin/partners_list.html", params)


class AdminPartnerAddHandler(Handler):
    @admin_required
    def get(self):
        params = {}
        self.render_template("admin/partner_add.html", params)

    @admin_required
    def post(self):
        title = self.request.get("title")
        country = self.request.get("country")
        website = self.request.get("website")
        logo = self.request.get("logo")
        summary = self.request.get("summary")
        description = self.request.get("description")

        Partner.create(title=title, country=country, website=website, logo=logo, summary=summary, description=description)

        self.redirect_to("admin-partners-list")


class AdminPartnerDetailsHandler(Handler):
    @admin_required
    def get(self, partner_id):
        partner = Partner.get_by_id(int(partner_id))
        params = {"partner": partner}
        self.render_template("admin/partner_details.html", params)


class AdminPartnerDeleteHandler(Handler):
    @admin_required
    def get(self, partner_id):
        partner = Partner.get_by_id(int(partner_id))
        params = {"partner": partner}
        self.render_template("admin/partner_delete.html", params)

    @admin_required
    def post(self, partner_id):
        partner = Partner.get_by_id(int(partner_id))
        partner.deleted = True
        partner.put()
        self.redirect_to("admin-partners-list")


class AdminPartnerEditHandler(Handler):
    @admin_required
    def get(self, partner_id):
        partner = Partner.get_by_id(int(partner_id))
        params = {"partner": partner}
        self.render_template("admin/partner_edit.html", params)

    @admin_required
    def post(self, partner_id):
        title = self.request.get("title")
        country = self.request.get("country")
        website = self.request.get("website")
        logo = self.request.get("logo")
        summary = self.request.get("summary")
        description = self.request.get("description")

        partner = Partner.get_by_id(int(partner_id))

        Partner.update(partner=partner, title=title, country=country, website=website, logo=logo, summary=summary,
                       description=description)

        self.redirect_to("admin-partner-details", partner_id=partner_id)


# Partner User Course


class AdminPartnerUserCourseList(Handler):
    @admin_required
    def get(self):
        pucs = PartnerUserCourse.query().fetch()
        params = {"pucs": pucs}
        self.render_template("admin/partner_user_course_list.html", params)


class AdminPartnerUserCourseAdd(Handler):
    @admin_required
    def get(self):
        courses = Course.query(Course.deleted == False, Course.start_date > datetime.datetime.now()).order(Course.start_date).fetch()
        params = {"courses": courses}
        self.render_template("admin/partner_user_course_add.html", params)

    @admin_required
    def post(self):
        email = self.request.get("email")
        first_name = self.request.get("first-name")
        last_name = self.request.get("last-name")
        course_id = self.request.get("course")

        user = User.get_by_email(email=email)

        if not user:
            user = User.short_create(email=email, first_name=first_name, last_name=last_name)

        course = Course.get_by_id(int(course_id))

        PartnerUserCourse.create(user_id=user.get_id, user_name=user.get_full_name, user_email=email, course=course)

        return self.redirect_to("admin-partner-user-course-list")


class AdminPartnerUserCourseDelete(Handler):
    @admin_required
    def get(self, puc_id):
        puc = PartnerUserCourse.get_by_id(int(puc_id))
        params = {"puc": puc}
        self.render_template("admin/partner_user_course_delete.html", params)
    @admin_required
    def post(self, puc_id):
        puc = PartnerUserCourse.get_by_id(int(puc_id))
        #PartnerUserCourse.delete(puc=puc)
        puc.key.delete()  # delete directly from the database, because not that important
        self.redirect_to("admin-partner-user-course-list")


# PUBLIC

class PublicPartnersHandler(Handler):
    def get(self):
        partners = Partner.query(Partner.deleted == False).fetch()
        params = {"partners": partners}
        self.render_template("public/partners.html", params=params)


# PARTNER

class PartnerCourseListHandler(Handler):
    @partner_required
    def get(self):
        current_user = users.get_current_user()
        user = User.query(User.email == str(current_user.email())).get()
        if not user:
            return self.redirect_to("403.html")
        else:
            pucs = PartnerUserCourse.query(PartnerUserCourse.user_id == user.get_id).fetch()

            courses = []
            for puc in pucs:
                course = Course.get_by_id(puc.course_id)
                courses.append(course)

            past_courses = []
            future_courses = []
            for course in courses:
                if course.start_date > datetime.date.today():
                    future_courses.append(course)
                else:
                    past_courses.append(course)
            params = {"future_courses": future_courses, "past_courses": past_courses}
            self.render_template("partner/course_list.html", params)