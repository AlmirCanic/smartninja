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


def change_email(user, email, new_user=None):
    user.email = email
    user.put()

    applications = CourseApplication.query(CourseApplication.student_id == user.get_id).fetch()

    for application in applications:
        application.student_email = email
        if new_user:
            application.student_id = new_user.get_id
            application.student_name = new_user.get_full_name
        application.put()

    pucs = PartnerUserCourse.query(PartnerUserCourse.user_id == user.get_id).fetch()

    for puc in pucs:
        puc.user_email = email
        if new_user:
            puc.user_id = new_user.get_id
            puc.user_name = new_user.get_full_name
        puc.put()

    instructors = Instructor.query(Instructor.user_id == user.get_id).fetch()
    instructor_counter = 0

    for instructor in instructors:
        if instructor_counter > 0:
            instructor.key.delete()
        else:
            instructor.email = email
            if new_user:
                instructor.full_name = new_user.get_full_name
                instructor.user_id = new_user.get_id
            instructor.put()
            instructor_counter += 1

    student_courses = StudentCourse.query(StudentCourse.user_id == user.get_id).fetch()

    for stc in student_courses:
        stc.user_email = email
        if new_user:
            stc.user_id = new_user.get_id
            stc.user_name = new_user.get_full_name
        stc.put()

    logga("User %s email changed." % user.get_id)