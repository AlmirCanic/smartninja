# ADMIN
import datetime
from google.appengine.api import users
from app.handlers.base import Handler
from app.models.auth import User
from app.models.course import Course, CourseApplication, CourseType
from app.models.franchise import Franchise, FranchiseList
from app.models.instructor import Instructor
from app.models.job_application import JobApplication
from app.models.manager import Manager
from app.models.report import Report
from app.utils.decorators import admin_required, instructor_required, manager_required
from app.utils.other import logga


# ADMIN
class AdminInstructorsListHandler(Handler):
    @admin_required
    def get(self):
        instructors = Instructor.query(Instructor.deleted == False).fetch()

        active_instructors = []
        inactive_instructors = []

        for instructor in instructors:
            if instructor.active:
                active_instructors.append(instructor)
            else:
                inactive_instructors.append(instructor)

        params = {"active_instructors": active_instructors, "inactive_instructors": inactive_instructors}
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

        user = User.get_or_short_create(email=email, first_name=first_name, last_name=last_name)

        instructor = Instructor.add_or_create(full_name=user.get_full_name, user_id=user.get_id, email=user.email,
                                              franchises=[franchise_list_item])

        logga("Instructor %s added to franchise %s." % (instructor.get_id, franchise.get_id))

        return self.redirect_to("admin-instructors-list")


class AdminInstructorEditHandler(Handler):
    @admin_required
    def get(self, instructor_id):
        instructor = Instructor.get_by_id(int(instructor_id))
        instructor_user = User.get_by_id(int(instructor.user_id))
        params = {"instructor": instructor, "i_user": instructor_user}
        return self.render_template("admin/instructor_edit.html", params)

    @admin_required
    def post(self, instructor_id):
        email = self.request.get("email")
        city = self.request.get("city")
        phone = self.request.get("phone")
        address = self.request.get("address")
        github = self.request.get("github")
        linkedin = self.request.get("linkedin")
        homepage = self.request.get("homepage")
        dob = self.request.get("dob")

        # update instructor
        instructor = Instructor.get_by_id(int(instructor_id))
        Instructor.update(instructor=instructor, email=email, city=city)

        # update user (that belongs to instructor)
        user = User.get_by_id(int(instructor.user_id))
        user.phone_number = phone
        user.address = address
        user.github_url = github
        user.linkedin_url = linkedin
        user.homepage_url = homepage
        user.dob = dob
        user.put()

        logga("Instructor %s and user %s edited." % (instructor.get_id, user.get_id))

        return self.redirect_to("admin-instructor-details", instructor_id=instructor_id)


class AdminInstructorDeleteHandler(Handler):
    @admin_required
    def get(self, instructor_id):
        instructor = Instructor.get_by_id(int(instructor_id))
        params = {"instructor": instructor}
        return self.render_template("admin/instructor_delete.html", params)

    @admin_required
    def post(self, instructor_id):
        instructor = Instructor.get_by_id(int(instructor_id))
        instructor.deleted = True
        instructor.put()
        logga("Instructor %s removed." % instructor_id)
        return self.redirect_to("admin-instructors-list")


class AdminInstructorDetailsHandler(Handler):
    @admin_required
    def get(self, instructor_id):
        instructor = Instructor.get_by_id(int(instructor_id))
        instructor_user = User.get_by_id(int(instructor.user_id))
        job_applications = JobApplication.query(JobApplication.instructor_id == int(instructor_id)).fetch()
        params = {"instructor": instructor, "i_user": instructor_user, "applications": job_applications}
        return self.render_template("admin/instructor_details.html", params)


class AdminInstructorAddAccessCurriculumHandler(Handler):
    @admin_required
    def get(self, instructor_id):
        instructor = Instructor.get_by_id(int(instructor_id))
        curriculums = CourseType.query().fetch()
        params = {"instructor": instructor, "curriculums": curriculums}
        return self.render_template("admin/instructor_add_access_curriculum.html", params)

    @admin_required
    def post(self, instructor_id):
        instructor = Instructor.get_by_id(int(instructor_id))

        curriculum_id = self.request.get("curriculum")

        if curriculum_id:
            curriculum = CourseType.get_by_id(int(curriculum_id))
            Instructor.add_curriculum(instructor=instructor, curriculum_id=int(curriculum_id), curriculum_title=curriculum.title)
            return self.redirect_to("admin-instructor-details", instructor_id=instructor_id)
        else:
            return self.redirect_to("oops")


class AdminInstructorRemoveAccessCurriculumHandler(Handler):
    @admin_required
    def get(self, instructor_id, curriculum_id):
        instructor = Instructor.get_by_id(int(instructor_id))
        curriculum = CourseType.get_by_id(int(curriculum_id))
        params = {"instructor": instructor, "curriculum": curriculum}
        return self.render_template("admin/instructor_remove_access_curriculum.html", params)

    @admin_required
    def post(self, instructor_id, curriculum_id):
        instructor = Instructor.get_by_id(int(instructor_id))
        Instructor.remove_curriculum(instructor=instructor, curriculum_id=int(curriculum_id))
        return self.redirect_to("admin-instructor-details", instructor_id=instructor_id)


class AdminInstructorDeActivateHandler(Handler):
    @admin_required
    def post(self, instructor_id):
        instructor = Instructor.get_by_id(int(instructor_id))

        if instructor.active:
            instructor.active = False
        else:
            instructor.active = True

        instructor.put()

        return self.redirect_to("admin-instructor-details", instructor_id=instructor_id)


class AdminInstructorGradeHandler(Handler):
    @admin_required
    def post(self, instructor_id):
        instructor = Instructor.get_by_id(int(instructor_id))

        score = self.request.get("score")
        notes = self.request.get("notes")

        Instructor.grade(instructor=instructor, score=score, notes=notes)

        return self.redirect_to("admin-instructor-details", instructor_id=instructor_id)


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

        user = User.get_or_short_create(email=email, first_name=first_name, last_name=last_name)

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
            instructor.deleted = True
            instructor.put()
            logga("Instructor %s removed." % instructor_id)
        elif manager_franchise and other_franchises:
            existing_franchises = instructor.franchises
            existing_franchises.remove(manager_franchise[0])
            instructor.franchises = existing_franchises
            instructor.put()

        return self.redirect_to("manager-instructors-list")