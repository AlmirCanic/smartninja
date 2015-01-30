from google.appengine.ext import ndb


class Partner(ndb.Model):
    title = ndb.StringProperty()
    summary = ndb.StringProperty()
    website = ndb.StringProperty()
    description = ndb.TextProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)

    @property
    def get_id(self):
        return self.key.id()

    @classmethod
    def create(cls, title, summary, website, description):
        partner = cls(title=title, summary=summary, website=website, description=description)
        partner.put()
        return partner