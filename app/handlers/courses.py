import datetime
from app.handlers.base import Handler
from app.models.auth import User
from app.models.course import Course, CourseApplication, CourseType
from app.utils.decorators import admin_required


class AdminCourseListHandler(Handler):
    @admin_required
    def get(self):
        courses = Course.query(Course.deleted == False).fetch()
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

        course_price = str(course.price).replace("[", "").replace("]", "")

        params = {"course": course,
                  "applications": applications,
                  "num_paid": num_paid,
                  "no_laptop": num_no_laptop,
                  "total_paid": total_paid,
                  "course_price": course_price}
        self.render_template("admin/course_details.html", params)


class AdminCourseAddHandler(Handler):
    @admin_required
    def get(self):
        course_types = CourseType.query().fetch()
        instructors = User.query(User.instructor == True).fetch()
        params = {"course_types": course_types, "instructors": instructors}
        self.render_template("admin/course_add.html", params)

    @admin_required
    def post(self):
        course_type = self.request.get("course-type")
        title = self.request.get("title")
        city = self.request.get("city")
        place = self.request.get("place")
        start_date = self.request.get("start-date")
        end_date = self.request.get("end-date")
        price = self.request.get("price")
        currency = self.request.get("currency")
        summary = self.request.get("summary")
        description = self.request.get("description")
        category = self.request.get("category")
        spots = self.request.get("spots")
        instructor = self.request.get("instructor")

        try:
            instructor = int(instructor)
        except Exception, e:
            instructor = None

        if course_type and title and city and place and start_date and end_date and price and currency:
            prices = [float(prc) for prc in price.strip().split(",")]
            start = start_date.split("-")
            end = end_date.split("-")

            Course.create(title=title, course_type=int(course_type), city=city, place=place, spots=int(spots), summary=summary,
                          description=description, start_date=datetime.date(int(start[0]), int(start[1]), int(start[2])),
                          end_date=datetime.date(int(end[0]), int(end[1]), int(end[2])), price=prices, currency=currency,
                          category=category, instructor=instructor)
            self.redirect_to("course-list")


class AdminCourseEditHandler(Handler):
    @admin_required
    def get(self, course_id):
        course_types = CourseType.query().fetch()
        course = Course.get_by_id(int(course_id))
        selected_course_type = CourseType.get_by_id(course.course_type)
        course_price = str(course.price).replace("[", "").replace("]", "")
        params = {"course": course,
                  "course_types": course_types,
                  "course_price": course_price,
                  "selected_course_type": selected_course_type}
        self.render_template("admin/course_edit.html", params)

    @admin_required
    def post(self, course_id):
        course_type = self.request.get("course-type")
        title = self.request.get("title")
        city = self.request.get("city")
        place = self.request.get("place")
        start_date = self.request.get("start-date")
        end_date = self.request.get("end-date")
        price = self.request.get("price")
        currency = self.request.get("currency")
        summary = self.request.get("summary")
        description = self.request.get("description")
        category = self.request.get("category")
        spots = self.request.get("spots")
        instructor = self.request.get("instructor")

        course = Course.get_by_id(int(course_id))

        try:
            instructor = int(instructor)
        except Exception, e:
            instructor = None

        if course_type and title and city and place and start_date and end_date and price and currency:
            prices = [float(prc) for prc in price.strip().split(",")]
            start = start_date.split("-")
            end = end_date.split("-")

            Course.update(course=course, title=title, course_type=int(course_type), city=city, place=place, spots=int(spots),
                          description=description, start_date=datetime.date(int(start[0]), int(start[1]), int(start[2])),
                          end_date=datetime.date(int(end[0]), int(end[1]), int(end[2])), price=prices, currency=currency,
                           summary=summary, category=category, instructor=instructor)
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
        course_list = Course.query(Course.deleted == False).fetch()

        courses = []
        for course in course_list:
            course.price_min = str(course.price[0]).replace(".", ",0")
            courses.append(course)

        params = {"courses": courses}
        self.render_template("public/course_list.html", params=params)


class PublicCourseDetailsHandler(Handler):
    def get(self, course_id):
        course = Course.get_by_id(int(course_id))
        if course.deleted:
            self.redirect_to("404")
        params = {"course": course}
        self.render_template("public/course_details.html", params=params)