from google.appengine.ext import ndb


class ContactCandidate(ndb.Model):
    candidate_name = ndb.StringProperty()
    candidate_user_id = ndb.IntegerProperty()
    candidate_email = ndb.StringProperty()
    employer_name = ndb.StringProperty()
    employer_user_id = ndb.IntegerProperty()
    employer_email = ndb.StringProperty()
    employer_company_id = ndb.IntegerProperty()
    employer_company_title = ndb.StringProperty()
    message = ndb.TextProperty()
    successful_employment = ndb.BooleanProperty(default=False)
    deleted = ndb.BooleanProperty(default=False)
    created = ndb.DateTimeProperty(auto_now_add=True)

    @property
    def get_id(self):
        return self.key.id()

    @classmethod
    def create(cls, candidate, employer_user, message):
        contact_candidate = cls(candidate_name=candidate.get_full_name, candidate_user_id=candidate.get_id,
                                candidate_email=candidate.email, employer_name=employer_user.get_full_name,
                                employer_user_id=employer_user.get_id, employer_email=employer_user.email,
                                message=message)
        contact_candidate.put()
        return contact_candidate

    @classmethod
    def delete(cls, contact_candidate):
        contact_candidate.deleted = True
        contact_candidate.put()
        return True