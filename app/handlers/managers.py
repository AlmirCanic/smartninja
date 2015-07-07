from app.handlers.base import Handler
from app.models.auth import User
from app.models.franchise import Franchise
from app.models.manager import Manager
from app.utils.decorators import admin_required
from app.utils.other import logga


class AdminManagersListHandler(Handler):
    @admin_required
    def get(self):
        managers = Manager.query().fetch()
        params = {"managers": managers}
        self.render_template("admin/manager_list.html", params)


class AdminManagerAddHandler(Handler):
    @admin_required
    def get(self):
        franchises = Franchise.query(Franchise.deleted == False).fetch()
        params = {"franchises": franchises}
        self.render_template("admin/manager_add.html", params)

    @admin_required
    def post(self):
        email = self.request.get("email")
        first_name = self.request.get("first-name")
        last_name = self.request.get("last-name")
        franchise_id = self.request.get("franchise")

        franchise = Franchise.get_by_id(int(franchise_id))

        user = User.get_by_email(email=email)

        if not user:
            user = User.short_create(email=email, first_name=first_name, last_name=last_name)

        manager = Manager.create(full_name=user.get_full_name, email=email, user_id=user.get_id, franchise=franchise)
        logga("Manager %s added." % manager.get_id)

        return self.redirect_to("admin-managers-list")


class AdminManagerDeleteHandler(Handler):
    @admin_required
    def get(self, manager_id):
        manager = Manager.get_by_id(int(manager_id))
        params = {"manager": manager}
        self.render_template("admin/manager_delete.html", params)
    @admin_required
    def post(self, manager_id):
        manager = Manager.get_by_id(int(manager_id))
        manager.key.delete()
        logga("Manager %s removed." % manager_id)
        self.redirect_to("admin-managers-list")