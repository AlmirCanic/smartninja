from google.appengine.ext import ndb


class Lesson(ndb.Model):
    title = ndb.StringProperty()
    order = ndb.IntegerProperty(default=1)
    text = ndb.TextProperty()
    course_type = ndb.IntegerProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)

    @property
    def get_id(self):
        return self.key.id()

    @classmethod
    def create(cls, title, order, text, course_type):
        lesson = cls(title=title, order=order, text=text, course_type=course_type)
        lesson.put()
        return lesson

    @classmethod
    def update(cls, lesson, title, order, text, course_type):
        lesson.title = title
        lesson.order = order
        lesson.text = text
        lesson.course_type = course_type
        lesson.put()
        return lesson

    @classmethod
    def delete(cls, lesson):
        lesson.deleted = True
        lesson.put()