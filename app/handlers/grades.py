from google.appengine.api import users
from app.handlers.base import Handler
from app.models.auth import User
from app.models.course import CourseApplication, Course
from app.utils.decorators import instructor_required
from app.utils.other import logga, convert_tags_to_string, convert_tags_to_list


class InstructorGradeStudentDetailsHandler(Handler):
    @instructor_required
    def get(self, application_id):
        current_user = users.get_current_user()
        user = User.query(User.email == str(current_user.email())).get()

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
        user = User.query(User.email == str(current_user.email())).get()

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
        user = User.query(User.email == str(current_user.email())).get()

        application = CourseApplication.get_by_id(int(application_id))
        course = Course.get_by_id(application.course_id)

        course_instructors = []
        for instructor in course.course_instructors:
            course_instructors.append(instructor.user_id)

        if user.get_id in course_instructors:
            score = self.request.get("score")
            tags = self.request.get("all-tags")
            summary = self.request.get("summary")

            tags = convert_tags_to_list(tags)

            CourseApplication.grade_student(application=application, score=int(score), summary=summary, tags=list(tags))
            logga("User %s edited student application %s grade." % (user.get_id, application.get_id))
            self.redirect_to("instructor-grade-student", application_id=application_id)
        else:
            return self.redirect_to("forbidden")