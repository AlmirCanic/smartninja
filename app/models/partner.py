from google.appengine.ext import ndb


class Partner(ndb.Model):
    title = ndb.StringProperty()
    summary = ndb.StringProperty()
    website = ndb.StringProperty()
    country = ndb.StringProperty()
    logo = ndb.StringProperty()
    description = ndb.TextProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)

    @property
    def get_id(self):
        return self.key.id()

    @classmethod
    def create(cls, title, summary, website, country, logo, description):
        partner = cls(title=title, summary=summary, website=website, description=description, country=country, logo=logo)
        partner.put()
        return partner

    @classmethod
    def update(cls, partner, title, summary, website, country, logo, description):
        partner.title = title
        partner.summary = summary
        partner.website = website
        partner.country = country
        partner.logo = logo
        partner.description = description
        partner.put()
        return partner