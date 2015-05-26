from app.handlers.base import Handler
from app.models.auth import User
from app.models.employer import Employer
from app.utils.decorators import admin_required
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