# INSTRUCTOR
import datetime
from google.appengine.api import users
from app.handlers.base import Handler
from app.models.auth import User
from app.models.course import CourseType, Course
from app.models.manager import Manager
from app.models.report import Report
from app.utils.decorators import instructor_required, admin_required, manager_required
from app.utils.other import logga


# ADMIN
class AdminReportsListHandler(Handler):
    @admin_required
    def get(self):
        courses = Course.query(Course.deleted == False,
                               Course.end_date >= datetime.date.today()).order(Course.end_date).fetch()

        params = {"current_courses": courses}
        return self.render_template("admin/reports.html", params=params)


class AdminReportsPastListHandler(Handler):
    @admin_required
    def get(self):
        courses = Course.query(Course.deleted == False,
                               Course.end_date < datetime.date.today()).order(Course.end_date).fetch()

        params = {"past_courses": courses}
        return self.render_template("admin/reports_past_list.html", params=params)


class AdminCourseReportsHandler(Handler):
    @admin_required
    def get(self, course_id):
        course = Course.get_by_id(int(course_id))
        reports = Report.query(Report.course_id == int(course_id), Report.deleted == False).order(-Report.lesson_date).fetch()
        params = {"course": course, "reports": reports}
        return self.render_template("admin/reports_for_course.html", params=params)


class AdminReportDetailsHandler(Handler):
    @admin_required
    def get(self, report_id):
        report = Report.get_by_id(int(report_id))
        course = Course.get_by_id(report.course_id)
        params = {"report": report, "course": course}
        return self.render_template("admin/report_details.html", params)


# MANAGER
class ManagerReportsListHandler(Handler):
    @manager_required
    def get(self):
        current_user = users.get_current_user()
        manager = Manager.query(Manager.email == str(current_user.email()).lower()).get()

        courses = Course.query(Course.deleted == False,
                               Course.franchise_id == manager.franchise_id,
                               Course.end_date >= datetime.date.today()).order(Course.end_date).fetch()

        params = {"current_courses": courses}
        return self.render_template("manager/reports.html", params=params)


class ManagerReportsPastListHandler(Handler):
    @manager_required
    def get(self):
        current_user = users.get_current_user()
        manager = Manager.query(Manager.email == str(current_user.email()).lower()).get()

        courses = Course.query(Course.deleted == False,
                               Course.franchise_id == manager.franchise_id,
                               Course.end_date < datetime.date.today()).order(Course.end_date).fetch()

        params = {"past_courses": courses}
        return self.render_template("manager/reports_past_list.html", params=params)


class ManagerCourseReportsHandler(Handler):
    @manager_required
    def get(self, course_id):
        course = Course.get_by_id(int(course_id))
        reports = Report.query(Report.course_id == int(course_id), Report.deleted == False).order(-Report.lesson_date).fetch()
        params = {"course": course, "reports": reports}
        return self.render_template("manager/reports_for_course.html", params=params)


class ManagerReportDetailsHandler(Handler):
    @manager_required
    def get(self, report_id):
        report = Report.get_by_id(int(report_id))
        course = Course.get_by_id(report.course_id)
        params = {"report": report, "course": course}
        return self.render_template("manager/report_details.html", params)


# INSTRUCTOR
class InstructorReportAddHandler(Handler):
    @instructor_required
    def get(self, course_id):
        course = Course.get_by_id(int(course_id))
        params = {"course": course}
        return self.render_template("instructor/report_add.html", params=params)

    @instructor_required
    def post(self, course_id):
        date = self.request.get("date")
        text = self.request.get("text")

        if date and text:
            user = users.get_current_user()
            author = User.get_by_email(email=user.email().lower())
            course = Course.get_by_id(int(course_id))

            lesson_date = date.split("/")

            report = Report.create(lesson_date=datetime.date(int(lesson_date[2]), int(lesson_date[0]),
                                                             int(lesson_date[1])),
                                   course=course, author=author, text=text)
            logga("Report %s added." % report.get_id)
            return self.redirect_to("instructor-course-details", course_id=course.get_id)


class InstructorReportDetailsHandler(Handler):
    @instructor_required
    def get(self, report_id):
        report = Report.get_by_id(int(report_id))
        author = User.get_by_email(users.get_current_user().email().lower())
        course = Course.get_by_id(report.course_id)
        params = {"report": report, "course": course, "author": author}
        return self.render_template("instructor/report_details.html", params)


class InstructorReportEditHandler(Handler):
    @instructor_required
    def get(self, report_id):
        report = Report.get_by_id(int(report_id))
        params = {"report": report}
        return self.render_template("instructor/report_edit.html", params)

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
            return self.redirect_to("instructor-report-details", report_id=int(report_id))
        else:
            return self.redirect_to("oops")


class InstructorReportDeleteHandler(Handler):
    @instructor_required
    def get(self, report_id):
        report = Report.get_by_id(int(report_id))
        params = {"report": report}
        return self.render_template("instructor/report_delete.html", params)

    @instructor_required
    def post(self, report_id):
        report = Report.get_by_id(int(report_id))
        course_id = report.course_id
        report.deleted = True
        report.put()
        logga("Report %s deleted." % report_id)
        return self.redirect_to("instructor-course-details", course_id=course_id)