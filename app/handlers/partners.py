import datetime
from app.models.auth import User
from app.models.course import Course, CourseApplication
from app.models.franchise import Franchise
from app.models.manager import Manager
from app.utils.decorators import admin_required, partner_required, manager_required
from app.handlers.base import Handler
from app.models.partner import Partner, PartnerUserCourse
from google.appengine.api import users
from app.utils.other import logga


# ADMIN
class AdminPartnersListHandler(Handler):
    @admin_required
    def get(self):
        partners = Partner.query(Partner.deleted == False).fetch()
        params = {"partners": partners}
        return self.render_template("admin/partners_list.html", params)


class AdminPartnerAddHandler(Handler):
    @admin_required
    def get(self):
        franchises = Franchise.query(Franchise.deleted == False).fetch()
        params = {"franchises": franchises}
        return self.render_template("admin/partner_add.html", params)

    @admin_required
    def post(self):
        title = self.request.get("title")
        website = self.request.get("website")
        logo = self.request.get("logo")
        summary = self.request.get("summary")
        description = self.request.get("description")
        franchise_id = self.request.get("franchise")

        franchise = Franchise.get_by_id(int(franchise_id))

        partner = Partner.create(title=title, website=website, logo=logo, summary=summary, description=description,
                                 franchise=franchise)
        logga("Partner %s added." % partner.get_id)

        return self.redirect_to("admin-partners-list")


class AdminPartnerDetailsHandler(Handler):
    @admin_required
    def get(self, partner_id):
        partner = Partner.get_by_id(int(partner_id))
        params = {"partner": partner}
        return self.render_template("admin/partner_details.html", params)


class AdminPartnerDeleteHandler(Handler):
    @admin_required
    def get(self, partner_id):
        partner = Partner.get_by_id(int(partner_id))
        params = {"partner": partner}
        return self.render_template("admin/partner_delete.html", params)

    @admin_required
    def post(self, partner_id):
        partner = Partner.get_by_id(int(partner_id))
        partner.deleted = True
        partner.put()
        logga("Partner %s deleted." % partner_id)
        return self.redirect_to("admin-partners-list")


class AdminPartnerEditHandler(Handler):
    @admin_required
    def get(self, partner_id):
        partner = Partner.get_by_id(int(partner_id))
        franchises = Franchise.query(Franchise.deleted == False).fetch()
        params = {"partner": partner, "franchises": franchises}
        return self.render_template("admin/partner_edit.html", params)

    @admin_required
    def post(self, partner_id):
        title = self.request.get("title")
        website = self.request.get("website")
        logo = self.request.get("logo")
        summary = self.request.get("summary")
        description = self.request.get("description")
        franchise_id = self.request.get("franchise")

        franchise = Franchise.get_by_id(int(franchise_id))

        partner = Partner.get_by_id(int(partner_id))

        Partner.update(partner=partner, title=title, website=website, logo=logo, summary=summary,
                       description=description, franchise=franchise)
        logga("Partner %s updated." % partner_id)

        return self.redirect_to("admin-partner-details", partner_id=partner_id)


# Partner User Course
class AdminPartnerUserCourseList(Handler):
    @admin_required
    def get(self):
        pucs = PartnerUserCourse.query().fetch()
        params = {"pucs": pucs}
        return self.render_template("admin/partner_user_course_list.html", params)


class AdminPartnerUserCourseAdd(Handler):
    @admin_required
    def get(self):
        courses = Course.query(Course.deleted == False, Course.start_date > datetime.datetime.now()).order(Course.start_date).fetch()
        params = {"courses": courses}
        return self.render_template("admin/partner_user_course_add.html", params)

    @admin_required
    def post(self):
        email = self.request.get("email")
        first_name = self.request.get("first-name")
        last_name = self.request.get("last-name")
        course_id = self.request.get("course")

        user = User.get_or_short_create(email=email, first_name=first_name, last_name=last_name)

        course = Course.get_by_id(int(course_id))

        puc = PartnerUserCourse.create(user_id=user.get_id, user_name=user.get_full_name, user_email=email, course=course)
        logga("PartnerUserCourse %s added." % puc.get_id)

        return self.redirect_to("admin-partner-user-course-list")


class AdminPartnerUserCourseDelete(Handler):
    @admin_required
    def get(self, puc_id):
        puc = PartnerUserCourse.get_by_id(int(puc_id))
        params = {"puc": puc}
        return self.render_template("admin/partner_user_course_delete.html", params)

    @admin_required
    def post(self, puc_id):
        puc = PartnerUserCourse.get_by_id(int(puc_id))
        #PartnerUserCourse.delete(puc=puc)
        puc.key.delete()  # delete directly from the database, because not that important
        logga("PartnerUserCourse %s deleted." % puc_id)
        return self.redirect_to("admin-partner-user-course-list")


# MANAGER
class ManagerPartnersListHandler(Handler):
    @manager_required
    def get(self):
        curr_user = users.get_current_user()
        manager = Manager.query(Manager.email == curr_user.email().lower()).get()

        partners = Partner.query(Partner.deleted == False, Partner.franchise_id == manager.franchise_id).fetch()
        params = {"partners": partners}
        return self.render_template("manager/partners_list.html", params)


class ManagerPartnerDetailsHandler(Handler):
    @manager_required
    def get(self, partner_id):
        partner = Partner.get_by_id(int(partner_id))
        params = {"partner": partner}
        return self.render_template("manager/partner_details.html", params)


class ManagerPartnerAddHandler(Handler):
    @manager_required
    def get(self):
        return self.render_template("manager/partner_add.html")

    @manager_required
    def post(self):
        title = self.request.get("title")
        website = self.request.get("website")
        logo = self.request.get("logo")
        summary = self.request.get("summary")
        description = self.request.get("description")

        curr_user = users.get_current_user()
        manager = Manager.query(Manager.email == curr_user.email().lower()).get()

        franchise = Franchise.get_by_id(manager.franchise_id)

        partner = Partner.create(title=title, website=website, logo=logo, summary=summary, description=description,
                                 franchise=franchise)

        logga("Partner %s added." % partner.get_id)

        return self.redirect_to("manager-partners-list")


class ManagerPartnerEditHandler(Handler):
    @manager_required
    def get(self, partner_id):
        partner = Partner.get_by_id(int(partner_id))
        params = {"partner": partner}
        return self.render_template("manager/partner_edit.html", params)

    @manager_required
    def post(self, partner_id):
        title = self.request.get("title")
        website = self.request.get("website")
        logo = self.request.get("logo")
        summary = self.request.get("summary")
        description = self.request.get("description")

        curr_user = users.get_current_user()
        manager = Manager.query(Manager.email == curr_user.email().lower()).get()

        franchise = Franchise.get_by_id(manager.franchise_id)

        partner = Partner.get_by_id(int(partner_id))

        Partner.update(partner=partner, title=title, website=website, logo=logo, summary=summary,
                       description=description, franchise=franchise)

        logga("Partner %s updated." % partner_id)

        return self.redirect_to("manager-partner-details", partner_id=partner_id)


class ManagerPartnerDeleteHandler(Handler):
    @manager_required
    def get(self, partner_id):
        partner = Partner.get_by_id(int(partner_id))
        params = {"partner": partner}
        return self.render_template("manager/partner_delete.html", params)

    @manager_required
    def post(self, partner_id):
        partner = Partner.get_by_id(int(partner_id))
        curr_user = users.get_current_user()
        manager = Manager.query(Manager.email == curr_user.email().lower()).get()

        if manager.franchise_id == partner.franchise_id:
            partner.deleted = True
            partner.put()
            logga("Partner %s deleted." % partner_id)

        return self.redirect_to("manager-partners-list")


# PUBLIC
class PublicPartnersHandler(Handler):
    def get(self):
        partners = Partner.query(Partner.deleted == False).fetch()
        params = {"partners": partners}
        return self.render_template("public/partners.html", params=params)


# PARTNER
class PartnerCourseListHandler(Handler):
    @partner_required
    def get(self):
        current_user = users.get_current_user()
        user = User.query(User.email == str(current_user.email()).lower()).get()
        if not user:
            return self.redirect_to("forbidden")
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
            return self.render_template("partner/course_list.html", params)


class PartnerCourseDetailsHandler(Handler):
    @partner_required
    def get(self, course_id):
        current_user = users.get_current_user()
        user = User.query(User.email == str(current_user.email()).lower()).get()
        if not user:
            return self.redirect_to("forbidden")
        else:
            puc = PartnerUserCourse.query(PartnerUserCourse.course_id == int(course_id),
                                          PartnerUserCourse.user_id == user.get_id).get()

            if puc:
                course = Course.get_by_id(int(course_id))

                applications = CourseApplication.query(CourseApplication.course_id == int(course_id),
                                                       CourseApplication.deleted == False).order(-CourseApplication.created).fetch()

                num_paid = 0
                num_no_laptop = 0
                total_paid = 0.0
                for application in applications:
                    if application.payment_status:
                        num_paid += 1
                        total_paid += application.price
                    if application.laptop == "no":
                        num_no_laptop += 1

                params = {"course": course,
                          "applications": applications,
                          "num_paid": num_paid,
                          "no_laptop": num_no_laptop,
                          "total_paid": total_paid}
                return self.render_template("partner/course_details.html", params)
            else:
                return self.redirect_to("forbidden")


class PartnerProfileDetailsHandler(Handler):
    @partner_required
    def get(self):
        current_user = users.get_current_user()
        profile = User.query(User.email == str(current_user.email()).lower()).get()

        if not profile:
            return self.redirect_to("forbidden")

        params = {"profile": profile}
        return self.render_template("partner/profile.html", params)


class PartnerProfileEditHandler(Handler):
    @partner_required
    def get(self):
        current_user = users.get_current_user()
        profile = User.query(User.email == str(current_user.email()).lower()).get()

        if not profile:
            return self.redirect_to("forbidden")
        else:
            params = {"profile": profile}
            return self.render_template("partner/profile_edit.html", params)

    @partner_required
    def post(self):
        current_user = users.get_current_user()
        profile = User.query(User.email == str(current_user.email()).lower()).get()

        if not profile:
            return self.redirect_to("forbidden")
        else:
            first_name = self.request.get("first_name")
            last_name = self.request.get("last_name")
            address = self.request.get("address")
            summary = self.request.get("summary")
            photo_url = self.request.get("photo_url")
            phone_number = self.request.get("phone_number")
            dob = self.request.get("dob")
            User.update(user=profile, first_name=first_name, last_name=last_name, address=address, phone_number=phone_number,
                    summary=summary, photo_url=photo_url, dob=dob)
            logga("Partner %s profile edited." % profile.get_id)
            return self.redirect_to("partner-profile")