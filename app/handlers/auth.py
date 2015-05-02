from app.handlers.base import Handler
from google.appengine.api import users
from app.models.auth import User


class LoginHandler(Handler):
    def get(self):
        self.redirect(users.create_login_url(self.request.uri))


class LogoutHandler(Handler):
    def get(self):
        self.redirect(users.create_logout_url("/"))


class ForbiddenHandler(Handler):
    def get(self):
        self.render_template("403.html")


class NotExistHandler(Handler):
    def get(self):
        self.render_template("404.html")


class OopsHandler(Handler):
    def get(self):
        self.render_template("oops.html")


class ProfileHandler(Handler):
    def get(self):
        current_user = users.get_current_user()
        profile = User.query(User.email == str(current_user.email())).get()
        if not profile:
            profile = User()
            profile.email = current_user.email().lower()
            profile.put()

        params = {"profile": profile}
        self.render_template("admin/profile.html", params)