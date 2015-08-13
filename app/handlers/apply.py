"""
Course applications handlers
"""

import datetime
from google.appengine.api import users
from app.emails.apply import email_course_application_thank_you, email_course_app_to_smartninja, \
    email_course_application_thank_you_2
from app.handlers.base import Handler
from app.models.auth import User
from app.models.course import Course, CourseApplication
from app.models.manager import Manager
from app.models.student import StudentCourse
from app.settings import is_local
from app.utils.csrf import check_csrf
from app.utils.decorators import admin_required, manager_required
from app.utils.other import logga


# ADMIN
class AdminCourseApplicationDetailsHandler(Handler):
    @admin_required
    def get(self, application_id):
        application = CourseApplication.get_by_id(int(application_id))
        user_id = application.student_id
        user = User.get_by_id(user_id)
        params = {"application": application, "this_user": user}
        self.render_template("admin/application_details.html", params)

    @admin_required
    def post(self, application_id):
        application = CourseApplication.get_by_id(int(application_id))
        application.payment_status = bool(self.request.get("paid"))
        application.price = float(self.request.get("price"))
        application.invoice = self.request.get("invoice")
        application.put()

        if application.payment_status:
            StudentCourse.create(user_id=application.student_id, user_name=application.student_name,
                                 user_email=application.student_email, course=Course.get_by_id(application.course_id))

        logga("Course application %s edited." % application_id)
        self.redirect_to("course-details", course_id=application.course_id)


class AdminCourseApplicationDeleteHandler(Handler):
    @admin_required
    def get(self, application_id):
        application = CourseApplication.get_by_id(int(application_id))
        params = {"application": application}
        self.render_template("admin/application_delete.html", params)

    @admin_required
    def post(self, application_id):
        application = CourseApplication.get_by_id(int(application_id))
        CourseApplication.delete(application=application)
        logga("Course application %s deleted." % application_id)
        self.redirect_to("course-details", course_id=application.course_id)


class AdminCourseApplicationMoveStudentHandler(Handler):
    @admin_required
    def get(self, application_id):
        application = CourseApplication.get_by_id(int(application_id))
        courses = Course.query(Course.deleted == False, Course.start_date > datetime.datetime.now()).order(Course.start_date).fetch()
        params = {"application": application, "courses": courses}
        self.render_template("admin/application_move_student.html", params)

    @admin_required
    def post(self, application_id):
        application = CourseApplication.get_by_id(int(application_id))
        course_id = self.request.get("course")
        new_course = Course.get_by_id(int(course_id))
        old_course = Course.get_by_id(application.course_id)
        CourseApplication.move_student_to_another_course(application=application, old_course=old_course, new_course=new_course)
        logga("Student application %s moved to another course." % application_id)
        self.redirect_to("course-details", course_id=application.course_id)


# PUBLIC

class PublicCourseApplicationAddHandler(Handler):
    def post(self, course_id):
        hidden = self.request.get("hidden")
        csrf = self.request.get("csrf")
        if hidden:
            return self.redirect_to("public-course-details", course_id=int(course_id))
        elif check_csrf(csrf):
            first_name = self.request.get("first_name")
            last_name = self.request.get("last_name")
            email = self.request.get("email").strip().lower()
            address = self.request.get("address")
            dob = self.request.get("dob")
            phone = self.request.get("phone")
            laptop = self.request.get("laptop")
            shirt = self.request.get("shirt")
            price = self.request.get("price")
            company = self.request.get("company_invoice")
            other_info = self.request.get("other_info")

            if first_name and last_name and email and address and phone:
                user = User.get_by_email(email)

                if not shirt:
                    shirt = "/"

                if not dob:
                    dob = "/"

                if not user:
                    # add user to database
                    user = User.create(first_name=first_name, last_name=last_name, email=email, address=address,
                                       dob=dob, phone_number=phone)

                course = Course.get_by_id(int(course_id))

                if not price:
                    try:
                        price = str(course.prices[0].price_dot)
                    except:
                        price = str(course.price[0])

                if company:
                    company_title = self.request.get("company_title")
                    company_address = self.request.get("company_address")
                    company_zip = self.request.get("company_zip")
                    company_town = self.request.get("company_town")
                    company_tax = self.request.get("company_tax")
                    course_app = CourseApplication.create(course=course, student_name=user.get_full_name,
                                                          student_id=user.get_id, student_email=email,
                                                          price=float(price), currency=course.currency, laptop=laptop,
                                                          shirt=shirt, company_invoice=True, company_title=company_title,
                                                          company_address=company_address, company_zip=company_zip,
                                                          company_town=company_town, company_tax_number=company_tax,
                                                          other_info=other_info)
                elif not company:
                    course_app = CourseApplication.create(course=course, student_name=user.get_full_name, student_id=user.get_id,
                                                      student_email=email, price=float(price), currency=course.currency,
                                                      laptop=laptop, shirt=shirt, other_info=other_info)
                else:
                    return self.redirect_to("oops")

                ts = str(course_app.created.month) + str(course_app.created.day) + str(course_app.created.microsecond)
                final_date = course_app.created + datetime.timedelta(days=8)
                price_str = str(course_app.price).replace(".0", ",00")

                course_app.invoice = ts
                course_app.put()

                # send email to info@smartninja.org
                if not is_local():
                    email_course_app_to_smartninja(course=course, user=user, application=course_app)

                # send email to the student
                if not is_local():
                    email_course_application_thank_you_2(course_app)
                    email_course_application_thank_you(course_app, ts=ts, final_date=final_date, price_str=price_str)

                return self.redirect("/apply_thank_you?caid=%s" % course_app.get_id)
            else:
                # TODO: error in params
                return self.redirect_to("oops")
        else:
            return self.redirect_to("oops")


# MANAGER
class ManagerCourseApplicationDetailsHandler(Handler):
    @manager_required
    def get(self, application_id):
        application = CourseApplication.get_by_id(int(application_id))
        user_id = application.student_id
        user = User.get_by_id(user_id)
        params = {"application": application, "this_user": user}
        return self.render_template("manager/application_details.html", params)

    @manager_required
    def post(self, application_id):
        application = CourseApplication.get_by_id(int(application_id))

        # check if manager has permissions to edit this application (if in the same franchise)
        course = Course.get_by_id(application.course_id)
        current_user = users.get_current_user()
        manager = Manager.query(Manager.email == current_user.email().lower()).get()

        if course.franchise_id != manager.franchise_id:
            return self.redirect_to("forbidden")

        # edit and save changes for course application
        application.payment_status = bool(self.request.get("paid"))
        application.price = float(self.request.get("price"))
        application.invoice = self.request.get("invoice")
        application.put()

        if application.payment_status:
            StudentCourse.create(user_id=application.student_id, user_name=application.student_name,
                                 user_email=application.student_email, course=course)

        logga("Course application %s edited." % application_id)
        return self.redirect_to("manager-course-details", course_id=application.course_id)


class ManagerCourseApplicationDeleteHandler(Handler):
    @manager_required
    def get(self, application_id):
        application = CourseApplication.get_by_id(int(application_id))
        params = {"application": application}
        return self.render_template("manager/application_delete.html", params)

    @manager_required
    def post(self, application_id):
        application = CourseApplication.get_by_id(int(application_id))

        # check if manager has permissions to edit this application (if in the same franchise)
        course = Course.get_by_id(application.course_id)
        current_user = users.get_current_user()
        manager = Manager.query(Manager.email == current_user.email().lower()).get()

        if course.franchise_id != manager.franchise_id:
            return self.redirect_to("forbidden")
        else:
            CourseApplication.delete(application=application)
            logga("Course application %s deleted." % application_id)
            return self.redirect_to("manager-course-details", course_id=application.course_id)


class ManagerCourseApplicationMoveStudentHandler(Handler):
    @manager_required
    def get(self, application_id):
        current_user = users.get_current_user()
        manager = Manager.query(Manager.email == str(current_user.email()).lower()).get()

        application = CourseApplication.get_by_id(int(application_id))

        courses = Course.query(Course.deleted == False,
                               Course.start_date > datetime.datetime.now(),
                               Course.franchise_id == manager.franchise_id).order(Course.start_date).fetch()
        params = {"application": application, "courses": courses}
        return self.render_template("manager/application_move_student.html", params)

    @manager_required
    def post(self, application_id):
        application = CourseApplication.get_by_id(int(application_id))

        # check if manager has permissions to edit this application (if in the same franchise)
        course = Course.get_by_id(application.course_id)
        current_user = users.get_current_user()
        manager = Manager.query(Manager.email == current_user.email().lower()).get()

        if course.franchise_id != manager.franchise_id:
            return self.redirect_to("forbidden")

        course_id = self.request.get("course")
        new_course = Course.get_by_id(int(course_id))

        CourseApplication.move_student_to_another_course(application=application, old_course=course, new_course=new_course)

        logga("Student application %s moved to another course." % application_id)
        return self.redirect_to("manager-course-details", course_id=application.course_id)