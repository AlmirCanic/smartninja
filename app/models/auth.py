from google.appengine.ext import ndb
from app.utils.user_utils import change_name


class User(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    address = ndb.StringProperty()
    current_town = ndb.StringProperty()
    phone_number = ndb.StringProperty()
    dob = ndb.StringProperty()  # date of birth
    created = ndb.DateTimeProperty(auto_now_add=True)
    student_courses = ndb.StringProperty(repeated=True)  # list of course IDs where this user is student
    instructor_courses = ndb.StringProperty(repeated=True)  # list of course IDs where this user is instructor
    instructor = ndb.BooleanProperty(default=False)  # is user an instructor?
    summary = ndb.StringProperty()
    long_description = ndb.TextProperty()
    photo_url = ndb.StringProperty()
    github_url = ndb.StringProperty()
    linkedin_url = ndb.StringProperty()
    homepage_url = ndb.StringProperty()
    cv_blob = ndb.BlobKeyProperty()
    started_programming = ndb.DateProperty()
    grade_avg_score = ndb.FloatProperty(default=0.0)
    grade_all_tags = ndb.StringProperty(repeated=True)
    grade_top_student = ndb.IntegerProperty(default=0)  # How many times did student receive Top student award by instructor
    job_searching = ndb.BooleanProperty(default=False)
    contacted_by = ndb.IntegerProperty(repeated=True)  # companies (partner ids) or employers that contacted user for a job opportunity
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
        user = User.query(User.email == email.lower(), User.deleted == False).get()
        return user

    @classmethod
    def short_create(cls, email, first_name=None, last_name=None):
        user = cls(email=email.lower(),
                   first_name=first_name,
                   last_name=last_name)
        user.put()
        return user

    @classmethod
    def create(cls, first_name, last_name, email, address, phone_number, dob):
        user = cls(first_name=first_name,
                   last_name=last_name,
                   email=email.lower(),
                   address=address,
                   phone_number=phone_number,
                   dob=dob)
        user.put()
        return user

    @classmethod
    def update(cls, user, first_name, last_name, address, phone_number, summary, photo_url, dob, email=None,
               instructor=False, github=None, job_searching=None, current_town=None, linkedin=None, homepage=None,
               started_programming=None, long_description=None):
        change_name(user, first_name, last_name)

        user.address = address
        user.phone_number = phone_number
        user.summary = summary
        if email != None:
            user.email = email.lower()
        user.photo_url = photo_url
        user.instructor = instructor
        if github != None:
            user.github_url = github
        if linkedin != None:
            user.linkedin_url = linkedin
        if job_searching != None:
            user.job_searching = job_searching
        if current_town != None:
            user.current_town = current_town
        if homepage != None:
            user.homepage_url = homepage
        if started_programming != None:
            user.started_programming = started_programming
        if long_description != None:
            user.long_description = long_description
        user.dob = dob
        user.put()
        return user