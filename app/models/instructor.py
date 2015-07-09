from google.appengine.ext import ndb
from app.models.franchise import FranchiseList


class Instructor(ndb.Model):
    full_name = ndb.StringProperty()
    user_id = ndb.IntegerProperty()
    email = ndb.StringProperty()
    franchises = ndb.StructuredProperty(modelclass=FranchiseList, repeated=True)
    created = ndb.DateTimeProperty(auto_now_add=True)

    @property
    def get_id(self):
        return self.key.id()

    @classmethod
    def create(cls, full_name, user_id, email, franchises):
        instructor = cls(full_name=full_name, user_id=user_id, email=email.lower(), franchises=franchises)
        instructor.put()
        return instructor