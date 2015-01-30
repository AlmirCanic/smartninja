import datetime
from app.handlers.base import Handler
from app.models.auth import User
from app.models.course import Course, CourseApplication, CourseType, Price, CourseInstructor
from app.models.partner import Partner
from app.utils.csrf import get_csrf
from app.utils.decorators import admin_required
from app.utils.other import convert_markdown_to_html, convert_prices_data, convert_partners_data


class AdminCourseListHandler(Handler):
    @admin_required
    def get(self):
        courses = Course.query(Course.deleted == False).order(Course.start_date).fetch()
        params = {"courses": courses}
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

        params = {"course": course,
                  "applications": applications,
                  "num_paid": num_paid,
                  "no_laptop": num_no_laptop,
                  "total_paid": total_paid}
        self.render_template("admin/course_details.html", params)


class AdminCourseAddHandler(Handler):
    @admin_required
    def get(self):
        course_types = CourseType.query(CourseType.deleted == False).fetch()
        instructors = User.query(User.instructor == True).fetch()
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

        if course_type and title and city and place and start_date and end_date and currency and instructor and prices_data_string:
            # convert prices data string to list of Price objects
            prices = convert_prices_data(data=prices_data_string)

            # instructors
            instructor_id, instructor_name = instructor.split("|")
            user_instructor = User.get_by_id(int(instructor_id))
            course_instructor = CourseInstructor(name=instructor_name, summary=user_instructor.summary,
                                                 photo_url=user_instructor.photo_url, user_id=int(instructor_id))

            # partner
            partners = convert_partners_data(partner_id)

            # course date
            start = start_date.split("-")
            end = end_date.split("-")

            Course.create(title=title, course_type=int(course_type), city=city, place=place, spots=int(spots), summary=summary,
                          description=description, start_date=datetime.date(int(start[0]), int(start[1]), int(start[2])),
                          end_date=datetime.date(int(end[0]), int(end[1]), int(end[2])), prices=prices, currency=currency,
                          category=category, course_instructors=[course_instructor], image_url=image_url,
                          partners=partners)
            self.redirect_to("course-list")


class AdminCourseEditHandler(Handler):
    @admin_required
    def get(self, course_id):
        course_types = CourseType.query(CourseType.deleted == False).fetch()
        course = Course.get_by_id(int(course_id))
        selected_course_type = CourseType.get_by_id(course.course_type)
        instructors = User.query(User.instructor == True).fetch()
        partners = Partner.query(Partner.deleted == False).fetch()
        params = {"course": course,
                  "course_types": course_types,
                  "selected_course_type": selected_course_type,
                  "instructors": instructors,
                  "partners": partners}
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

        course = Course.get_by_id(int(course_id))

        if course_type and title and city and place and start_date and end_date and currency and instructor and prices_data_string:
            # convert prices data string to list of Price objects
            prices = convert_prices_data(data=prices_data_string)

            # instructors
            instructor_id, instructor_name = instructor.split("|")
            user_instructor = User.get_by_id(int(instructor_id))
            course_instructor = CourseInstructor(name=instructor_name, summary=user_instructor.summary,
                                                 photo_url=user_instructor.photo_url, user_id=int(instructor_id))

            # partner
            partners = convert_partners_data(partner_id)

            start = start_date.split("-")
            end = end_date.split("-")

            Course.update(course=course, title=title, course_type=int(course_type), city=city, place=place, spots=int(spots),
                          description=description, start_date=datetime.date(int(start[0]), int(start[1]), int(start[2])),
                          end_date=datetime.date(int(end[0]), int(end[1]), int(end[2])), prices=prices, currency=currency,
                          summary=summary, category=category, course_instructors=[course_instructor],
                          image_url=image_url, partners=partners)
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
        self.redirect_to("course-list")


class AdminCourseTypesListHandler(Handler):
    @admin_required
    def get(self):
        course_types = CourseType.query(CourseType.deleted == False).fetch()
        params = {"course_types": course_types}
        self.render_template("admin/course_types_list.html", params)


class AdminCourseTypeDetailsHandler(Handler):
    @admin_required
    def get(self, course_type_id):
        course_type = CourseType.get_by_id(int(course_type_id))
        params = {"course_type": course_type}
        self.render_template("admin/course_type_details.html", params)


class AdminCourseTypeAddHandler(Handler):
    @admin_required
    def get(self):
        self.render_template("admin/course_type_add.html")

    @admin_required
    def post(self):
        title = self.request.get("title")
        curriculum = self.request.get("curriculum")
        description = self.request.get("description")

        if title and curriculum:
            CourseType.create(title=title, curriculum=curriculum, description=description)
            self.redirect_to("course-types-list")


class AdminCourseTypeEditHandler(Handler):
    @admin_required
    def get(self, course_type_id):
        course_type = CourseType.get_by_id(int(course_type_id))
        params = {"course_type": course_type}
        self.render_template("admin/course_type_edit.html", params)

    @admin_required
    def post(self, course_type_id):
        course_type = CourseType.get_by_id(int(course_type_id))
        course_type.title = self.request.get("title")
        course_type.curriculum = self.request.get("curriculum")
        course_type.description = self.request.get("description")
        course_type.put()
        self.redirect_to("course-type-details", course_type_id=int(course_type_id))


class AdminCourseTypeDeleteHandler(Handler):
    @admin_required
    def get(self, course_type_id):
        course_type = CourseType.get_by_id(int(course_type_id))
        params = {"course_type": course_type}
        self.render_template("admin/course_type_delete.html", params)

    @admin_required
    def post(self, course_type_id):
        course_type = CourseType.get_by_id(int(course_type_id))
        course_type.deleted = True
        course_type.put()
        self.redirect_to("course-types-list")


# PUBLIC

class PublicCourseListHandler(Handler):
    def get(self):
        course_list = Course.query(Course.deleted == False, Course.start_date > datetime.datetime.now()).order(Course.start_date).fetch()

        courses = []
        for course in course_list:
            try:
                course.price_min = str(course.price[0]).replace(".", ",0")
            except:
                course.price_min = course.prices[0].price_comma
            courses.append(course)

        params = {"courses": courses}
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

        courses = Course.query(Course.deleted == False).fetch()

        # CSRF
        csrf = get_csrf()

        params = {"course": course, "instructor": instructor, "courses": courses, "csrf": csrf}
        return self.render_template("public/course_details.html", params=params)