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
    AdminBlogEditHandler, AdminBlogDeleteHandler, PublicBlogDetailsHandler
from app.handlers.contact import PublicContactUsHandler, PublicContactThankYou
from app.handlers.courses import AdminCourseListHandler, AdminCourseDetailsHandler, AdminCourseTypesListHandler, \
    AdminCourseTypeDetailsHandler, AdminCourseAddHandler, AdminCourseTypeAddHandler, AdminCourseEditHandler, \
    AdminCourseDeleteHandler, AdminCourseTypeEditHandler, AdminCourseTypeDeleteHandler, PublicCourseListHandler, \
    PublicCourseDetailsHandler
from app.handlers.newsletter import NewsletterSubscribeHandler
from app.handlers.partners import AdminPartnersListHandler, AdminPartnerAddHandler, AdminPartnerDetailsHandler, \
    AdminPartnerDeleteHandler, AdminPartnerEditHandler, PublicPartnersHandler, AdminPartnerUserCourseList, \
    AdminPartnerUserCourseAdd, AdminPartnerUserCourseDelete, PartnerCourseListHandler
from app.handlers.public import MainHandler, \
    PublicAboutHandler, PublicComingSoonHandler, PublicApplyThankYouHandler, PublicNewsletterThankYouHandler, \
    PublicNewsletterThankYou2Handler, PublicFaqHandler
from app.handlers.users import AdminUsersListHandler, AdminUserDetailsHandler, AdminUserDeleteHandler, \
    AdminUserEditHandler


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

    # course types
    webapp2.Route('/admin/course/types', AdminCourseTypesListHandler, name="course-types-list"),
    webapp2.Route('/admin/course/type/<course_type_id:\d+>', AdminCourseTypeDetailsHandler, name="course-type-details"),
    webapp2.Route('/admin/course/type/<course_type_id:\d+>/edit', AdminCourseTypeEditHandler, name="course-type-edit"),
    webapp2.Route('/admin/course/type/<course_type_id:\d+>/delete', AdminCourseTypeDeleteHandler, name="course-type-delete"),
    webapp2.Route('/admin/course/type/add', AdminCourseTypeAddHandler, name="course-type-add"),

    # users
    webapp2.Route('/admin/users', AdminUsersListHandler, name="users-list"),
    webapp2.Route('/admin/user/<user_id:\d+>', AdminUserDetailsHandler, name="user-details"),
    webapp2.Route('/admin/user/<user_id:\d+>/delete', AdminUserDeleteHandler, name="user-delete"),
    webapp2.Route('/admin/user/<user_id:\d+>/edit', AdminUserEditHandler, name="user-edit"),

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

    # blog
    webapp2.Route('/admin/blog', AdminBlogListHandler, name="admin-blog-list"),
    webapp2.Route('/admin/blog/add', AdminBlogAddHandler, name="admin-blog-add"),
    webapp2.Route('/admin/blog/<post_id:\d+>', AdminBlogDetailsHandler, name="admin-blog-details"),
    webapp2.Route('/admin/blog/<post_id:\d+>/edit', AdminBlogEditHandler, name="admin-blog-edit"),
    webapp2.Route('/admin/blog/<post_id:\d+>/delete', AdminBlogDeleteHandler, name="admin-blog-delete"),

    # PARTNER URLS
    webapp2.Route('/partner', PartnerCourseListHandler, name="partner"),
    webapp2.Route('/partner/courses', PartnerCourseListHandler, name="partner-course-list"),

    # OTHER
    webapp2.Route('/forbidden', ForbiddenHandler, name="forbidden"),
    webapp2.Route('/404', NotExistHandler, name="404"),
    webapp2.Route('/oops', OopsHandler, name="oops"),
    webapp2.Route('/secured', SecuredSiteHandler, name="secured"),
    webapp2.Route('/login', LoginHandler, name="login"),
    webapp2.Route('/logout', LogoutHandler, name="logout"),
], debug=True)
