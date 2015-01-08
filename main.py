#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from app.handlers.apply import TempPrijavaHandler
from app.handlers.auth import LoginHandler, LogoutHandler, ForbiddenHandler, ProfileHandler
from app.handlers.base import MainHandler, SecuredSiteHandler, AdminHandler, TempMainHandler
from app.handlers.courses import AdminCourseListHandler, AdminCourseDetailsHandler, AdminCourseTypesListHandler, \
    AdminCourseTypeDetailsHandler, AdminCourseAddHandler, AdminCourseTypeAddHandler, AdminCourseEditHandler
from app.handlers.users import AdminUsersListHandler, AdminUserDetailsHandler, AdminUserDeleteHandler, \
    AdminUserEditHandler


app = webapp2.WSGIApplication([
    # PUBLIC
    webapp2.Route('/main', MainHandler, name="main"),
    webapp2.Route('/', TempMainHandler, name="temp"),
    webapp2.Route('/prijava', TempPrijavaHandler, name="prijava"),

    # ADMIN URLS
    # basic
    webapp2.Route('/admin', AdminHandler, name="admin"),
    webapp2.Route('/login', LoginHandler, name="login"),
    webapp2.Route('/logout', LogoutHandler, name="logout"),
    webapp2.Route('/admin/profile', ProfileHandler, name='profile'),

    # courses
    webapp2.Route('/admin/courses', AdminCourseListHandler, name="course-list"),
    webapp2.Route('/admin/course/<course_id:\d+>', AdminCourseDetailsHandler, name="course-details"),
    webapp2.Route('/admin/course/<course_id:\d+>/edit', AdminCourseEditHandler, name="course-edit"),
    webapp2.Route('/admin/course/add', AdminCourseAddHandler, name="course-add"),

    # course types
    webapp2.Route('/admin/course/types', AdminCourseTypesListHandler, name="course-types-list"),
    webapp2.Route('/admin/course/type/<course_type_id:\d+>', AdminCourseTypeDetailsHandler, name="course-type-details"),
    webapp2.Route('/admin/course/type/add', AdminCourseTypeAddHandler, name="course-type-add"),

    #users
    webapp2.Route('/admin/users', AdminUsersListHandler, name="users-list"),
    webapp2.Route('/admin/user/<user_id:\d+>', AdminUserDetailsHandler, name="user-details"),
    webapp2.Route('/admin/user/<user_id:\d+>/delete', AdminUserDeleteHandler, name="user-delete"),
    webapp2.Route('/admin/user/<user_id:\d+>/edit', AdminUserEditHandler, name="user-edit"),

    # other
    webapp2.Route('/forbidden', ForbiddenHandler, name="forbidden"),
    webapp2.Route('/secured', SecuredSiteHandler, name="secured"),
], debug=True)
