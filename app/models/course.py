from google.appengine.ext import ndb


class CourseType(ndb.Model):
    title = ndb.StringProperty()
    curriculum = ndb.StringProperty()
    description = ndb.TextProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)

    @property
    def get_id(self):
        return self.key.id()

    @classmethod
    def create(cls, title, curriculum, description):
        course_type = cls(title=title, curriculum=curriculum, description=description)
        course_type.put()
        return course_type


class Course(ndb.Model):
    title = ndb.StringProperty()
    course_type = ndb.IntegerProperty()
    city = ndb.StringProperty()
    place = ndb.StringProperty()
    spots = ndb.IntegerProperty()  # Number of spots available for students
    taken = ndb.IntegerProperty(default=0)  # Number of spots TAKEN
    description = ndb.TextProperty()
    start_date = ndb.DateProperty()
    end_date = ndb.DateProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    price = ndb.FloatProperty(repeated=True)
    currency = ndb.StringProperty()
    deleted = ndb.BooleanProperty(default=False)

    @property
    def get_id(self):
        return self.key.id()

    @classmethod
    def create(cls, title, course_type, city, place, spots, description, start_date, end_date, price, currency):
        course = cls(title=title, course_type=course_type, city=city, place=place, spots=spots, description=description,
                     start_date=start_date, end_date=end_date, price=price, currency=currency)
        course.put()
        return course

    @classmethod
    def update(cls, course, title, course_type, city, place, spots, description, start_date, end_date, price, currency):
        course.title = title
        course.course_type = course_type
        course.city = city
        course.place = place
        course.spots = spots
        course.description = description
        course.start_date = start_date
        course.end_date = end_date
        course.price = price
        course.currency = currency
        course.put()
        return course


class CourseApplication(ndb.Model):
    course_title = ndb.StringProperty()
    course_id = ndb.IntegerProperty()
    student_name = ndb.StringProperty()
    student_id = ndb.IntegerProperty()
    student_email = ndb.StringProperty()
    price = ndb.FloatProperty()
    payment_status = ndb.BooleanProperty(default=False)
    currency = ndb.StringProperty()
    laptop = ndb.StringProperty()
    shirt = ndb.StringProperty()
    deleted = ndb.BooleanProperty(default=False)

    @property
    def get_id(self):
        return self.key.id()

    @classmethod
    def create(cls, course_title, course_id, student_name, student_id, student_email, price, currency, laptop, shirt):
        course_app = cls(course_title=course_title, course_id=course_id, student_name=student_name, student_id=student_id,
                         student_email=student_email, price=price, currency=currency, laptop=laptop, shirt=shirt)
        course_app.put()
        return course_app