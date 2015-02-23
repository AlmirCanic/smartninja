#!/usr/bin/env python
#
# Copyright 2015 SmartNinja
#

import webapp2
from app.handlers.apply import AdminCourseApplicationDetailsHandler, \
    AdminCourseApplicationDeleteHandler, PublicCourseApplicationAddHandler
from app.handlers.auth import LoginHandler, LogoutHandler, ForbiddenHandler, ProfileHandler, NotExistHandler, \
    OopsHandler
from app.handlers.base import SecuredSiteHandler, AdminHandler
from app.handlers.blog import PublicBlogHandler, AdminBlogListHandler, AdminBlogAddHandler, AdminBlogDetailsHandler, \
    AdminBlogEditHandler, AdminBlogDeleteHandler, PublicBlogDetailsHandler, InstructorBlogListHandler, \
    InstructorBlogAddHandler, InstructorBlogDetailsHandler, InstructorBlogEditHandler, InstructorBlogDeleteHandler
from app.handlers.contact import PublicContactUsHandler, PublicContactThankYou
from app.handlers.courses import AdminCourseListHandler, AdminCourseDetailsHandler, \
    AdminCourseAddHandler, AdminCourseEditHandler, \
    AdminCourseDeleteHandler, PublicCourseListHandler, \
    PublicCourseDetailsHandler
from app.handlers.curriculums import AdminCourseTypesListHandler, AdminCourseTypeDetailsHandler, \
    AdminCourseTypeEditHandler, AdminCourseTypeDeleteHandler, AdminCourseTypeAddHandler, \
    InstructorCurriculumsListHandler, InstructorCurriculumDetailsHandler, InstructorCurriculumEditHandler, \
    InstructorCurriculumAddHandler
from app.handlers.instructors import AdminInstructorsListHandler, AdminInstructorAddHandler, AdminInstructorDeleteHandler, \
    InstructorCourseListHandler, InstructorCourseDetailsHandler, InstructorProfileDetailsHandler, InstructorProfileEditHandler
from app.handlers.lessons import AdminLessonAddHandler, AdminLessonDetailsHandler, AdminLessonEditHandler, AdminLessonDeleteHandler, \
    InstructorLessonAddHandler, InstructorLessonDetailsHandler, InstructorLessonEditHandler, \
    InstructorLessonDeleteHandler, StudentLessonDetailsHandler
from app.handlers.newsletter import NewsletterSubscribeHandler
from app.handlers.partners import AdminPartnersListHandler, AdminPartnerAddHandler, AdminPartnerDetailsHandler, \
    AdminPartnerDeleteHandler, AdminPartnerEditHandler, PublicPartnersHandler, AdminPartnerUserCourseList, \
    AdminPartnerUserCourseAdd, AdminPartnerUserCourseDelete, PartnerCourseListHandler, PartnerCourseDetailsHandler, \
    PartnerProfileDetailsHandler, PartnerProfileEditHandler
from app.handlers.public import MainHandler, \
    PublicAboutHandler, PublicComingSoonHandler, PublicApplyThankYouHandler, PublicNewsletterThankYouHandler, \
    PublicNewsletterThankYou2Handler, PublicFaqHandler, PublicCareersHandler
from app.handlers.reports import InstructorReportAddHandler
from app.handlers.students import AdminStudentCourseList, AdminStudentCourseAdd, AdminStudentCourseDelete, \
    StudentCourseListHandler, StudentCourseDetailsHandler, StudentProfileDetailsHandler, StudentProfileEditHandler
from app.handlers.users import AdminUsersListHandler, AdminUserDetailsHandler, AdminUserDeleteHandler, \
    AdminUserEditHandler, AdminUsersAllListHandler


app = webapp2.WSGIApplication([
    # PUBLIC
    webapp2.Route('/', MainHandler, name="main"),
    webapp2.Route('/newsletter', NewsletterSubscribeHandler, name="newsletter"),
    webapp2.Route('/partners', PublicPartnersHandler, name="partners"),
    webapp2.Route('/about', PublicAboutHandler, name="about"),
    webapp2.Route('/faq', PublicFaqHandler, name="faq"),
    webapp2.Route('/coming-soon', PublicComingSoonHandler, name="coming-soon"),
    webapp2.Route('/apply_thank_you', PublicApplyThankYouHandler, name="apply-thank-you"),
    webapp2.Route('/email_thank_you', PublicNewsletterThankYouHandler, name="newsletter-thank-you-1"),
    webapp2.Route('/email_thank_you_2', PublicNewsletterThankYou2Handler, name="newsletter-thank-you-2"),
    webapp2.Route('/contact-thank-you', PublicContactThankYou, name="public-contact-thanks"),
    webapp2.Route('/contact', PublicContactUsHandler, name="public-contact"),
    webapp2.Route('/careers', PublicCareersHandler, name="public-contact"),

    # blog
    webapp2.Route('/blog', PublicBlogHandler, name="blog"),
    webapp2.Route('/blog/<post_slug:.+>', PublicBlogDetailsHandler, name="blog-details"),

    # course
    webapp2.Route('/courses', PublicCourseListHandler, name="public-courses"),
    webapp2.Route('/course/<course_id:\d+>', PublicCourseDetailsHandler, name="public-course-details"),
    webapp2.Route('/course/<course_id:\d+>/apply', PublicCourseApplicationAddHandler, name="public-application-add"),


    # ADMIN URLS
    # basic
    webapp2.Route('/admin', AdminHandler, name="admin"),
    webapp2.Route('/admin/profile', ProfileHandler, name='profile'),

    # courses
    webapp2.Route('/admin/courses', AdminCourseListHandler, name="course-list"),
    webapp2.Route('/admin/course/<course_id:\d+>', AdminCourseDetailsHandler, name="course-details"),
    webapp2.Route('/admin/course/<course_id:\d+>/edit', AdminCourseEditHandler, name="course-edit"),
    webapp2.Route('/admin/course/<course_id:\d+>/delete', AdminCourseDeleteHandler, name="course-delete"),
    webapp2.Route('/admin/course/add', AdminCourseAddHandler, name="course-add"),

    # course applications
    webapp2.Route('/admin/application/<application_id:\d+>', AdminCourseApplicationDetailsHandler, name="application-details"),
    webapp2.Route('/admin/application/<application_id:\d+>/delete', AdminCourseApplicationDeleteHandler, name="application-delete"),

    # course types/curriculums
    webapp2.Route('/admin/course/types', AdminCourseTypesListHandler, name="course-types-list"),
    webapp2.Route('/admin/course/type/<course_type_id:\d+>', AdminCourseTypeDetailsHandler, name="course-type-details"),
    webapp2.Route('/admin/course/type/<course_type_id:\d+>/edit', AdminCourseTypeEditHandler, name="course-type-edit"),
    webapp2.Route('/admin/course/type/<course_type_id:\d+>/delete', AdminCourseTypeDeleteHandler, name="course-type-delete"),
    webapp2.Route('/admin/course/type/add', AdminCourseTypeAddHandler, name="course-type-add"),

    # lessons
    webapp2.Route('/admin/course/type/<course_type_id:\d+>/add-lesson', AdminLessonAddHandler, name="admin-lesson-add"),
    webapp2.Route('/admin/lesson/<lesson_id:\d+>', AdminLessonDetailsHandler, name="admin-lesson-details"),
    webapp2.Route('/admin/lesson/<lesson_id:\d+>/edit', AdminLessonEditHandler, name="admin-lesson-edit"),
    webapp2.Route('/admin/lesson/<lesson_id:\d+>/delete', AdminLessonDeleteHandler, name="admin-lesson-delete"),

    # users
    webapp2.Route('/admin/users', AdminUsersListHandler, name="users-list"),
    webapp2.Route('/admin/users/all', AdminUsersAllListHandler, name="users-all-list"),
    webapp2.Route('/admin/user/<user_id:\d+>', AdminUserDetailsHandler, name="user-details"),
    webapp2.Route('/admin/user/<user_id:\d+>/delete', AdminUserDeleteHandler, name="user-delete"),
    webapp2.Route('/admin/user/<user_id:\d+>/edit', AdminUserEditHandler, name="user-edit"),

    # instructors
    webapp2.Route('/admin/users/instructors', AdminInstructorsListHandler, name="admin-instructors-list"),
    webapp2.Route('/admin/users/instructor/add', AdminInstructorAddHandler, name="admin-instructor-add"),
    webapp2.Route('/admin/users/instructor/<instructor_id:\d+>/delete', AdminInstructorDeleteHandler, name="admin-instructor-delete"),

    # partners
    webapp2.Route('/admin/partners', AdminPartnersListHandler, name="admin-partners-list"),
    webapp2.Route('/admin/partner/add', AdminPartnerAddHandler, name="admin-partner-add"),
    webapp2.Route('/admin/partner/<partner_id:\d+>', AdminPartnerDetailsHandler, name="admin-partner-details"),
    webapp2.Route('/admin/partner/<partner_id:\d+>/delete', AdminPartnerDeleteHandler, name="admin-partner-delete"),
    webapp2.Route('/admin/partner/<partner_id:\d+>/edit', AdminPartnerEditHandler, name="admin-partner-edit"),

    # partner user course
    webapp2.Route('/admin/partner-courses', AdminPartnerUserCourseList, name="admin-partner-user-course-list"),
    webapp2.Route('/admin/partner-course/add', AdminPartnerUserCourseAdd, name="admin-partner-user-course-add"),
    webapp2.Route('/admin/partner-course/<puc_id:\d+>/delete', AdminPartnerUserCourseDelete, name="admin-partner-user-course-delete"),

    # student access to courses
    webapp2.Route('/admin/users/students', AdminStudentCourseList, name="admin-student-course-list"),
    webapp2.Route('/admin/users/students/add', AdminStudentCourseAdd, name="admin-student-course-add"),
    webapp2.Route('/admin/users/students/<student_id:\d+>/delete', AdminStudentCourseDelete, name="admin-student-course-delete"),

    # blog
    webapp2.Route('/admin/blog', AdminBlogListHandler, name="admin-blog-list"),
    webapp2.Route('/admin/blog/add', AdminBlogAddHandler, name="admin-blog-add"),
    webapp2.Route('/admin/blog/<post_id:\d+>', AdminBlogDetailsHandler, name="admin-blog-details"),
    webapp2.Route('/admin/blog/<post_id:\d+>/edit', AdminBlogEditHandler, name="admin-blog-edit"),
    webapp2.Route('/admin/blog/<post_id:\d+>/delete', AdminBlogDeleteHandler, name="admin-blog-delete"),

    # PARTNER URLS
    webapp2.Route('/partner', PartnerCourseListHandler, name="partner"),
    webapp2.Route('/partner/profile', PartnerProfileDetailsHandler, name="partner-profile"),
    webapp2.Route('/partner/profile/edit', PartnerProfileEditHandler, name="partner-profile-edit"),
    webapp2.Route('/partner/courses', PartnerCourseListHandler, name="partner-course-list"),
    webapp2.Route('/partner/course/<course_id:\d+>', PartnerCourseDetailsHandler, name="partner-course-details"),

    # INSTRUCTOR URLS
    webapp2.Route('/instructor', InstructorCourseListHandler, name="instructor"),
    webapp2.Route('/instructor/courses', InstructorCourseListHandler, name="instructor-course-list"),
    webapp2.Route('/instructor/course/<course_id:\d+>', InstructorCourseDetailsHandler, name="instructor-course-details"),

    webapp2.Route('/instructor/profile', InstructorProfileDetailsHandler, name="instructor-profile"),
    webapp2.Route('/instructor/profile/edit', InstructorProfileEditHandler, name="instructor-profile-edit"),

    # instructor blog
    webapp2.Route('/instructor/blog', InstructorBlogListHandler, name="instructor-blog-list"),
    webapp2.Route('/instructor/blog/add', InstructorBlogAddHandler, name="instructor-blog-add"),
    webapp2.Route('/instructor/blog/<post_id:\d+>', InstructorBlogDetailsHandler, name="instructor-blog-details"),
    webapp2.Route('/instructor/blog/<post_id:\d+>/edit', InstructorBlogEditHandler, name="instructor-blog-edit"),
    webapp2.Route('/instructor/blog/<post_id:\d+>/delete', InstructorBlogDeleteHandler, name="instructor-blog-delete"),

    # instructor course types/curriculums
    webapp2.Route('/instructor/curriculums', InstructorCurriculumsListHandler, name="instructor-curriculum-list"),
    webapp2.Route('/instructor/curriculum/<course_type_id:\d+>', InstructorCurriculumDetailsHandler, name="instructor-curriculum-details"),
    webapp2.Route('/instructor/curriculum/<course_type_id:\d+>/edit', InstructorCurriculumEditHandler, name="instructor-curriculum-edit"),
    webapp2.Route('/instructor/curriculum/add', InstructorCurriculumAddHandler, name="instructor-curriculum-add"),

    # instructor lessons
    webapp2.Route('/instructor/curriculum/<course_type_id:\d+>/add-lesson', InstructorLessonAddHandler, name="instructor-lesson-add"),
    webapp2.Route('/instructor/lesson/<lesson_id:\d+>', InstructorLessonDetailsHandler, name="instructor-lesson-details"),
    webapp2.Route('/instructor/lesson/<lesson_id:\d+>/edit', InstructorLessonEditHandler, name="instructor-lesson-edit"),
    webapp2.Route('/instructor/lesson/<lesson_id:\d+>/delete', InstructorLessonDeleteHandler, name="instructor-lesson-delete"),

    # instructor reports
    webapp2.Route('/instructor/course/<course_id:\d+>/add-report', InstructorReportAddHandler, name="instructor-report-add"),

    # STUDENT URLS
    webapp2.Route('/student', StudentCourseListHandler, name="student"),
    webapp2.Route('/student/course/<course_id:\d+>', StudentCourseDetailsHandler, name="student-course-details"),
    webapp2.Route('/student/course/<course_id:\d+>/lesson/<lesson_id:\d+>', StudentLessonDetailsHandler, name="student-lesson-details"),
    webapp2.Route('/student/profile', StudentProfileDetailsHandler, name="student-profile"),
    webapp2.Route('/student/profile/edit', StudentProfileEditHandler, name="student-profile-edit"),

    # OTHER
    webapp2.Route('/forbidden', ForbiddenHandler, name="forbidden"),
    webapp2.Route('/404', NotExistHandler, name="404"),
    webapp2.Route('/oops', OopsHandler, name="oops"),
    webapp2.Route('/secured', SecuredSiteHandler, name="secured"),
    webapp2.Route('/login', LoginHandler, name="login"),
    webapp2.Route('/logout', LogoutHandler, name="logout"),
], debug=True)
