# INSTRUCTOR
import datetime
from google.appengine.api import users
from app.handlers.base import Handler
from app.models.auth import User
from app.models.course import CourseType, Course
from app.models.report import Report
from app.utils.decorators import instructor_required, admin_required
from app.utils.other import logga


# ADMIN
class AdminReportsListHandler(Handler):
    @admin_required
    def get(self):
        courses = Course.query(Course.deleted == False).order(Course.end_date).fetch()
        past_courses = []
        current_courses = []
        for course in courses:
            if course.end_date > datetime.date.today():
                current_courses.append(course)
            else:
                past_courses.append(course)
        params = {"current_courses": current_courses, "past_courses": past_courses}
        self.render_template("admin/reports.html", params=params)


class AdminCourseReportsHandler(Handler):
    @admin_required
    def get(self, course_id):
        course = Course.get_by_id(int(course_id))
        reports = Report.query(Report.course_id == int(course_id), Report.deleted == False).fetch()
        params = {"course": course, "reports": reports}
        self.render_template("admin/reports_for_course.html", params=params)


class AdminReportDetailsHandler(Handler):
    @admin_required
    def get(self, report_id):
        report = Report.get_by_id(int(report_id))
        course = Course.get_by_id(report.course_id)
        params = {"report": report, "course": course}
        self.render_template("admin/report_details.html", params)


# INSTRUCTOR
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


class InstructorReportDeleteHandler(Handler):
    @instructor_required
    def get(self, report_id):
        report = Report.get_by_id(int(report_id))
        params = {"report": report}
        self.render_template("instructor/report_delete.html", params)

    @instructor_required
    def post(self, report_id):
        report = Report.get_by_id(int(report_id))
        course_id = report.course_id
        report.deleted = True
        report.put()
        logga("Report %s deleted." % report_id)
        self.redirect_to("instructor-course-details", course_id=course_id)