import datetime
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from app.handlers.base import Handler
from app.models.auth import User
from app.models.contact_candidate import ContactCandidate
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.manager import Manager
from app.models.student import StudentCourse
from app.utils.decorators import admin_required, student_required, manager_required
from app.utils.other import logga, convert_markdown_to_html, convert_tags_to_string, convert_tags_to_list


class AdminStudentCourseList(Handler):
    @admin_required
    def get(self):
        courses = Course.query(Course.deleted == False).order(Course.start_date).fetch()

        current_courses = []
        future_courses = []
        for course in courses:
            if course.start_date >= datetime.date.today():
                future_courses.append(course)
            elif course.start_date < datetime.date.today() and course.end_date >= datetime.date.today():
                current_courses.append(course)

        params = {"future_courses": future_courses, "current_courses": current_courses}

        self.render_template("admin/student_course_list.html", params)


class AdminStudentPastCoursesList(Handler):
    @admin_required
    def get(self):
        courses = Course.query(Course.deleted == False).order(-Course.start_date).fetch()

        past_courses = []

        for course in courses:
            if course.start_date < datetime.date.today():
                past_courses.append(course)

        params = {"past_courses": past_courses}

        self.render_template("admin/student_course_past_list.html", params)


class AdminStudentCourseAccessHandler(Handler):
    @admin_required
    def get(self, course_id):
        students = StudentCourse.query(StudentCourse.course_id == int(course_id)).fetch()
        course = Course.get_by_id(int(course_id))
        params = {"students": students, "course": course}
        self.render_template("admin/student_access_per_course.html", params)


class AdminStudentCourseAdd(Handler):
    @admin_required
    def get(self):
        courses = Course.query(Course.deleted == False).order(Course.start_date).fetch()
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

        return self.redirect_to("admin-student-course-access", course_id=course_id)


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


# MANAGER
class ManagerStudentCourseList(Handler):
    @manager_required
    def get(self):
        curr_user = users.get_current_user()
        manager = Manager.query(Manager.email == curr_user.email().lower()).get()

        courses = Course.query(Course.deleted == False, Course.franchise_id == manager.franchise_id).order(Course.start_date).fetch()

        current_courses = []
        future_courses = []
        for course in courses:
            if course.start_date >= datetime.date.today():
                future_courses.append(course)
            elif course.start_date < datetime.date.today() and course.end_date >= datetime.date.today():
                current_courses.append(course)

        params = {"future_courses": future_courses, "current_courses": current_courses}

        self.render_template("manager/student_course_list.html", params)


class ManagerStudentPastCoursesList(Handler):
    @manager_required
    def get(self):
        curr_user = users.get_current_user()
        manager = Manager.query(Manager.email == curr_user.email().lower()).get()

        courses = Course.query(Course.deleted == False, Course.franchise_id == manager.franchise_id).order(-Course.start_date).fetch()

        past_courses = []

        for course in courses:
            if course.start_date < datetime.date.today():
                past_courses.append(course)

        params = {"past_courses": past_courses}

        return self.render_template("manager/student_course_past_list.html", params)


class ManagerStudentCourseAccessHandler(Handler):
    @manager_required
    def get(self, course_id):
        students = StudentCourse.query(StudentCourse.course_id == int(course_id)).fetch()
        course = Course.get_by_id(int(course_id))
        params = {"students": students, "course": course}
        return self.render_template("manager/student_access_per_course.html", params)


class ManagerStudentCourseAdd(Handler):
    @manager_required
    def get(self):
        curr_user = users.get_current_user()
        manager = Manager.query(Manager.email == curr_user.email().lower()).get()

        courses = Course.query(Course.deleted == False, Course.franchise_id == manager.franchise_id).order(Course.start_date).fetch()

        params = {"courses": courses}
        return self.render_template("manager/student_course_add.html", params)

    @manager_required
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

        return self.redirect_to("manager-student-course-access", course_id=course_id)


class ManagerStudentCourseDelete(Handler):
    @manager_required
    def get(self, student_id):
        student = StudentCourse.get_by_id(int(student_id))
        params = {"student": student}
        return self.render_template("manager/student_course_delete.html", params)

    @manager_required
    def post(self, student_id):
        student = StudentCourse.get_by_id(int(student_id))

        course = Course.get_by_id(student.course_id)

        curr_user = users.get_current_user()
        manager = Manager.query(Manager.email == curr_user.email().lower()).get()

        if course.franchise_id == manager.franchise_id:
            student.key.delete()  # delete directly from the database, because not that important
            logga("StudentCourse %s deleted." % student_id)

        return self.redirect_to("manager-student-course-access", course_id=course.get_id)


# STUDENT
class StudentCourseListHandler(Handler):
    @student_required
    def get(self):
        current_user = users.get_current_user()
        user = User.query(User.email == str(current_user.email()).lower()).get()
        if not user:
            return self.redirect_to("forbidden")
        else:
            students = StudentCourse.query(StudentCourse.user_id == user.get_id).fetch()

            courses = []
            for student in students:
                course = Course.get_by_id(student.course_id)
                courses.append(course)

            past_courses = []
            future_courses = []
            for course in courses:
                if course.start_date > datetime.date.today():
                    future_courses.append(course)
                else:
                    past_courses.append(course)
            params = {"future_courses": future_courses, "past_courses": past_courses}
            self.render_template("student/course_list.html", params)


class StudentCourseDetailsHandler(Handler):
    @student_required
    def get(self, course_id):
        current_user = users.get_current_user()
        user = User.query(User.email == str(current_user.email()).lower()).get()
        if not user:
            return self.redirect_to("forbidden")
        else:
            stc = StudentCourse.query(StudentCourse.course_id == int(course_id), StudentCourse.user_id == user.get_id).get()

            if stc:
                course = Course.get_by_id(int(course_id))

                lessons = Lesson.query(Lesson.course_type == course.course_type, Lesson.deleted == False).order(Lesson.order).fetch()

                params = {"course": course,
                          "lessons": lessons}
                return self.render_template("student/course_details.html", params)
            else:
                return self.redirect_to("forbidden")


class StudentProfileDetailsHandler(Handler):
    @student_required
    def get(self):
        current_user = users.get_current_user()
        profile = User.query(User.email == str(current_user.email()).lower()).get()

        if not profile:
            return self.redirect_to("forbidden")

        upload_url = blobstore.create_upload_url(success_path='/student/profile/upload-cv',
                                                 max_bytes_per_blob=1000000, max_bytes_total=1000000)  # max 1 MB

        if profile.long_description:
            profile.long_description = convert_markdown_to_html(profile.long_description)

        all_skills = list(set(profile.grade_all_tags + profile.other_skills))

        params = {"profile": profile, "upload_url": upload_url, "all_skills": all_skills}
        self.render_template("student/profile.html", params)


class StudentCVUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    @student_required
    def post(self):
        current_user = users.get_current_user()
        profile = User.query(User.email == str(current_user.email()).lower()).get()

        try:
            upload = self.get_uploads()[0]

            profile.cv_blob = upload.key()

            profile.put()

            self.redirect_to('student-profile')

        except Exception, e:
            self.response.out.write("upload failed: %s" % e)


class StudentCVDownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
    @student_required
    def get(self, ):
        current_user = users.get_current_user()
        profile = User.query(User.email == str(current_user.email()).lower()).get()

        if not blobstore.get(profile.cv_blob):
            self.redirect_to('student-profile')
        else:
            self.send_blob(profile.cv_blob, save_as="%s.pdf" % profile.get_id)


class StudentProfileEditHandler(Handler):
    @student_required
    def get(self):
        current_user = users.get_current_user()
        profile = User.query(User.email == str(current_user.email()).lower()).get()

        courses_skills = convert_tags_to_string(profile.grade_all_tags)

        other_skills = convert_tags_to_string(profile.other_skills)

        if not profile:
            return self.redirect_to("forbidden")
        else:
            params = {"profile": profile, "other_skills": other_skills, "courses_skills": courses_skills}
            self.render_template("student/profile_edit.html", params)

    @student_required
    def post(self):
        current_user = users.get_current_user()
        profile = User.query(User.email == str(current_user.email()).lower()).get()

        if not profile:
            return self.redirect_to("forbidden")
        else:
            first_name = self.request.get("first_name")
            last_name = self.request.get("last_name")
            address = self.request.get("address")
            current_town = self.request.get("current_town")
            summary = self.request.get("summary")
            github_url = self.request.get("github_url")
            linkedin_url = self.request.get("linkedin_url")
            homepage_url = self.request.get("homepage_url")
            photo_url = self.request.get("photo_url")
            job_searching = self.request.get("searching")
            phone_number = self.request.get("phone_number")
            dob = self.request.get("dob")

            programming_year = self.request.get("programming-year")
            programming_month = self.request.get("programming-month")

            long_description = self.request.get("long-description")

            other_skills = self.request.get("skills")

            skills_list = convert_tags_to_list(other_skills)

            # add only skilly that are not already in skills from courses (grade_all_tags)
            skills_list_clean = []

            for skill in skills_list:
                if skill not in profile.grade_all_tags:
                    skills_list_clean.append(skill)

            if programming_month and programming_year:
                started_programming = datetime.date(year=int(programming_year), month=int(programming_month), day=10)
            else:
                started_programming = None

            User.update(user=profile, first_name=first_name, last_name=last_name, address=address, phone_number=phone_number,
                        summary=summary, photo_url=photo_url, dob=dob, github=github_url, job_searching=bool(job_searching),
                        current_town=current_town, linkedin=linkedin_url, homepage=homepage_url,
                        started_programming=started_programming, long_description=long_description,
                        other_skills=skills_list_clean)
            logga("Student %s profile edited." % profile.get_id)
            self.redirect_to("student-profile")


class StudentContactedByEmployersListHandler(Handler):
    @student_required
    def get(self):
        student = users.get_current_user()

        contacted_list = ContactCandidate.query(ContactCandidate.candidate_email == student.email(),
                                                ContactCandidate.deleted == False).fetch()

        params = {"contacted_list": contacted_list}

        return self.render_template("student/contacted_list.html", params)