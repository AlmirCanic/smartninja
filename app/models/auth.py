from google.appengine.ext import ndb
from app.models.course import CourseApplication
from app.settings import ADMINS


class User(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    address = ndb.StringProperty()
    phone_number = ndb.StringProperty()
    dob = ndb.StringProperty()  # date of birth
    created = ndb.DateTimeProperty(auto_now_add=True)
    student = ndb.StringProperty(repeated=True)  # list of course IDs where this user is student
    instructor = ndb.StringProperty(repeated=True)  # list of course IDs where this user is instructor
    deleted = ndb.BooleanProperty(default=False)

    @property
    def get_id(self):
        return self.key.id()

    @property
    def get_full_name(self):
        if self.first_name and self.last_name:
            return "%s %s" % (self.first_name, self.last_name)
        else:
            return self.email

    @classmethod
    def get_by_email(cls, email):
        user = User.query(User.email == email).get()
        return user

    @classmethod
    def create(cls, first_name, last_name, email, address, phone_number, dob):
        user = cls(first_name=first_name,
                   last_name=last_name,
                   email=email,
                   address=address,
                   phone_number=phone_number,
                   dob=dob)
        user.put()
        return user

    @classmethod
    def update(cls, user, first_name, last_name, address, phone_number):
        if user.first_name != first_name or user.last_name != last_name:
            user.first_name = first_name
            user.last_name = last_name
            applications = CourseApplication.query(CourseApplication.student_id == user.get_id).fetch()

            for application in applications:
                application.student_name = "%s %s" % (first_name, last_name)
                application.put()

        user.address = address
        user.phone_number = phone_number
        user.put()
        return user