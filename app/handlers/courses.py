import datetime
from app.handlers.base import Handler
from app.models.course import Course, CourseApplication, CourseType
from app.utils.decorators import admin_required


class AdminCourseListHandler(Handler):
    @admin_required
    def get(self):
        courses = Course.query().fetch()
        params = {"courses": courses}
        self.render_template("admin/course_list.html", params)


class AdminCourseDetailsHandler(Handler):
    @admin_required
    def get(self, course_id):
        course = Course.get_by_id(int(course_id))
        applications = CourseApplication.query(CourseApplication.course_id == int(course_id)).fetch()
        params = {"course": course, "applications": applications}
        self.render_template("admin/course_details.html", params)


class AdminCourseAddHandler(Handler):
    @admin_required
    def get(self):
        course_types = CourseType.query().fetch()
        params = {"course_types": course_types}
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
        description = self.request.get("description")

        if course_type and title and city and place and start_date and end_date and price and currency:
            prices = [float(prc) for prc in price.strip().split(",")]
            start = start_date.split("-")
            end = end_date.split("-")

            Course.create(title=title, course_type=int(course_type), city=city, place=place, description=description,
                          start_date=datetime.date(int(start[0]), int(start[1]), int(start[2])),
                          end_date=datetime.date(int(end[0]), int(end[1]), int(end[2])), price=prices, currency=currency)
            self.redirect_to("course-list")


class AdminCourseTypesListHandler(Handler):
    @admin_required
    def get(self):
        course_types = CourseType.query().fetch()
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