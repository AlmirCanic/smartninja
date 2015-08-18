from google.appengine.api import users
from webapp2 import redirect_to
from app.models.employer import Employer
from app.models.instructor import Instructor
from app.models.manager import Manager
from app.models.partner import PartnerUserCourse
from app.models.student import StudentCourse
from app.settings import ADMINS


def admin_required(handler):
    def check_login(self, *args, **kwargs):
        user = users.get_current_user()
        if user:
            email = user.email().lower()
            if email in ADMINS:
                return handler(self, *args, **kwargs)
            else:
                return redirect_to("forbidden")
        else:
            return self.redirect(users.create_login_url(self.request.uri))
    return check_login


def manager_required(handler):
    def check_login(self, *args, **kwargs):
        user = users.get_current_user()
        if user:
            email = user.email().lower()
            managers = Manager.query(Manager.email == email).fetch()
            if managers:
                return handler(self, *args, **kwargs)
            else:
                return redirect_to("forbidden")
        else:
            return self.redirect(users.create_login_url(self.request.uri))
    return check_login


def partner_required(handler):
    def check_login(self, *args, **kwargs):
        user = users.get_current_user()
        if user:
            email = user.email().lower()
            pucs = PartnerUserCourse.query(PartnerUserCourse.user_email == email).fetch()
            if pucs:
                return handler(self, *args, **kwargs)
            else:
                return redirect_to("forbidden")
        else:
            return self.redirect(users.create_login_url(self.request.uri))
    return check_login


def student_required(handler):
    def check_login(self, *args, **kwargs):
        user = users.get_current_user()
        if user:
            email = user.email().lower()
            students = StudentCourse.query(StudentCourse.user_email == email).fetch()
            if students:
                return handler(self, *args, **kwargs)
            else:
                return redirect_to("forbidden")
        else:
            return self.redirect(users.create_login_url(self.request.uri))
    return check_login


def instructor_required(handler):
    def check_login(self, *args, **kwargs):
        user = users.get_current_user()
        if user:
            email = user.email().lower()
            instructors = Instructor.query(Instructor.email == email, Instructor.active == True).fetch()
            if instructors:
                return handler(self, *args, **kwargs)
            else:
                return redirect_to("forbidden")
        else:
            return self.redirect(users.create_login_url(self.request.uri))
    return check_login


def employer_required(handler):
    def check_login(self, *args, **kwargs):
        user = users.get_current_user()
        if user:
            email = user.email().lower()
            employers = Employer.query(Instructor.email == email).fetch()
            if employers:
                return handler(self, *args, **kwargs)
            else:
                return redirect_to("forbidden")
        else:
            return self.redirect(users.create_login_url(self.request.uri))
    return check_login