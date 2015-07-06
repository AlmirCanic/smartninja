from google.appengine.ext import ndb


class Franchise(ndb.Model):
    title = ndb.StringProperty()  # title within SmartNinja group
    full_company_name = ndb.StringProperty()  # full company name
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
    def create(cls, title, full_company_name, street, city, zip, country, website, tax_number):
        franchise = cls(title=title, full_company_name=full_company_name, street=street, city=city, zip=zip,
                        country=country, website=website, tax_number=tax_number)
        franchise.put()
        return franchise

    @classmethod
    def update(cls, franchise, title, full_company_name, street, city, zip, country, website, tax_number):
        franchise.title = title
        franchise.full_company_name = full_company_name
        franchise.street = street
        franchise.city = city
        franchise.zip = zip
        franchise.country = country
        franchise.website = website
        franchise.tax_number = tax_number
        franchise.put()
        return franchise