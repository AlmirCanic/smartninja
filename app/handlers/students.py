import datetime
from app.handlers.base import Handler
from app.models.auth import User
from app.models.course import Course
from app.models.student import StudentCourse
from app.utils.decorators import admin_required
from app.utils.other import logga


class AdminStudentCourseList(Handler):
    @admin_required
    def get(self):
        students = StudentCourse.query().fetch()
        params = {"students": students}
        self.render_template("admin/student_course_list.html", params)


class AdminStudentCourseAdd(Handler):
    @admin_required
    def get(self):
        courses = Course.query(Course.deleted == False, Course.start_date > datetime.datetime.now()).order(Course.start_date).fetch()
        params = {"courses": courses}
        self.render_template("admin/student_course_add.html", params)

    @admin_required
    def post(self):
        email = self.request.get("email")
        first_name = self.request.get("first-name")
        last_name = self.request.get("last-name")
        course_id = self.request.get("course")

        user = User.get_by_email(email=email)

        if not user:
            user = User.short_create(email=email, first_name=first_name, last_name=last_name)

        course = Course.get_by_id(int(course_id))

        student = StudentCourse.create(user_id=user.get_id, user_name=user.get_full_name, user_email=email, course=course)
        logga("StudentCourse %s added." % student.get_id)

        return self.redirect_to("admin-student-course-list")


class AdminStudentCourseDelete(Handler):
    @admin_required
    def get(self, student_id):
        student = StudentCourse.get_by_id(int(student_id))
        params = {"student": student}
        self.render_template("admin/student_course_delete.html", params)
    @admin_required
    def post(self, student_id):
        student = StudentCourse.get_by_id(int(student_id))
        student.key.delete()  # delete directly from the database, because not that important
        logga("StudentCourse %s deleted." % student_id)
        self.redirect_to("admin-student-course-list")