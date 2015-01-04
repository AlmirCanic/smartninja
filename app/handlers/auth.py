from app.handlers.base import Handler
from google.appengine.api import users


class LoginHandler(Handler):
    def get(self):
        self.redirect(users.create_login_url("/admin/courses"))


class LogoutHandler(Handler):
    def get(self):
        self.redirect(users.create_logout_url("/"))


class ForbiddenHandler(Handler):
    def get(self):
        self.render_template('403.html')