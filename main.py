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
from app.handlers.courses import CourseListHandler, CourseDetailsHandler


app = webapp2.WSGIApplication([
    # PUBLIC
    webapp2.Route('/main', MainHandler, name="main"),
    webapp2.Route('/', TempMainHandler, name="temp"),
    webapp2.Route('/prijava', TempPrijavaHandler, name="prijava"),

    # ADMIN
    webapp2.Route('/admin', AdminHandler, name="admin"),
    webapp2.Route('/login', LoginHandler, name="login"),
    webapp2.Route('/logout', LogoutHandler, name="logout"),
    webapp2.Route('/admin/courses', CourseListHandler, name="course-list"),
    webapp2.Route('/admin/course/<course_id:\d+>', CourseDetailsHandler, name="course-details"),
    webapp2.Route('/admin/profile', ProfileHandler, name='profile'),
    webapp2.Route('/forbidden', ForbiddenHandler, name="forbidden"),
    webapp2.Route('/secured', SecuredSiteHandler, name="secured"),
], debug=True)
