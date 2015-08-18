from google.appengine.ext import ndb
from app.models.instructor import Instructor
from app.models.job import Job


class JobApplication(ndb.Model):
    full_name = ndb.StringProperty()
    user_id = ndb.IntegerProperty()
    instructor_id = ndb.IntegerProperty()
    job_id = ndb.IntegerProperty()
    job_title = ndb.StringProperty()
    curriculum_id = ndb.IntegerProperty()
    curriculum_title = ndb.StringProperty()
    city = ndb.StringProperty()
    email = ndb.StringProperty()
    phone = ndb.StringProperty()
    github_url = ndb.StringProperty()
    linkedin_url = ndb.StringProperty()
    experience = ndb.TextProperty()  # applicant describes their experience with technology and teaching
    other_info = ndb.TextProperty()  # other info that applicant adds in the application
    manager_notes = ndb.TextProperty()  # notes by manager about the applicant
    manager_grade = ndb.IntegerProperty()  # manager grades applicant about these exact job requirements
    created = ndb.DateTimeProperty(auto_now_add=True)
    contacted = ndb.BooleanProperty(default=False)
    approved = ndb.BooleanProperty(default=False)
    deleted = ndb.BooleanProperty(default=False)

    @property
    def get_id(self):
        return self.key.id()

    @classmethod
    def create(cls, instructor, job, city, email, phone, github_url, linkedin_url, experience, other_info):
        application = cls(full_name=instructor.full_name, user_id=instructor.user_id, instructor_id=instructor.get_id,
                          job_id=job.get_id, job_title=job.title, curriculum_id=job.curriculum_id,
                          curriculum_title=job.curriculum_title, city=city, email=email, phone=phone,
                          github_url=github_url, linkedin_url=linkedin_url, experience=experience, other_info=other_info)
        application.put()

        job.applied += 1  # increase the number of applicants in job by one
        job.put()
        return application

    @classmethod
    def update(cls, application, phone, city, linkedin, github):
        application.phone = phone
        application.city = city
        application.linkedin_url = linkedin
        application.github_url = github
        application.put()
        return application

    @classmethod
    def contacted_and_approved(cls, application, contacted, approved):
        """Manager fills a checkbox if user has already been contacted and, after that, if user has been approved to
        be a SmartNinja instructor for this particular job/curriculum"""
        application.contacted = contacted
        application.approved = approved
        application.put()

        if approved:
            instructor = Instructor.get_by_id(application.instructor_id)
            Instructor.add_curriculum(instructor=instructor, curriculum_id=application.curriculum_id,
                                      curriculum_title=application.curriculum_title)
        return application

    @classmethod
    def delete(cls, application):
        application.deleted = True
        application.put()

        job = Job.get_by_id(application.job_id)
        job.applied -= 1
        job.put()

        return True