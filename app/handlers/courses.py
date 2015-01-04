from app.handlers.base import Handler
from app.models.course import Course, CourseApplication
from app.utils.decorators import admin_required


class CourseListHandler(Handler):
    @admin_required
    def get(self):
        courses = Course.query().fetch()
        params = {"courses": courses}
        self.render_template("admin/course_list.html", params)


class CourseDetailsHandler(Handler):
    @admin_required
    def get(self, course_id):
        course = Course.get_by_id(int(course_id))
        applications = CourseApplication.query(CourseApplication.course_id == int(course_id)).fetch()
        params = {"course": course, "applications": applications}
        self.render_template("admin/course_details.html", params)