from google.appengine.api import users
from webapp2 import redirect_to
from app.models.instructor import Instructor
from app.models.partner import PartnerUserCourse
from app.settings import ADMINS


def admin_required(handler):
    def check_login(self, *args, **kwargs):
        user = users.get_current_user()
        if user:
            email = user.email()
            if email in ADMINS:
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
            email = user.email()
            pucs = PartnerUserCourse.query(PartnerUserCourse.user_email == email).fetch()
            if pucs:
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
            email = user.email()
            instructors = Instructor.query(Instructor.email == email).fetch()
            if instructors:
                return handler(self, *args, **kwargs)
            else:
                return redirect_to("forbidden")
        else:
            return self.redirect(users.create_login_url(self.request.uri))
    return check_login