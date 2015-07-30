# ADMIN
import datetime
from google.appengine.api import users
from app.handlers.base import Handler
from app.models.auth import User
from app.models.course import Course, CourseApplication
from app.models.franchise import Franchise, FranchiseList
from app.models.instructor import Instructor
from app.models.manager import Manager
from app.models.report import Report
from app.utils.decorators import admin_required, instructor_required, manager_required
from app.utils.other import logga


# ADMIN
class AdminInstructorsListHandler(Handler):
    @admin_required
    def get(self):
        instructors = Instructor.query().fetch()
        params = {"instructors": instructors}
        return self.render_template("admin/instructor_list.html", params)


class AdminInstructorAddHandler(Handler):
    @admin_required
    def get(self):
        franchises = Franchise.query(Franchise.deleted == False).fetch()
        params = {"franchises": franchises}
        return self.render_template("admin/instructor_add.html", params)

    @admin_required
    def post(self):
        email = self.request.get("email")
        first_name = self.request.get("first-name")
        last_name = self.request.get("last-name")
        franchise_id = self.request.get("franchise")

        franchise = Franchise.get_by_id(int(franchise_id))

        franchise_list_item = FranchiseList(franchise_id=franchise.get_id, franchise_title=franchise.title)

        user = User.get_by_email(email=email)

        if not user:
            user = User.short_create(email=email, first_name=first_name, last_name=last_name)

        instructor = Instructor.add_or_create(full_name=user.get_full_name, user_id=user.get_id, email=user.email,
                                              franchises=[franchise_list_item])

        logga("Instructor %s added to franchise %s." % (instructor.get_id, franchise.get_id))

        return self.redirect_to("admin-instructors-list")


class AdminInstructorDeleteHandler(Handler):
    @admin_required
    def get(self, instructor_id):
        instructor = Instructor.get_by_id(int(instructor_id))
        params = {"instructor": instructor}
        return self.render_template("admin/instructor_delete.html", params)
    @admin_required
    def post(self, instructor_id):
        instructor = Instructor.get_by_id(int(instructor_id))
        instructor.key.delete()
        logga("Instructor %s removed." % instructor_id)
        return self.redirect_to("admin-instructors-list")


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
            return self.render_template("instructor/course_list.html", params)


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
            reports = Report.query(Report.course_id == int(course_id), Report.deleted == False).order(-Report.lesson_date).fetch()

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
        return self.render_template("instructor/profile.html", params)


class InstructorProfileEditHandler(Handler):
    @instructor_required
    def get(self):
        current_user = users.get_current_user()
        profile = User.query(User.email == str(current_user.email()).lower()).get()

        if not profile:
            return self.redirect_to("forbidden")
        else:
            params = {"profile": profile}
            return self.render_template("instructor/profile_edit.html", params)

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
            description = self.request.get("long-description")

            user = User.update(user=profile, first_name=first_name, last_name=last_name, address=address,
                               phone_number=phone_number, summary=summary, photo_url=photo_url, dob=dob,
                               long_description=description)

            logga("User %s edited." % user.get_id)
            return self.redirect_to("instructor-profile")


# MANAGER
class ManagerInstructorsListHandler(Handler):
    @manager_required
    def get(self):
        curr_user = users.get_current_user()
        manager = Manager.query(Manager.email == curr_user.email().lower()).get()

        instructors = Instructor.query(Instructor.franchises.franchise_id == manager.franchise_id).fetch()

        params = {"instructors": instructors}
        return self.render_template("manager/instructor_list.html", params)


class ManagerInstructorAddHandler(Handler):
    @manager_required
    def get(self):
        return self.render_template("manager/instructor_add.html")

    @manager_required
    def post(self):
        email = self.request.get("email")
        first_name = self.request.get("first-name")
        last_name = self.request.get("last-name")

        curr_user = users.get_current_user()
        manager = Manager.query(Manager.email == curr_user.email().lower()).get()

        franchise = Franchise.get_by_id(manager.franchise_id)

        franchise_list_item = FranchiseList(franchise_id=franchise.get_id, franchise_title=franchise.title)

        user = User.get_by_email(email=email)

        if not user:
            user = User.short_create(email=email, first_name=first_name, last_name=last_name)

        instructor = Instructor.add_or_create(full_name=user.get_full_name, user_id=user.get_id, email=user.email,
                                              franchises=[franchise_list_item])

        logga("Instructor %s added to franchise %s." % (instructor.get_id, franchise.get_id))

        return self.redirect_to("manager-instructors-list")


class ManagerInstructorDeleteHandler(Handler):
    @manager_required
    def get(self, instructor_id):
        instructor = Instructor.get_by_id(int(instructor_id))

        params = {"instructor": instructor}
        return self.render_template("manager/instructor_delete.html", params)

    @manager_required
    def post(self, instructor_id):
        instructor = Instructor.get_by_id(int(instructor_id))

        curr_user = users.get_current_user()
        manager = Manager.query(Manager.email == curr_user.email().lower()).get()

        manager_franchise = []
        other_franchises = []

        for instructor_franchise in instructor.franchises:
            if manager.franchise_id != instructor_franchise.franchise_id:
                other_franchises.append(instructor_franchise)
            else:
                manager_franchise.append(instructor_franchise)

        if not other_franchises:
            instructor.key.delete()
            logga("Instructor %s removed." % instructor_id)
        elif manager_franchise and other_franchises:
            existing_franchises = instructor.franchises
            existing_franchises.remove(manager_franchise[0])
            instructor.franchises = existing_franchises
            instructor.put()

        return self.redirect_to("manager-instructors-list")