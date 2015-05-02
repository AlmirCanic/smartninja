# ADMIN
import datetime
from google.appengine.api import users
from app.handlers.base import Handler
from app.models.auth import User
from app.models.course import Course, CourseApplication
from app.models.instructor import Instructor
from app.models.report import Report
from app.utils.decorators import admin_required, instructor_required
from app.utils.other import logga


class AdminInstructorsListHandler(Handler):
    @admin_required
    def get(self):
        instructors = Instructor.query().fetch()
        params = {"instructors": instructors}
        self.render_template("admin/instructor_list.html", params)


class AdminInstructorAddHandler(Handler):
    @admin_required
    def get(self):
        self.render_template("admin/instructor_add.html")

    @admin_required
    def post(self):
        email = self.request.get("email")
        first_name = self.request.get("first-name")
        last_name = self.request.get("last-name")

        user = User.get_by_email(email=email)

        if not user:
            user = User.short_create(email=email, first_name=first_name, last_name=last_name)

        instructor = Instructor.create(full_name=user.get_full_name, email=email, user_id=user.get_id)
        logga("Instructor %s added." % instructor.get_id)

        return self.redirect_to("admin-instructors-list")


class AdminInstructorDeleteHandler(Handler):
    @admin_required
    def get(self, instructor_id):
        instructor = Instructor.get_by_id(int(instructor_id))
        params = {"instructor": instructor}
        self.render_template("admin/instructor_delete.html", params)
    @admin_required
    def post(self, instructor_id):
        instructor = Instructor.get_by_id(int(instructor_id))
        instructor.key.delete()
        logga("Instructor %s removed." % instructor_id)
        self.redirect_to("admin-instructors-list")


# INSTRUCTOR

class InstructorCourseListHandler(Handler):
    @instructor_required
    def get(self):
        current_user = users.get_current_user()
        user = User.query(User.email == str(current_user.email()).lower()).get()
        if not user:
            return self.redirect_to("forbidden")
        else:
            courses = Course.query(Course.course_instructors.user_id == user.get_id, Course.deleted == False).fetch()

            past_courses = []
            future_courses = []
            for course in courses:
                if course.start_date > datetime.date.today():
                    future_courses.append(course)
                else:
                    past_courses.append(course)
            params = {"future_courses": future_courses, "past_courses": past_courses}
            self.render_template("instructor/course_list.html", params)


class InstructorCourseDetailsHandler(Handler):
    @instructor_required
    def get(self, course_id):
        current_user = users.get_current_user()
        user = User.query(User.email == str(current_user.email()).lower()).get()
        if not user:
            return self.redirect_to("forbidden")
        else:
            course = Course.get_by_id(int(course_id))
            courses = Course.query(Course.course_instructors.user_id == user.get_id, Course.deleted == False).fetch()
            reports = Report.query(Report.course_id == int(course_id), Report.deleted == False).fetch()

            if course in courses:
                applications = CourseApplication.query(CourseApplication.course_id == int(course_id),
                                                       CourseApplication.deleted == False).order(-CourseApplication.created).fetch()

                num_no_laptop = 0
                for application in applications:
                    if application.laptop == "no":
                        num_no_laptop += 1

                params = {"course": course,
                          "reports": reports,
                          "applications": applications,
                          "no_laptop": num_no_laptop}
                return self.render_template("instructor/course_details.html", params)
            else:
                return self.redirect_to("forbidden")


class InstructorProfileDetailsHandler(Handler):
    @instructor_required
    def get(self):
        current_user = users.get_current_user()
        profile = User.query(User.email == str(current_user.email()).lower()).get()

        if not profile:
            return self.redirect_to("forbidden")

        params = {"profile": profile}
        self.render_template("instructor/profile.html", params)


class InstructorProfileEditHandler(Handler):
    @instructor_required
    def get(self):
        current_user = users.get_current_user()
        profile = User.query(User.email == str(current_user.email()).lower()).get()

        if not profile:
            return self.redirect_to("forbidden")
        else:
            params = {"profile": profile}
            self.render_template("instructor/profile_edit.html", params)

    @instructor_required
    def post(self):
        current_user = users.get_current_user()
        profile = User.query(User.email == str(current_user.email()).lower()).get()

        if not profile:
            return self.redirect_to("forbidden")
        else:
            first_name = self.request.get("first_name")
            last_name = self.request.get("last_name")
            address = self.request.get("address")
            summary = self.request.get("summary")
            photo_url = self.request.get("photo_url")
            phone_number = self.request.get("phone_number")
            dob = self.request.get("dob")
            user = User.update(user=profile, first_name=first_name, last_name=last_name, address=address, phone_number=phone_number,
                    summary=summary, photo_url=photo_url, dob=dob)
            logga("User %s edited." % user.get_id)
            self.redirect_to("instructor-profile")