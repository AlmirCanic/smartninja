from app.models.partner import PartnerUserCourse
from app.models.course import CourseApplication


def change_name_or_email(user, first_name, last_name, email):
    if user.first_name != first_name or user.last_name != last_name or user.email != email:
        user.first_name = first_name
        user.last_name = last_name
        applications = CourseApplication.query(CourseApplication.student_id == user.get_id).fetch()

        for application in applications:
            application.student_name = "%s %s" % (first_name, last_name)
            if email != None:
                application.student_email = email
            application.put()

        pucs = PartnerUserCourse.query(PartnerUserCourse.user_id == user.get_id).fetch()

        for puc in pucs:
            puc.user_name = user.first_name + " " + user.last_name
            puc.put()