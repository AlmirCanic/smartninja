from google.appengine.ext import ndb


class Employer(ndb.Model):
    full_name = ndb.StringProperty()
    user_id = ndb.IntegerProperty()
    email = ndb.StringProperty()
    partner_id = ndb.IntegerProperty()
    partner_title = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

    @property
    def get_id(self):
        return self.key.id()

    @classmethod
    def create(cls, full_name, user_id, email, partner=None):
        employer = cls(full_name=full_name, user_id=user_id, email=email.lower())

        if partner != None:
            employer.partner_id = partner.get_id
            employer.partner_title = partner.title

        employer.put()
        return employer