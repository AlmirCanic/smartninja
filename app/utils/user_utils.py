from app.models.instructor import Instructor
from app.models.partner import PartnerUserCourse
from app.models.course import CourseApplication
from app.models.student import StudentCourse
from app.utils.other import logga


def change_name(user, first_name, last_name):
    if user.first_name != first_name or user.last_name != last_name:
        user.first_name = first_name
        user.last_name = last_name
        applications = CourseApplication.query(CourseApplication.student_id == user.get_id).fetch()

        for application in applications:
            application.student_name = "%s %s" % (first_name, last_name)
            application.put()

        pucs = PartnerUserCourse.query(PartnerUserCourse.user_id == user.get_id).fetch()

        for puc in pucs:
            puc.user_name = user.first_name + " " + user.last_name
            puc.put()


def change_email(user, email, new_id=None):
    user.email = email
    user.put()

    applications = CourseApplication.query(CourseApplication.student_id == user.get_id).fetch()

    for application in applications:
        application.student_email = email
        if new_id:
            application.student_id = new_id
        application.put()

    pucs = PartnerUserCourse.query(PartnerUserCourse.user_id == user.get_id).fetch()

    for puc in pucs:
        puc.user_email = email
        if new_id:
            puc.user_id = new_id
        puc.put()

    instructors = Instructor.query(Instructor.user_id == user.get_id).fetch()

    for instructor in instructors:
        instructor.email = email
        if new_id:
            instructor.user_id = new_id
        instructor.put()

    student_courses = StudentCourse.query(StudentCourse.user_id == user.get_id).fetch()

    for stc in student_courses:
        stc.user_email = email
        if new_id:
            stc.user_id = new_id
        stc.put()

    logga("User %s email changed." % user.get_id)