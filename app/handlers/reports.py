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
            self.redirect_to("instructor-course-details", course_id=course.get_id)


class InstructorReportDetailsHandler(Handler):
    @instructor_required
    def get(self, report_id):
        report = Report.get_by_id(int(report_id))
        author = User.get_by_email(users.get_current_user().email())
        course = Course.get_by_id(report.course_id)
        params = {"report": report, "course": course, "author": author}
        self.render_template("instructor/report_details.html", params)


class InstructorReportEditHandler(Handler):
    @instructor_required
    def get(self, report_id):
        report = Report.get_by_id(int(report_id))
        params = {"report": report}
        self.render_template("instructor/report_edit.html", params)

    @instructor_required
    def post(self, report_id):
        text = self.request.get("text")
        date = self.request.get("date")

        if date and text:
            report = Report.get_by_id(int(report_id))
            lesson_date = date.split("/")
            Report.update(report=report, lesson_date=datetime.date(int(lesson_date[2]), int(lesson_date[0]),
                                                                   int(lesson_date[1])),
                          text=text)
            logga("Report %s updated." % report_id)
            self.redirect_to("instructor-report-details", report_id=int(report_id))
        else:
            self.redirect_to("oops")

"""
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