from app.handlers.base import Handler
from app.models.auth import User
from app.utils.decorators import admin_required
from app.utils.user_utils import change_email


class AdminUserChangeEmailHandler(Handler):
    @admin_required
    def get(self, user_id):
        user = User.get_by_id(int(user_id))
        params = {"this_user": user}
        self.render_template("admin/user_change_email.html", params)

    @admin_required
    def post(self, user_id):
        user = User.get_by_id(int(user_id))
        email = self.request.get("email")

        other_user = User.get_by_email(email=email)

        if not other_user:
            change_email(user, email)
            self.redirect_to("user-details", user_id=int(user_id))
        else:
            pass