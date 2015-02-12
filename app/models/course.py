from google.appengine.ext import ndb
from app.models.partner import Partner, PartnerUserCourse


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


class Price(ndb.Model):
    price_dot = ndb.FloatProperty()
    price_comma = ndb.StringProperty()
    summary = ndb.StringProperty()
    notes = ndb.StringProperty()


class CourseInstructor(ndb.Model):
    name = ndb.StringProperty()
    summary = ndb.StringProperty()
    photo_url = ndb.StringProperty()
    user_id = ndb.IntegerProperty()


class Course(ndb.Model):
    title = ndb.StringProperty()
    course_type = ndb.IntegerProperty()
    city = ndb.StringProperty()
    place = ndb.StringProperty()
    category = ndb.StringProperty()
    spots = ndb.IntegerProperty()  # Number of spots available for students
    taken = ndb.IntegerProperty(default=0)  # Number of spots TAKEN
    summary = ndb.StringProperty()
    description = ndb.TextProperty()
    start_date = ndb.DateProperty()
    end_date = ndb.DateProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    price = ndb.FloatProperty(repeated=True)
    instructor = ndb.IntegerProperty()
    instructor_name = ndb.StringProperty()
    currency = ndb.StringProperty()
    image_url = ndb.StringProperty()
    deleted = ndb.BooleanProperty(default=False)
    prices = ndb.StructuredProperty(modelclass=Price, repeated=True)
    course_instructors = ndb.StructuredProperty(modelclass=CourseInstructor, repeated=True)
    partners = ndb.StructuredProperty(modelclass=Partner, repeated=True)
    applications_closed = ndb.BooleanProperty(default=False)
    tags = ndb.StringProperty(repeated=True)

    @property
    def get_id(self):
        return self.key.id()

    @classmethod
    def create(cls, title, course_type, city, place, spots, summary, description, start_date, end_date, prices, currency,
               category, course_instructors, image_url, partners, tags):
        course = cls(title=title, course_type=course_type, city=city, place=place, spots=spots, summary=summary,
                     description=description, start_date=start_date, end_date=end_date, prices=prices, currency=currency,
                     category=category, course_instructors=course_instructors, image_url=image_url, partners=partners,
                     tags=tags)
        course.put()
        return course

    @classmethod
    def update(cls, course, title, course_type, city, place, spots, summary, description, start_date, end_date, prices,
               currency, category, course_instructors, image_url, partners, tags):

        if course.title != title or course.start_date != start_date or course.city != city:
            applications = CourseApplication.query(CourseApplication.course_id == course.get_id).fetch()

            for application in applications:
                application.course_title = title
                application.put()

            pucs = PartnerUserCourse.query(PartnerUserCourse.course_id == course.get_id).fetch()

            for puc in pucs:
                puc.course_title = title
                puc.start_date = start_date
                puc.city = city
                puc.put()

        course.title = title
        course.course_type = course_type
        course.city = city
        course.place = place
        course.spots = spots
        course.summary = summary
        course.description = description
        course.start_date = start_date
        course.end_date = end_date
        course.prices = prices
        course.currency = currency
        course.category = category
        course.partners = partners
        course.course_instructors = course_instructors
        course.image_url = image_url
        course.tags = tags
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
    invoice = ndb.StringProperty()
    deleted = ndb.BooleanProperty(default=False)
    created = ndb.DateTimeProperty(auto_now_add=True)
    company_invoice = ndb.BooleanProperty(default=False)
    company_title = ndb.StringProperty()
    company_address = ndb.StringProperty()
    company_town = ndb.StringProperty()
    company_zip = ndb.StringProperty()
    company_tax_number = ndb.StringProperty()
    other_info = ndb.TextProperty()

    @property
    def get_id(self):
        return self.key.id()

    @classmethod
    def create(cls, course, student_name, student_id, student_email, price, currency, laptop, shirt,
               company_invoice=False, company_title=None, company_address=None, company_town=None, company_zip=None,
               company_tax_number=None, other_info=None):
        course_app = cls(course_title=course.title, course_id=course.get_id, student_name=student_name, student_id=student_id,
                         student_email=student_email, price=price, currency=currency, laptop=laptop, shirt=shirt,
                         company_invoice=company_invoice, company_title=company_title, company_address=company_address,
                         company_town=company_town, company_zip=company_zip, company_tax_number=company_tax_number,
                         other_info=other_info)
        course_app.put()
        course.taken += 1
        course.put()
        return course_app

    @classmethod
    def delete(cls, application):
        application.deleted = True
        application.put()
        course = Course.get_by_id(int(application.course_id))
        course.taken -= 1
        course.put()

    @classmethod
    def create_temp(cls, course_title, course_id, student_name, student_id, student_email, price, currency, laptop, shirt):
        course_app = cls(course_title=course_title, course_id=course_id, student_name=student_name, student_id=student_id,
                         student_email=student_email, price=price, currency=currency, laptop=laptop, shirt=shirt)
        course_app.put()
        return course_app