from app.emails.contact import email_contact_us_to_smartninja
from app.handlers.base import Handler
from app.settings import is_local


class PublicContactUsHandler(Handler):
    def post(self):
        hidden = self.request.get("hidden")
        first_name = self.request.get("first_name")
        last_name = self.request.get("last_name")
        email = self.request.get("email")
        phone = self.request.get("phone")
        message = self.request.get("message")

        if hidden:
            return self.redirect_to("oops")

        if first_name and email and message:
            if not is_local():
                email_contact_us_to_smartninja(first_name=first_name, last_name=last_name, email=email, phone=phone,
                                               message=message)

        return self.redirect_to("public-contact-thanks")


class PublicContactThankYou(Handler):
    def get(self):
        self.render_template("public/contact_thanks.html")