from google.appengine.ext import ndb
from app.models.franchise import FranchiseList


class Instructor(ndb.Model):
    full_name = ndb.StringProperty()
    user_id = ndb.IntegerProperty()
    email = ndb.StringProperty()
    franchises = ndb.StructuredProperty(modelclass=FranchiseList, repeated=True)
    city = ndb.StringProperty()
    manager_notes = ndb.TextProperty()
    manager_grade = ndb.IntegerProperty()  # manager grades instructor about these exact job requirements
    skills = ndb.StringProperty(repeated=True)  # programming skills that instructor has (e.g.: PHP, Python, SQL, ...)
    active = ndb.BooleanProperty(default=False)
    created = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)

    @property
    def get_id(self):
        return self.key.id()

    @classmethod
    def create(cls, full_name, user_id, email, franchises, city=None):
        instructor = cls(full_name=full_name, user_id=user_id, email=email.lower(), franchises=franchises, city=city)
        instructor.put()
        return instructor

    @classmethod
    def add_or_create(cls, full_name, user_id, email, franchises, city=None):
        instructor = cls.query(Instructor.email == email).get()

        if instructor:
            existing_franchises = instructor.franchises
            if franchises[0] not in existing_franchises:
                existing_franchises.append(franchises[0])
                instructor.franchises = existing_franchises
                if not instructor.city:
                    instructor.city = city
                instructor.put()
        else:
            instructor = cls.create(full_name=full_name, email=email, user_id=user_id, franchises=franchises, city=city)

        return instructor