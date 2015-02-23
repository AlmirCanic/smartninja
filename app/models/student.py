from google.appengine.ext import ndb


class StudentCourse(ndb.Model):
    """Student (user) access to course"""
    user_id = ndb.IntegerProperty()
    user_name = ndb.StringProperty()
    user_email = ndb.StringProperty()
    course_id = ndb.IntegerProperty()
    course_title = ndb.StringProperty()
    course_city = ndb.StringProperty()
    course_start_date = ndb.DateProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)

    @property
    def get_id(self):
        return self.key.id()

    @classmethod
    def create(cls, user_id, user_name, user_email, course):
        student = cls(user_id=user_id, user_name=user_name, user_email=user_email, course_id=course.get_id,
                      course_title=course.title, course_city=course.city, course_start_date=course.start_date)
        student.put()
        return student

    @classmethod
    def update(cls, student, user_id, user_name, user_email, course):
        student.user_id = user_id
        student.user_name = user_name
        student.user_email = user_email
        student.course_id = course.get_id
        student.course_title = course.title
        student.course_city = course.city
        student.course_start_date = course.start_date
        student.put()
        return student

    @classmethod
    def delete(cls, student):
        student.deleted = True
        student.put()