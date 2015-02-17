import logging
from app.handlers.base import Handler
from app.models.auth import User
from app.models.course import CourseApplication
from app.settings import ADMINS
from app.utils.decorators import admin_required
from app.utils.other import logga


class AdminUsersListHandler(Handler):
    @admin_required
    def get(self):
        users = User.query(User.deleted == False).fetch()

        admins = []

        for user in users:
            if user.email in ADMINS:
                admins.append(user)

        params = {"admins": admins}
        self.render_template("admin/users_list.html", params)


class AdminUsersAllListHandler(Handler):
    @admin_required
    def get(self):
        users = User.query(User.deleted == False).fetch()

        params = {"users": users}
        self.render_template("admin/users_all_list.html", params)


class AdminUserDetailsHandler(Handler):
    @admin_required
    def get(self, user_id):
        user = User.get_by_id(int(user_id))
        admin = False
        if user.email in ADMINS:
            admin = True
        params = {"this_user": user, "admin": admin}
        self.render_template("admin/user_details.html", params)


class AdminUserDeleteHandler(Handler):
    @admin_required
    def get(self, user_id):
        user = User.get_by_id(int(user_id))
        params = {"this_user": user}
        self.render_template("admin/user_delete.html", params)

    @admin_required
    def post(self, user_id):
        user = User.get_by_id(int(user_id))
        if user.email not in ADMINS:
            user.deleted = True
            user.put()
            logga("User %s deleted." % user_id)
        self.redirect_to("users-list")


class AdminUserEditHandler(Handler):
    @admin_required
    def get(self, user_id):
        user = User.get_by_id(int(user_id))
        params = {"this_user": user}
        self.render_template("admin/user_edit.html", params)

    @admin_required
    def post(self, user_id):
        user = User.get_by_id(int(user_id))
        first_name = self.request.get("first_name")
        last_name = self.request.get("last_name")
        address = self.request.get("address")
        summary = self.request.get("summary")
        photo_url = self.request.get("photo_url")
        phone_number = self.request.get("phone_number")
        dob = self.request.get("dob")
        instructor = bool(self.request.get("instructor"))
        User.update(user=user, first_name=first_name, last_name=last_name, address=address, phone_number=phone_number,
                    summary=summary, photo_url=photo_url, dob=dob, instructor=instructor)
        logga("User %s edited." % user_id)
        self.redirect_to("user-details", user_id=int(user_id))