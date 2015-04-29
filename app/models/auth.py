from google.appengine.ext import ndb
from app.utils.user_utils import change_name_or_email


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
    github_url = ndb.StringProperty()
    grade_avg_score = ndb.FloatProperty()
    grade_all_tags = ndb.StringProperty(repeated=True)
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
    def update(cls, user, first_name, last_name, address, phone_number, summary, photo_url, dob, email=None,
               instructor=False, github=None):
        change_name_or_email(user, first_name, last_name, email)

        user.address = address
        user.phone_number = phone_number
        user.summary = summary
        if email != None:
            user.email = email
        user.photo_url = photo_url
        user.instructor = instructor
        if github != None:
            user.github_url = github
        user.dob = dob
        user.put()
        return user