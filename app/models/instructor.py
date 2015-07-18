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

    @classmethod
    def add_or_create(cls, full_name, user_id, email, franchises):
        instructor = cls.query(Instructor.email == email).get()

        if instructor:
            existing_franchises = instructor.franchises
            if franchises[0] not in existing_franchises:
                existing_franchises.append(franchises[0])
                instructor.franchises = existing_franchises
                instructor.put()
        else:
            instructor = cls.create(full_name=full_name, email=email, user_id=user_id, franchises=franchises)

        return instructor