from google.appengine.ext import ndb


class Job(ndb.Model):
    title = ndb.StringProperty()
    curriculum_id = ndb.IntegerProperty()
    curriculum_title = ndb.StringProperty()
    city = ndb.StringProperty()
    franchise_id = ndb.IntegerProperty()
    franchise_title = ndb.IntegerProperty()
    description = ndb.TextProperty()
    applied = ndb.IntegerProperty(default=0)  # number of applications
    created = ndb.DateTimeProperty(auto_now_add=True)
    active = ndb.BooleanProperty(default=True)  # when Job is active, it is shown/available publicly
    deleted = ndb.BooleanProperty(default=False)

    @property
    def get_id(self):
        return self.key.id()

    @classmethod
    def create(cls, title, curriculum, city, franchise, description):
        job = cls(title=title, curriculum_id=curriculum.get_id, curriculum_title=curriculum.title, city=city,
                  franchise_id=franchise.get_id, franchise_title=franchise.title, description=description)
        job.put()
        return job

    @classmethod
    def update(cls, job, title, curriculum, city, description):
        job.title = title
        job.curriculum_id = curriculum.get_id
        job.curriculum_title = curriculum.title
        job.city = city
        job.description = description
        job.put()
        return job

    @classmethod
    def delete(cls, job):
        job.active = False
        job.deleted = True
        job.put()
        return True