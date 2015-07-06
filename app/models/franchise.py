from google.appengine.ext import ndb


class Franchise(ndb.Model):
    title = ndb.StringProperty()  # full company name
    street = ndb.StringProperty()  # street and street number
    city = ndb.StringProperty()
    zip = ndb.StringProperty()
    country = ndb.StringProperty()
    website = ndb.StringProperty()
    tax_number = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)

    @property
    def get_id(self):
        return self.key.id()

    @classmethod
    def create(cls, title, street, city, zip, country, website, tax_number):
        franchise = cls(title=title, street=street, city=city, zip=zip, country=country, website=website,
                        tax_number=tax_number)
        franchise.put()
        return franchise