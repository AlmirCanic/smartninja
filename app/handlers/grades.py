from google.appengine.api import users
from app.handlers.base import Handler
from app.models.auth import User
from app.models.course import CourseApplication, Course
from app.utils.decorators import instructor_required, admin_required
from app.utils.other import logga, convert_tags_to_string, convert_tags_to_list


# ADMIN
class AdminGradesListHandler(Handler):
    @admin_required
    def get(self):
        courses = Course.query(Course.deleted == False).order(Course.end_date).fetch()

        params = {"courses": courses}
        self.render_template("admin/grades.html", params=params)


class AdminCourseGradesHandler(Handler):
    @admin_required
    def get(self, course_id):
        course = Course.get_by_id(int(course_id))
        applications = CourseApplication.query(CourseApplication.course_id == int(course_id), CourseApplication.deleted == False).order(-CourseApplication.created).fetch()

        params = {"course": course, "applications": applications}
        self.render_template("admin/grades_for_course.html", params=params)


class AdminGradeStudentDetailsHandler(Handler):
    @admin_required
    def get(self, application_id):
        application = CourseApplication.get_by_id(int(application_id))

        tags = convert_tags_to_string(application.grade_tags)

        params = {"application": application, "tags": tags}
        self.render_template("admin/grade_details.html", params)


# INSTRUCTOR
class InstructorGradeStudentDetailsHandler(Handler):
    @instructor_required
    def get(self, application_id):
        current_user = users.get_current_user()
        user = User.query(User.email == str(current_user.email()).lower()).get()

        application = CourseApplication.get_by_id(int(application_id))
        course = Course.get_by_id(application.course_id)

        tags = convert_tags_to_string(application.grade_tags)

        course_instructors = []
        for instructor in course.course_instructors:
            course_instructors.append(instructor.user_id)

        if user.get_id in course_instructors:
            params = {"application": application, "tags": tags}
            self.render_template("instructor/grade_details.html", params)
        else:
            return self.redirect_to("forbidden")


class InstructorGradeStudentEditHandler(Handler):
    @instructor_required
    def get(self, application_id):
        current_user = users.get_current_user()
        user = User.query(User.email == str(current_user.email()).lower()).get()

        application = CourseApplication.get_by_id(int(application_id))
        course = Course.get_by_id(application.course_id)

        tags = convert_tags_to_string(application.grade_tags)

        course_instructors = []
        for instructor in course.course_instructors:
            course_instructors.append(instructor.user_id)

        if user.get_id in course_instructors:
            params = {"application": application, "tags": tags}
            self.render_template("instructor/grade_edit.html", params)
        else:
            return self.redirect_to("forbidden")

    @instructor_required
    def post(self, application_id):
        current_user = users.get_current_user()
        user = User.query(User.email == str(current_user.email()).lower()).get()

        application = CourseApplication.get_by_id(int(application_id))
        course = Course.get_by_id(application.course_id)

        course_instructors = []
        for instructor in course.course_instructors:
            course_instructors.append(instructor.user_id)

        if user.get_id in course_instructors:
            score = self.request.get("score")
            tags = self.request.get("all-tags")
            summary = self.request.get("summary")
            top_dev = self.request.get("top-dev")

            tags = convert_tags_to_list(tags)

            CourseApplication.grade_student(application=application, score=int(score), summary=summary, tags=list(tags),
                                            top_student=bool(top_dev))
            logga("User %s edited student application %s grade." % (user.get_id, application.get_id))
            self.redirect_to("instructor-grade-student", application_id=application_id)
        else:
            return self.redirect_to("forbidden")