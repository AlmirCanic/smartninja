from google.appengine.ext import ndb


class Report(ndb.Model):
    lesson_date = ndb.DateProperty()
    course_id = ndb.IntegerProperty()
    course_title = ndb.StringProperty()
    author_id = ndb.IntegerProperty()
    author_name = ndb.StringProperty()
    text = ndb.TextProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)

    @property
    def get_id(self):
        return self.key.id()

    @classmethod
    def create(cls, lesson_date, course, author, text):
        report = cls(lesson_date=lesson_date, course_id=course.get_id, course_title=course.title,
                     author_id=author.get_id, author_name=author.get_full_name, text=text)
        report.put()
        return report

    @classmethod
    def update(cls, report, lesson_date, text):
        report.lesson_date = lesson_date
        report.text = text
        report.put()
        return report