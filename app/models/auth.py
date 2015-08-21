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
    instructor = ndb.BooleanProperty(default=False, indexed=False)  # is user an instructor?
    summary = ndb.StringProperty(indexed=False)
    long_description = ndb.TextProperty(indexed=False)
    photo_url = ndb.StringProperty(indexed=False)
    github_url = ndb.StringProperty(indexed=False)
    linkedin_url = ndb.StringProperty(indexed=False)
    homepage_url = ndb.StringProperty(indexed=False)
    other_skills = ndb.StringProperty(repeated=True)  # skills put in by the user
    cv_blob = ndb.BlobKeyProperty(indexed=False)
    photo_blob = ndb.BlobKeyProperty(indexed=False)
    started_programming = ndb.DateProperty()
    grade_avg_score = ndb.FloatProperty(default=0.0)
    grade_all_tags = ndb.StringProperty(repeated=True)  # skills user acquired at smartninja courses. Other skills are under other_skills field
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
    def get_by_id_non_deleted(cls, user_id):
        user = User.get_by_id(user_id)
        if user and not user.deleted:
            return user
        else:
            return None

    @classmethod
    def short_create(cls, email, first_name=None, last_name=None):
        user = cls(email=email.lower(), first_name=first_name, last_name=last_name)
        user.put()
        return user

    @classmethod
    def get_or_short_create(cls, email, first_name=None, last_name=None):
        user = cls.query(User.email == email.lower()).get()
        if user and user.deleted:
            user.deleted = False
            user.put()
        elif not user:
            user = cls.short_create(email=email.lower(), first_name=first_name, last_name=last_name)
        return user

    @classmethod
    def create(cls, first_name, last_name, email, address, phone_number, dob):
        user = cls.query(User.email == email.lower()).get()
        if user and user.deleted:
            user.deleted = False
            if not user.address:
                user.address = address
            if not user.phone_number:
                user.phone_number = phone_number
            if not user.dob:
                user.dob = dob
            user.put()
        elif not user:
            user = cls(first_name=first_name, last_name=last_name, email=email.lower(), address=address,
                       phone_number=phone_number, dob=dob)
            user.put()
        return user

    @classmethod
    def update(cls, user, first_name, last_name, address, phone_number, summary, photo_url, dob, email=None,
               instructor=False, github=None, job_searching=None, current_town=None, linkedin=None, homepage=None,
               started_programming=None, long_description=None, other_skills=None):
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
        if other_skills != None:
            user.other_skills = other_skills
        user.dob = dob
        user.put()
        return user

    @classmethod
    def update_none(cls, user, address=None, phone_number=None, summary=None, photo_url=None, dob=None, email=None,
                    instructor=None, github=None, job_searching=None, current_town=None, linkedin=None, homepage=None,
                    started_programming=None, long_description=None, other_skills=None):
        if address != None:
            user.address = address
        if phone_number != None:
            user.phone_number = phone_number
        if summary != None:
            user.summary = summary
        if email != None:
            user.email = email.lower()
        if photo_url != None:
            user.photo_url = photo_url
        if instructor != None:
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
        if other_skills != None:
            user.other_skills = other_skills
        if dob != None:
            user.dob = dob
        user.put()
        return user