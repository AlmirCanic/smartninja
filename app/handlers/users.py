from app.handlers.base import Handler
from app.models.auth import User
from app.utils.decorators import admin_required


class AdminUsersListHandler(Handler):
    @admin_required
    def get(self):
        users = User.query().fetch()
        params = {"users": users}
        self.render_template("admin/users_list.html", params)


class AdminUserDetailsHandler(Handler):
    @admin_required
    def get(self, user_id):
        user = User.get_by_id(int(user_id))
        params = {"this_user": user}
        self.render_template("admin/user_details.html", params)