import datetime
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from app.handlers.base import Handler
from app.models.auth import User
from app.models.contact_candidate import ContactCandidate
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.student import StudentCourse
from app.utils.decorators import admin_required, student_required
from app.utils.other import logga


class AdminStudentCourseList(Handler):
    @admin_required
    def get(self):
        courses = Course.query(Course.deleted == False).order(Course.start_date).fetch()
        params = {"courses": courses}
        self.render_template("admin/student_course_list.html", params)


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

        return self.redirect_to("admin-student-course-list")


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

        params = {"profile": profile, "upload_url": upload_url}
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

        if not profile:
            return self.redirect_to("forbidden")
        else:
            params = {"profile": profile}
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
            User.update(user=profile, first_name=first_name, last_name=last_name, address=address, phone_number=phone_number,
                    summary=summary, photo_url=photo_url, dob=dob, github=github_url, job_searching=bool(job_searching),
                    current_town=current_town, linkedin=linkedin_url, homepage=homepage_url)
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