from google.appengine.api import users
from app.handlers.base import Handler
from app.models.auth import User
from app.models.franchise import Franchise
from app.models.manager import Manager
from app.utils.decorators import admin_required, manager_required
from app.utils.other import logga


class AdminManagersListHandler(Handler):
    @admin_required
    def get(self):
        managers = Manager.query().fetch()
        params = {"managers": managers}
        return self.render_template("admin/manager_list.html", params)


class AdminManagerAddHandler(Handler):
    @admin_required
    def get(self):
        franchises = Franchise.query(Franchise.deleted == False).fetch()
        params = {"franchises": franchises}
        return self.render_template("admin/manager_add.html", params)

    @admin_required
    def post(self):
        email = self.request.get("email")
        first_name = self.request.get("first-name")
        last_name = self.request.get("last-name")
        franchise_id = self.request.get("franchise")

        franchise = Franchise.get_by_id(int(franchise_id))

        user = User.get_or_short_create(email=email, first_name=first_name, last_name=last_name)

        manager = Manager.create(full_name=user.get_full_name, email=email, user_id=user.get_id, franchise=franchise)
        logga("Manager %s added." % manager.get_id)

        return self.redirect_to("admin-managers-list")


class AdminManagerDeleteHandler(Handler):
    @admin_required
    def get(self, manager_id):
        manager = Manager.get_by_id(int(manager_id))
        params = {"manager": manager}
        return self.render_template("admin/manager_delete.html", params)

    @admin_required
    def post(self, manager_id):
        manager = Manager.get_by_id(int(manager_id))
        manager.key.delete()
        logga("Manager %s removed." % manager_id)
        return self.redirect_to("admin-managers-list")


# MANAGER
class ManagerProfileDetailsHandler(Handler):
    @manager_required
    def get(self):
        current_user = users.get_current_user()
        profile = User.query(User.email == str(current_user.email()).lower()).get()

        if not profile:
            return self.redirect_to("forbidden")

        params = {"profile": profile}
        return self.render_template("manager/profile.html", params)


class ManagerProfileEditHandler(Handler):
    @manager_required
    def get(self):
        current_user = users.get_current_user()
        profile = User.query(User.email == str(current_user.email()).lower()).get()

        if not profile:
            return self.redirect_to("forbidden")
        else:
            params = {"profile": profile}
            return self.render_template("manager/profile_edit.html", params)

    @manager_required
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

            user = User.update(user=profile, first_name=first_name, last_name=last_name, address=address,
                               phone_number=phone_number, summary=summary, photo_url=photo_url, dob=dob)

            logga("User %s edited." % user.get_id)
            return self.redirect_to("manager-profile")