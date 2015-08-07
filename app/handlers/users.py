import datetime
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.api import images
from google.appengine.ext.webapp import blobstore_handlers
from app.handlers.base import Handler
from app.models.auth import User
from app.models.course import CourseApplication
from app.models.manager import Manager
from app.settings import ADMINS
from app.utils.decorators import admin_required, manager_required
from app.utils.other import logga, convert_markdown_to_html, convert_tags_to_string, convert_tags_to_list


# ADMIN
class AdminUsersListHandler(Handler):
    @admin_required
    def get(self):
        users = User.query(User.deleted == False).fetch()

        admins = []

        for user in users:
            if user.email in ADMINS:
                admins.append(user)

        params = {"admins": admins}
        return self.render_template("admin/users_list.html", params)


class AdminUsersAllListHandler(Handler):
    @admin_required
    def get(self):
        users = User.query(User.deleted == False).fetch()

        params = {"users": users}
        return self.render_template("admin/users_all_list.html", params)


class AdminUserDetailsHandler(Handler):
    @admin_required
    def get(self, user_id):
        user = User.get_by_id(int(user_id))
        admin = False
        if user.email in ADMINS:
            admin = True

        # get url to upload CV
        cv_upload_url = blobstore.create_upload_url(success_path='/admin/user/%s/upload-cv' % user_id,
                                                    max_bytes_per_blob=1000000, max_bytes_total=1000000)  # max 1 MB

        # get all the courses that user applied to
        applications = CourseApplication.query(CourseApplication.student_id == int(user_id),
                                               CourseApplication.deleted == False).fetch()

        # convert long description from markdown to html
        if user.long_description:
            user.long_description = convert_markdown_to_html(user.long_description)

        # convert skills and grade tags to string
        other_skills = convert_tags_to_string(user.other_skills)
        grade_all_tags = convert_tags_to_string(user.grade_all_tags)

        # get profile image url
        if user.photo_blob:
            photo_url = images.get_serving_url(blob_key=user.photo_blob)
        else:
            photo_url = user.photo_url


        params = {"this_user": user, "admin": admin, "upload_url": cv_upload_url, "applications": applications,
                  "other_skills": other_skills, "grade_all_tags": grade_all_tags, "photo_url": photo_url}
        return self.render_template("admin/user_details.html", params)


class AdminUserCVUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    @admin_required
    def post(self, user_id):
        try:
            upload = self.get_uploads()[0]

            user = User.get_by_id(int(user_id))

            user.cv_blob = upload.key()

            user.put()

            return self.redirect_to('user-details', user_id=user_id)

        except Exception, e:
            return self.response.out.write("upload failed: %s" % e)


class AdminUserCVDownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
    @admin_required
    def get(self, user_id):
        user = User.get_by_id(int(user_id))

        if not blobstore.get(user.cv_blob):
            return self.redirect_to('user-details', user_id=user_id)
        else:
            return self.send_blob(user.cv_blob, save_as="%s.pdf" % user_id)


class AdminUserPhotoHandler(Handler):
    @admin_required
    def get(self, user_id):
        user = User.get_by_id(int(user_id))

        photo_upload_url = blobstore.create_upload_url(success_path='/admin/user/%s/photo/upload' % user_id,
                                                       max_bytes_per_blob=1000000, max_bytes_total=1000000)  # max 1 MB

        params = {"this_user": user, "upload_url": photo_upload_url}
        return self.render_template("admin/user_photo_upload.html", params)


class AdminUserPhotoUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    @admin_required
    def post(self, user_id):
        try:
            upload = self.get_uploads()[0]
            user = User.get_by_id(int(user_id))
            user.photo_blob = upload.key()
            user.put()
            return self.redirect_to('user-details', user_id=user_id)
        except Exception, e:
            return self.response.out.write("upload failed: %s" % e)


class AdminUserDeleteHandler(Handler):
    @admin_required
    def get(self, user_id):
        user = User.get_by_id(int(user_id))
        params = {"this_user": user}
        return self.render_template("admin/user_delete.html", params)

    @admin_required
    def post(self, user_id):
        user = User.get_by_id(int(user_id))
        if user.email not in ADMINS:
            user.deleted = True
            user.put()
            logga("User %s deleted." % user_id)
        return self.redirect_to("users-list")


class AdminUserEditHandler(Handler):
    @admin_required
    def get(self, user_id):
        user = User.get_by_id(int(user_id))

        courses_skills = convert_tags_to_string(user.grade_all_tags)

        other_skills = convert_tags_to_string(user.other_skills)

        params = {"this_user": user, "other_skills": other_skills, "courses_skills": courses_skills}
        return self.render_template("admin/user_edit.html", params)

    @admin_required
    def post(self, user_id):
        user = User.get_by_id(int(user_id))

        first_name = self.request.get("first_name")
        last_name = self.request.get("last_name")
        address = self.request.get("address")
        current_town = self.request.get("current-town")
        summary = self.request.get("summary")
        photo_url = self.request.get("photo_url")
        phone_number = self.request.get("phone_number")
        dob = self.request.get("dob")
        job_searching = self.request.get("searching")
        github = self.request.get("github_url")
        linkedin = self.request.get("linkedin_url")
        homepage = self.request.get("homepage_url")
        programming_year = self.request.get("programming-year")
        programming_month = self.request.get("programming-month")
        long_description = self.request.get("long-description")
        other_skills = self.request.get("skills")

        skills_list = convert_tags_to_list(other_skills)

        # add only skilly that are not already in skills from courses (grade_all_tags)
        skills_list_clean = []

        for skill in skills_list:
            if skill not in user.grade_all_tags:
                skills_list_clean.append(skill)

        if programming_month and programming_year:
            started_programming = datetime.date(year=int(programming_year), month=int(programming_month), day=10)
        else:
            started_programming = None

        User.update(user=user, first_name=first_name, last_name=last_name, address=address, phone_number=phone_number,
                    summary=summary, photo_url=photo_url, dob=dob, github=github, job_searching=bool(job_searching),
                    current_town=current_town, linkedin=linkedin, homepage=homepage,
                    started_programming=started_programming, long_description=long_description,
                    other_skills=skills_list_clean)

        logga("User %s edited." % user_id)
        return self.redirect_to("user-details", user_id=int(user_id))


# MANAGER
class ManagerUsersListHandler(Handler):
    @manager_required
    def get(self):
        curr_user = users.get_current_user()
        manager = Manager.query(Manager.email == curr_user.email().lower()).get()

        managers = Manager.query(Manager.franchise_id == manager.franchise_id).fetch()

        params = {"managers": managers}
        return self.render_template("manager/users_list.html", params)


class ManagerUserDetailsHandler(Handler):
    @manager_required
    def get(self, user_id):
        user = User.get_by_id(int(user_id))

        admin = False
        if user.email in ADMINS:
            admin = True

        upload_url = blobstore.create_upload_url(success_path='/manager/user/%s/upload-cv' % user_id,
                                                 max_bytes_per_blob=1000000, max_bytes_total=1000000)  # max 1 MB

        applications = CourseApplication.query(CourseApplication.student_id == int(user_id),
                                               CourseApplication.deleted == False).fetch()

        if user.long_description:
            user.long_description = convert_markdown_to_html(user.long_description)

        other_skills = convert_tags_to_string(user.other_skills)
        grade_all_tags = convert_tags_to_string(user.grade_all_tags)

        params = {"this_user": user, "admin": admin, "upload_url": upload_url, "applications": applications,
                  "other_skills": other_skills, "grade_all_tags": grade_all_tags}

        return self.render_template("manager/user_details.html", params)


class ManagerUserEditHandler(Handler):
    @manager_required
    def get(self, user_id):
        user = User.get_by_id(int(user_id))

        if user.email in ADMINS and not users.get_current_user().email() in ADMINS:
            return self.redirect_to("forbidden")

        courses_skills = convert_tags_to_string(user.grade_all_tags)

        other_skills = convert_tags_to_string(user.other_skills)

        params = {"this_user": user, "other_skills": other_skills, "courses_skills": courses_skills}
        return self.render_template("manager/user_edit.html", params)

    @manager_required
    def post(self, user_id):
        user = User.get_by_id(int(user_id))

        if user.email in ADMINS and not users.get_current_user().email() in ADMINS:
            return self.redirect_to("forbidden")

        first_name = self.request.get("first_name")
        last_name = self.request.get("last_name")
        address = self.request.get("address")
        current_town = self.request.get("current-town")
        summary = self.request.get("summary")
        photo_url = self.request.get("photo_url")
        phone_number = self.request.get("phone_number")
        dob = self.request.get("dob")
        job_searching = self.request.get("searching")
        github = self.request.get("github_url")
        linkedin = self.request.get("linkedin_url")
        homepage = self.request.get("homepage_url")
        programming_year = self.request.get("programming-year")
        programming_month = self.request.get("programming-month")
        long_description = self.request.get("long-description")
        other_skills = self.request.get("skills")

        skills_list = convert_tags_to_list(other_skills)

        # add only skilly that are not already in skills from courses (grade_all_tags)
        skills_list_clean = []

        for skill in skills_list:
            if skill not in user.grade_all_tags:
                skills_list_clean.append(skill)

        if programming_month and programming_year:
            started_programming = datetime.date(year=int(programming_year), month=int(programming_month), day=10)
        else:
            started_programming = None

        User.update(user=user, first_name=first_name, last_name=last_name, address=address, phone_number=phone_number,
                    summary=summary, photo_url=photo_url, dob=dob, github=github, job_searching=bool(job_searching),
                    current_town=current_town, linkedin=linkedin, homepage=homepage,
                    started_programming=started_programming, long_description=long_description,
                    other_skills=skills_list_clean)

        logga("User %s edited." % user_id)
        return self.redirect_to("manager-user-details", user_id=int(user_id))


class ManagerUserDeleteHandler(Handler):
    @manager_required
    def get(self, user_id):
        user = User.get_by_id(int(user_id))
        params = {"this_user": user}
        return self.render_template("manager/user_delete.html", params)

    @manager_required
    def post(self, user_id):
        user = User.get_by_id(int(user_id))
        if user.email not in ADMINS:
            user.deleted = True
            user.put()
            logga("User %s deleted." % user_id)
        return self.redirect_to("manager-users-list")


class ManagerUserCVUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    @manager_required
    def post(self, user_id):
        try:
            upload = self.get_uploads()[0]

            user = User.get_by_id(int(user_id))

            user.cv_blob = upload.key()

            user.put()

            return self.redirect_to('manager-user-details', user_id=user_id)

        except Exception, e:
            return self.response.out.write("upload failed: %s" % e)


class ManagerUserCVDownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
    @manager_required
    def get(self, user_id):
        user = User.get_by_id(int(user_id))

        if not blobstore.get(user.cv_blob):
            return self.redirect_to('manager-user-details', user_id=user_id)
        else:
            return self.send_blob(user.cv_blob, save_as="%s.pdf" % user_id)