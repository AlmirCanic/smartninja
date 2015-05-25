from google.appengine.ext import ndb


class Employer(ndb.Model):
    full_name = ndb.StringProperty()
    user_id = ndb.IntegerProperty()
    email = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

    @property
    def get_id(self):
        return self.key.id()

    @classmethod
    def create(cls, full_name, user_id, email):
        employer = cls(full_name=full_name, user_id=user_id, email=email.lower())
        employer.put()
        return employer