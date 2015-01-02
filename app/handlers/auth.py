from app.handlers.base import Handler
from google.appengine.api import users


class LoginHandler(Handler):
    def get(self):
        self.redirect(users.create_login_url("/"))


class LogoutHandler(Handler):
    def get(self):
        self.redirect(users.create_logout_url("/"))