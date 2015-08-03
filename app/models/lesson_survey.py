from google.appengine.ext import ndb


class LessonSurvey(ndb.Model):
    lesson_title = ndb.StringProperty()
    lesson_id = ndb.IntegerProperty()
    lesson_order = ndb.IntegerProperty()
    course_title = ndb.StringProperty()
    course_id = ndb.IntegerProperty()
    instructor_name = ndb.StringProperty()
    instructor_user_id = ndb.IntegerProperty()
    questions = ndb.JsonProperty()
    text = ndb.TextProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)

    @property
    def get_id(self):
        return self.key.id()

    @classmethod
    def create(cls, lesson, course, statements, text):
        survey = cls(lesson_title=lesson.title, lesson_id=lesson.get_id, course_title=course.title,
                     course_id=course.get_id, instructor_name=course.course_instructors[0].name,
                     instructor_user_id=course.course_instructors[0].user_id, questions=statements, text=text,
                     lesson_order=lesson.order)
        survey.put()
        return survey