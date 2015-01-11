import urllib2
from app.handlers.base import Handler
from app.utils.secret import get_mailchimp_api


class NewsletterSubscribeHandler(Handler):
    def post(self):
        hidden = self.request.get("hidden")
        if hidden:
            return self.redirect_to("temp")
        else:
            email = self.request.get("email")
            m = get_mailchimp_api()
            req = urllib2.Request("https://us9.api.mailchimp.com/2.0/helper/ping")
            try:
                resp = urllib2.urlopen(req)
                params = {"message": resp.read()}
                return self.write(resp.read())
            except Exception, e:
                return self.write("forbidden")