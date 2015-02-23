from google.appengine.ext import ndb
from app.models.course import CourseApplication
from app.models.partner import PartnerUserCourse


class User(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    address = ndb.StringProperty()
    phone_number = ndb.StringProperty()
    dob = ndb.StringProperty()  # date of birth
    created = ndb.DateTimeProperty(auto_now_add=True)
    student_courses = ndb.StringProperty(repeated=True)  # list of course IDs where this user is student
    instructor_courses = ndb.StringProperty(repeated=True)  # list of course IDs where this user is instructor
    instructor = ndb.BooleanProperty(default=False)  # is user an instructor?
    summary = ndb.StringProperty()
    photo_url = ndb.StringProperty()
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
    def short_create(cls, email, first_name=None, last_name=None):
        user = cls(email=email,
                   first_name=first_name,
                   last_name=last_name)
        user.put()
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
    def update(cls, user, first_name, last_name, address, phone_number, summary, photo_url, dob, email=None, instructor=False):
        if user.first_name != first_name or user.last_name != last_name or user.email != email:
            user.first_name = first_name
            user.last_name = last_name
            applications = CourseApplication.query(CourseApplication.student_id == user.get_id).fetch()

            for application in applications:
                application.student_name = "%s %s" % (first_name, last_name)
                if email != None:
                    application.student_email = email
                application.put()

            pucs = PartnerUserCourse.query(PartnerUserCourse.user_id == user.get_id).fetch()

            for puc in pucs:
                puc.user_name = user.first_name + " " + user.last_name
                puc.put()

        user.address = address
        user.phone_number = phone_number
        user.summary = summary
        if email != None:
            user.email = email
        user.photo_url = photo_url
        user.instructor = instructor
        user.dob = dob
        user.put()
        return user