from google.appengine.ext import ndb


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

    @property
    def get_id(self):
        return self.key.id()

    @property
    def get_full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

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