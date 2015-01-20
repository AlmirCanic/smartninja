from app.handlers.base import Handler


class MainHandler(Handler):
    def get(self):
        self.render_template("public/main.html")


class TempMainHandler(Handler):
    def get(self):
        self.render_template("public/main2.html")


class PublicPartnersHandler(Handler):
    def get(self):
        self.render_template("public/partners.html")


class PublicAboutHandler(Handler):
    def get(self):
        self.render_template("public/about.html")


class PublicFaqHandler(Handler):
    def get(self):
        self.render_template("public/faq.html")


class PublicComingSoonHandler(Handler):
    def get(self):
        self.render_template("public/coming_soon.html")


class PublicApplyThankYouHandler(Handler):
    def get(self):
        self.render_template("public/apply_thank_you.html")


class PublicNewsletterThankYouHandler(Handler):
    def get(self):
        self.render_template("public/newsletter_thank_you_1.html")


class PublicNewsletterThankYou2Handler(Handler):
    def get(self):
        self.render_template("public/newsletter_thank_you_2.html")