# INSTRUCTOR
import datetime
from google.appengine.api import users
from app.handlers.base import Handler
from app.models.auth import User
from app.models.course import CourseType, Course
from app.models.report import Report
from app.utils.decorators import instructor_required
from app.utils.other import logga


class InstructorReportAddHandler(Handler):
    @instructor_required
    def get(self, course_id):
        course = Course.get_by_id(int(course_id))
        params = {"course": course}
        self.render_template("instructor/report_add.html", params=params)

    @instructor_required
    def post(self, course_id):
        date = self.request.get("date")
        text = self.request.get("text")

        if date and text:
            user = users.get_current_user()
            author = User.get_by_email(email=user.email())
            course = Course.get_by_id(int(course_id))

            lesson_date = date.split("/")

            report = Report.create(lesson_date=datetime.date(int(lesson_date[2]), int(lesson_date[0]),
                                                             int(lesson_date[1])),
                                   course=course, author=author, text=text)
            logga("Report %s added." % report.get_id)
            #self.redirect_to("instructor-report-details", report_id=report.get_id)
            self.redirect_to("instructor-course-details", course_id=course.get_id)


"""
class InstructorReportDetailsHandler(Handler):
    @instructor_required
    def get(self, lesson_id):
        lesson = Report.get_by_id(int(lesson_id))
        course_type = CourseType.get_by_id(lesson.course_type)
        lesson.text = convert_markdown_to_html(lesson.text)
        params = {"lesson": lesson, "course_type": course_type}
        self.render_template("instructor/lesson_details.html", params)


class InstructorReportEditHandler(Handler):
    @instructor_required
    def get(self, lesson_id):
        lesson = Report.get_by_id(int(lesson_id))
        course_type = CourseType.get_by_id(lesson.course_type)
        params = {"course_type": course_type, "lesson": lesson}
        self.render_template("instructor/lesson_edit.html", params)

    @instructor_required
    def post(self, lesson_id):
        title = self.request.get("title")
        order = self.request.get("order")
        text = self.request.get("text")

        if title and text:
            lesson = Report.get_by_id(int(lesson_id))
            course_type = CourseType.get_by_id(lesson.course_type)
            Report.update(lesson=lesson, title=title, order=int(order), text=text, course_type=course_type.get_id)
            logga("Report %s updated." % lesson_id)
            self.redirect_to("instructor-lesson-details", lesson_id=int(lesson_id))
        else:
            self.redirect_to("oops")


class InstructorReportDeleteHandler(Handler):
    @instructor_required
    def get(self, lesson_id):
        lesson = Report.get_by_id(int(lesson_id))
        course_type = CourseType.get_by_id(lesson.course_type)
        params = {"course_type": course_type, "lesson": lesson}
        self.render_template("instructor/lesson_delete.html", params)

    @instructor_required
    def post(self, lesson_id):
        lesson = Report.get_by_id(int(lesson_id))
        lesson.deleted = True
        lesson.put()
        logga("Report %s deleted." % lesson_id)
        self.redirect_to("instructor-curriculum-details", course_type_id=lesson.course_type)
        """