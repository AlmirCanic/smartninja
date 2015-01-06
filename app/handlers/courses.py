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