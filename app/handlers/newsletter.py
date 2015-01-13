from google.appengine.api import urlfetch
from app.handlers.base import Handler
from app.utils.secret import get_mailchimp_api, get_newsletter_list_id


class NewsletterSubscribeHandler(Handler):
    def get(self):
        # TODO: Remove this method!!! (just for testing purposes)
        self.render_template("public/newsletter_thanks.html")

    def post(self):
        hidden = self.request.get("hidden")
        email = self.request.get("email_newsletter1")
        if hidden:
            self.render_template("public/main2.html")
        elif email:
            url = "https://us9.api.mailchimp.com/2.0/lists/subscribe.json?apikey="+get_mailchimp_api()+"&id="+get_newsletter_list_id()+"&email[email]="+str(email)

            try:
                result = urlfetch.fetch(url=url, method=urlfetch.POST, headers={'Content-Type': 'application/json'})
                params = {"error": "Email oddan! :)"}
            except Exception, e:
                params = {"error": "Problem pri prijavi na e-novice. Prosim pisi na info@startup.org."}
            self.render_template("public/newsletter_thanks.html", params)