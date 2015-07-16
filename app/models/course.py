from google.appengine.ext import ndb
from app.models.franchise import FranchiseList
from app.models.partner import Partner, PartnerUserCourse
from app.utils.course_utils import update_student_grade


class CourseType(ndb.Model):
    title = ndb.StringProperty()
    curriculum = ndb.StringProperty()
    description = ndb.TextProperty()
    franchises = ndb.StructuredProperty(modelclass=FranchiseList, repeated=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)

    @property
    def get_id(self):
        return self.key.id()

    @classmethod
    def create(cls, title, curriculum, description, franchises):
        course_type = cls(title=title, curriculum=curriculum, description=description, franchises=franchises)
        course_type.put()
        return course_type

    @classmethod
    def update(cls, course_type, title, curriculum, description, franchises):
        course_type.title = title
        course_type.curriculum = curriculum
        course_type.description = description
        course_type.franchises = franchises
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
    long_description = ndb.TextProperty()
    photo_url = ndb.StringProperty()
    user_id = ndb.IntegerProperty()


class Course(ndb.Model):
    title = ndb.StringProperty()
    course_type = ndb.IntegerProperty()
    level = ndb.IntegerProperty()  # 1-beginner, 2-intermediate, 3-advanced
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
    franchise_id = ndb.IntegerProperty()
    franchise_title = ndb.StringProperty()
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
               category, course_instructors, image_url, partners, tags, franchise, level=None):
        course = cls(title=title, course_type=course_type, city=city, place=place, spots=spots, summary=summary,
                     description=description, start_date=start_date, end_date=end_date, prices=prices, currency=currency,
                     category=category, course_instructors=course_instructors, image_url=image_url, partners=partners,
                     tags=tags, level=level, franchise_id=franchise.get_id, franchise_title=franchise.title)
        course.put()
        return course

    @classmethod
    def update(cls, course, title, course_type, city, place, spots, summary, description, start_date, end_date, prices,
               currency, category, course_instructors, image_url, partners, tags, closed, level, franchise=None):

        if course.title != title or course.start_date != start_date or course.city != city or course.level != level:
            applications = CourseApplication.query(CourseApplication.course_id == course.get_id).fetch()

            for application in applications:
                application.course_title = title
                application.course_level = level
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
        course.level = level
        if franchise != None:  # needed because manager cannot edit franchise (only admin can)
            course.franchise_id = franchise.get_id
            course.franchise_title = franchise.title
        course.applications_closed = closed
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
    course_level = ndb.IntegerProperty()
    grade_score = ndb.IntegerProperty()
    grade_summary = ndb.TextProperty()
    grade_tags = ndb.StringProperty(repeated=True)
    grade_top_student = ndb.BooleanProperty(default=False)

    @property
    def get_id(self):
        return self.key.id()

    @classmethod
    def create(cls, course, student_name, student_id, student_email, price, currency, laptop, shirt,
               company_invoice=False, company_title=None, company_address=None, company_town=None, company_zip=None,
               company_tax_number=None, other_info=None):
        course_app = cls(course_title=course.title, course_id=course.get_id, student_name=student_name, student_id=student_id,
                         student_email=student_email.lower(), price=price, currency=currency, laptop=laptop, shirt=shirt,
                         company_invoice=company_invoice, company_title=company_title, company_address=company_address,
                         company_town=company_town, company_zip=company_zip, company_tax_number=company_tax_number,
                         other_info=other_info, course_level=course.level)
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
    def move_student_to_another_course(cls, application, old_course, new_course):
        application.course_id = new_course.get_id
        application.course_title = new_course.title
        application.course_level = new_course.level
        application.put()
        old_course.taken -= 1
        old_course.put()
        new_course.taken += 1
        new_course.put()

    @classmethod
    def grade_student(cls, application, score, summary, tags, top_student=False):
        application.grade_score = score
        application.grade_summary = summary
        application.grade_tags = tags
        application.grade_top_student = top_student
        application.put()

        update_student_grade(application)
