import csv
import datetime
from app.handlers.base import Handler
from app.models.auth import User
from app.models.course import Course, CourseApplication, CourseType, CourseInstructor
from app.models.instructor import Instructor
from app.models.partner import Partner
from app.utils.csrf import get_csrf
from app.utils.decorators import admin_required
from app.utils.other import convert_markdown_to_html, convert_prices_data, convert_partners_data, convert_tags_to_list, \
    convert_tags_to_string, logga


class AdminCourseListHandler(Handler):
    @admin_required
    def get(self):
        courses = Course.query(Course.deleted == False).order(Course.start_date).fetch()
        past_courses = []
        current_courses = []
        future_courses = []
        for course in courses:
            if course.start_date >= datetime.date.today():
                future_courses.append(course)
            elif course.start_date < datetime.date.today() and course.end_date >= datetime.date.today():
                current_courses.append(course)
            else:
                past_courses.append(course)
        params = {"future_courses": future_courses, "past_courses": past_courses, "current_courses": current_courses}
        self.render_template("admin/course_list.html", params)


class AdminCourseDetailsHandler(Handler):
    @admin_required
    def get(self, course_id):
        course = Course.get_by_id(int(course_id))
        applications = CourseApplication.query(CourseApplication.course_id == int(course_id), CourseApplication.deleted == False).order(-CourseApplication.created).fetch()

        num_paid = 0
        num_no_laptop = 0
        total_paid = 0.0
        for application in applications:
            if application.payment_status:
                num_paid += 1
                total_paid += application.price
            if application.laptop == "no":
                num_no_laptop += 1

        tags = convert_tags_to_string(course.tags)

        params = {"course": course,
                  "applications": applications,
                  "num_paid": num_paid,
                  "no_laptop": num_no_laptop,
                  "total_paid": total_paid,
                  "tags": tags}
        self.render_template("admin/course_details.html", params)


class AdminCourseAddHandler(Handler):
    @admin_required
    def get(self):
        course_types = CourseType.query(CourseType.deleted == False).fetch()
        instructors = Instructor.query().fetch()
        partners = Partner.query(Partner.deleted == False).fetch()
        params = {"course_types": course_types, "instructors": instructors, "partners": partners}
        self.render_template("admin/course_add.html", params)

    @admin_required
    def post(self):
        course_type = self.request.get("course-type")
        title = self.request.get("title")
        city = self.request.get("city")
        place = self.request.get("place")
        start_date = self.request.get("start-date")
        end_date = self.request.get("end-date")
        currency = self.request.get("currency")
        summary = self.request.get("summary")
        description = self.request.get("description")
        category = self.request.get("category")
        spots = self.request.get("spots")
        instructor = self.request.get("instructor")
        partner_id = self.request.get("partner")
        image_url = self.request.get("image_url")
        prices_data_string = self.request.get("all-prices-data")
        tags = self.request.get("tags")
        level = self.request.get("level")

        if course_type and title and city and place and start_date and end_date and currency and instructor and prices_data_string:
            # convert prices data string to list of Price objects
            prices = convert_prices_data(data=prices_data_string)

            # instructors
            instructor_id, instructor_name = instructor.split("|")
            user_instructor = User.get_by_id(int(instructor_id))
            course_instructor = CourseInstructor(name=instructor_name, summary=user_instructor.summary,
                                                 photo_url=user_instructor.photo_url, user_id=int(instructor_id))

            # tags
            tags = convert_tags_to_list(tags)

            # partner
            partners = convert_partners_data(partner_id)

            # course date
            start = start_date.split("/")
            end = end_date.split("/")

            course = Course.create(title=title, course_type=int(course_type), city=city, place=place, spots=int(spots), summary=summary,
                          description=description, start_date=datetime.date(int(start[2]), int(start[0]), int(start[1])),
                          end_date=datetime.date(int(end[2]), int(end[0]), int(end[1])), prices=prices, currency=currency,
                          category=category, course_instructors=[course_instructor], image_url=image_url,
                          partners=partners, tags=tags, level=int(level))
            logga("Course %s added." % course.get_id)
            self.redirect_to("course-list")


class AdminCourseEditHandler(Handler):
    @admin_required
    def get(self, course_id):
        course_types = CourseType.query(CourseType.deleted == False).fetch()
        course = Course.get_by_id(int(course_id))
        selected_course_type = CourseType.get_by_id(course.course_type)
        instructors = Instructor.query().fetch()
        partners = Partner.query(Partner.deleted == False).fetch()

        tags = convert_tags_to_string(course.tags)

        start_date = "{0}/{1}/{2}".format(course.start_date.month, course.start_date.day, course.start_date.year)
        end_date = "{0}/{1}/{2}".format(course.end_date.month, course.end_date.day, course.end_date.year)

        params = {"course": course,
                  "course_types": course_types,
                  "selected_course_type": selected_course_type,
                  "instructors": instructors,
                  "partners": partners,
                  "tags": tags,
                  "start_date": start_date,
                  "end_date": end_date}
        self.render_template("admin/course_edit.html", params)

    @admin_required
    def post(self, course_id):
        course_type = self.request.get("course-type")
        title = self.request.get("title")
        city = self.request.get("city")
        place = self.request.get("place")
        start_date = self.request.get("start-date")
        end_date = self.request.get("end-date")
        currency = self.request.get("currency")
        summary = self.request.get("summary")
        description = self.request.get("description")
        category = self.request.get("category")
        spots = self.request.get("spots")
        instructor = self.request.get("instructor")
        image_url = self.request.get("image_url")
        prices_data_string = self.request.get("all-prices-data")
        partner_id = self.request.get("partner")
        tags = self.request.get("tags")
        closed = self.request.get("closed")
        level = self.request.get("level")

        course = Course.get_by_id(int(course_id))

        if course_type and title and city and place and start_date and end_date and currency and instructor and prices_data_string:
            # convert prices data string to list of Price objects
            prices = convert_prices_data(data=prices_data_string)

            # instructors
            instructor_id, instructor_name = instructor.split("|")
            user_instructor = User.get_by_id(int(instructor_id))
            course_instructor = CourseInstructor(name=instructor_name, summary=user_instructor.summary,
                                                 photo_url=user_instructor.photo_url, user_id=int(instructor_id))

            # tags
            tags = convert_tags_to_list(tags)

            # partner
            partners = convert_partners_data(partner_id)

            start = start_date.split("/")
            end = end_date.split("/")

            Course.update(course=course, title=title, course_type=int(course_type), city=city, place=place, spots=int(spots),
                          description=description, start_date=datetime.date(int(start[2]), int(start[0]), int(start[1])),
                          end_date=datetime.date(int(end[2]), int(end[0]), int(end[1])), prices=prices, currency=currency,
                          summary=summary, category=category, course_instructors=[course_instructor],
                          image_url=image_url, partners=partners, tags=tags, closed=bool(closed), level=int(level))
            logga("Course %s edited." % course_id)
            self.redirect_to("course-details", course_id=int(course_id))


class AdminCourseDeleteHandler(Handler):
    @admin_required
    def get(self, course_id):
        course = Course.get_by_id(int(course_id))
        params = {"course": course}
        self.render_template("admin/course_delete.html", params)

    @admin_required
    def post(self, course_id):
        course = Course.get_by_id(int(course_id))
        course.deleted = True
        course.put()
        logga("Course %s deleted." % course_id)
        self.redirect_to("course-list")


class AdminCourseExportDataHandler(Handler):
    @admin_required
    def post(self, course_id):
        applications = CourseApplication.query(CourseApplication.course_id == int(course_id),
                                               CourseApplication.deleted == False).fetch()

        self.response.headers['Content-Type'] = 'text/csv'
        self.response.headers['Content-Disposition'] = 'attachment; filename=students_%s.csv' % course_id
        writer = csv.DictWriter(self.response.out, fieldnames=["First name", "Last name", "Email", "Laptop", "Shirt",
                                                               "Price", "Paid", "Invoice", "Company", "Company title",
                                                               "Company address", "Company town", "Company ZIP",
                                                               "Company tax number"])
        writer.writeheader()

        for app in applications:
            student = User.get_by_id(int(app.student_id))
            if app.company_invoice:
                writer.writerow({"First name": student.first_name.encode('utf-8'),
                                 "Last name": student.last_name.encode('utf-8'),
                                 "Email": student.email.encode('utf-8'),
                                 "Laptop": app.laptop, "Shirt": app.shirt, "Price": app.price,
                                 "Paid": app.payment_status, "Invoice": app.invoice, "Company": app.company_invoice,
                                 "Company title": app.company_title.encode('utf-8'),
                                 "Company address": app.company_address.encode('utf-8'),
                                 "Company town": app.company_town.encode('utf-8'),
                                 "Company ZIP": app.company_zip, "Company tax number": app.company_tax_number})
            else:
                writer.writerow({"First name": student.first_name.encode('utf-8'),
                                 "Last name": student.last_name.encode('utf-8'),
                                 "Email": student.email.encode('utf-8'),
                                 "Laptop": app.laptop, "Shirt": app.shirt, "Price": app.price, "Paid": app.payment_status,
                                 "Invoice": app.invoice, "Company": app.company_invoice})


# PUBLIC

class PublicCourseListHandler(Handler):
    def get(self):
        course_list = Course.query(Course.deleted == False, Course.start_date >= datetime.datetime.now()).order(Course.start_date).fetch()

        # replace .0 price with ,00 (european system vs US)
        courses = []
        for course in course_list:
            try:
                course.price_min = str(course.price[0]).replace(".", ",0")
            except:
                course.price_min = course.prices[0].price_comma

            tags_string = ""
            for tag in course.tags:
                tags_string += tag + ","

            course.tags_string = tags_string[:-1]

            courses.append(course)

        # get all the tags from courses
        tags = []
        for course in courses:
            tags += course.tags

        tags = list(set(tags))

        params = {"courses": courses, "tags": tags}
        self.render_template("public/course_list.html", params=params)


class PublicCourseDetailsHandler(Handler):
    def get(self, course_id):
        course = Course.get_by_id(int(course_id))
        if course.deleted:
            return self.redirect_to("404")

        try:
            instructor = User.get_by_id(course.instructor)
        except Exception, e:
            instructor = None

        course.description = convert_markdown_to_html(course.description)

        courses = Course.query(Course.deleted == False, Course.start_date > datetime.datetime.now()).order(Course.start_date).fetch()

        # CSRF
        csrf = get_csrf()

        params = {"course": course, "instructor": instructor, "courses": courses, "csrf": csrf}
        return self.render_template("public/course_details.html", params=params)