from google.appengine.api import urlfetch
from app.handlers.base import Handler
from app.settings import is_local
from app.utils.secret import get_mailchimp_api, get_newsletter_list_id


class NewsletterSubscribeHandler(Handler):
    def post(self):
        hidden = self.request.get("hidden")
        email = self.request.get("email_newsletter1")
        if hidden:
            self.redirect_to("oops")
        elif email:
            if not is_local():
                subscribe_mailchimp(email=email)
            self.redirect_to("newsletter-thank-you-2")


def subscribe_mailchimp(email):
    url = "https://us9.api.mailchimp.com/2.0/lists/subscribe.json?apikey="+get_mailchimp_api()+"&id="+get_newsletter_list_id()+"&email[email]="+str(email)

    try:
        result = urlfetch.fetch(url=url, method=urlfetch.POST, headers={'Content-Type': 'application/json'})
        params = {"error": "Email oddan! :)"}
    except Exception, e:
        params = {"error": "Problem pri prijavi na e-novice. Prosim pisi na info@startup.org."}

    return params