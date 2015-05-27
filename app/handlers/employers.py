from google.appengine.api import users
from app.handlers.base import Handler
from app.models.auth import User
from app.models.employer import Employer
from app.utils.decorators import admin_required, employer_required
from app.utils.other import logga


# ADMIN
class AdminEmployersListHandler(Handler):
    @admin_required
    def get(self):
        employers = Employer.query().fetch()
        params = {"employers": employers}
        self.render_template("admin/employer_list.html", params)


class AdminEmployerAddHandler(Handler):
    @admin_required
    def get(self):
        self.render_template("admin/employer_add.html")

    @admin_required
    def post(self):
        email = self.request.get("email")
        first_name = self.request.get("first-name")
        last_name = self.request.get("last-name")

        user = User.get_by_email(email=email)

        if not user:
            user = User.short_create(email=email, first_name=first_name, last_name=last_name)

        employer = Employer.create(full_name=user.get_full_name, email=email, user_id=user.get_id)
        logga("Employer %s added." % employer.get_id)

        return self.redirect_to("admin-employers-list")


class AdminEmployerDeleteHandler(Handler):
    @admin_required
    def get(self, employer_id):
        employer = Employer.get_by_id(int(employer_id))
        params = {"employer": employer}
        self.render_template("admin/employer_delete.html", params)
    @admin_required
    def post(self, employer_id):
        employer = Employer.get_by_id(int(employer_id))
        employer.key.delete()
        logga("Employer %s removed." % employer_id)
        self.redirect_to("admin-employers-list")


# EMPLOYER
class EmployerProfileDetailsHandler(Handler):
    @employer_required
    def get(self):
        current_user = users.get_current_user()
        profile = User.query(User.email == str(current_user.email()).lower()).get()

        if not profile:
            return self.redirect_to("forbidden")

        params = {"profile": profile}
        self.render_template("employer/profile.html", params)


class EmployerProfileEditHandler(Handler):
    @employer_required
    def get(self):
        current_user = users.get_current_user()
        profile = User.query(User.email == str(current_user.email()).lower()).get()

        if not profile:
            return self.redirect_to("forbidden")
        else:
            params = {"profile": profile}
            self.render_template("employer/profile_edit.html", params)

    @employer_required
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
            current_town = self.request.get("current-town")
            dob = self.request.get("dob")
            User.update(user=profile, first_name=first_name, last_name=last_name, address=address, phone_number=phone_number,
                    summary=summary, photo_url=photo_url, dob=dob, current_town=current_town)
            logga("Employer %s profile edited." % profile.get_id)
            self.redirect_to("employer-profile")