from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from app.handlers.base import Handler
from app.models.auth import User
from app.models.course import CourseApplication
from app.settings import ADMINS
from app.utils.decorators import admin_required
from app.utils.other import logga


class AdminUsersListHandler(Handler):
    @admin_required
    def get(self):
        users = User.query(User.deleted == False).fetch()

        admins = []

        for user in users:
            if user.email in ADMINS:
                admins.append(user)

        params = {"admins": admins}
        self.render_template("admin/users_list.html", params)


class AdminUsersAllListHandler(Handler):
    @admin_required
    def get(self):
        users = User.query(User.deleted == False).fetch()

        params = {"users": users}
        self.render_template("admin/users_all_list.html", params)


class AdminUserDetailsHandler(Handler):
    @admin_required
    def get(self, user_id):
        user = User.get_by_id(int(user_id))
        admin = False
        if user.email in ADMINS:
            admin = True

        upload_url = blobstore.create_upload_url(success_path='/admin/user/%s/upload-cv' % user_id,
                                                 max_bytes_per_blob=1000000, max_bytes_total=1000000)  # max 1 MB

        applications = CourseApplication.query(CourseApplication.student_id == int(user_id),
                                               CourseApplication.deleted == False).fetch()

        params = {"this_user": user, "admin": admin, "upload_url": upload_url, "applications": applications}
        self.render_template("admin/user_details.html", params)


class AdminUserCVUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    @admin_required
    def post(self, user_id):
        try:
            upload = self.get_uploads()[0]

            user = User.get_by_id(int(user_id))

            user.cv_blob = upload.key()

            user.put()

            self.redirect_to('user-details', user_id=user_id)

        except Exception, e:
            self.response.out.write("upload failed: %s" % e)


class AdminUserCVDownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
    @admin_required
    def get(self, user_id):
        user = User.get_by_id(int(user_id))

        if not blobstore.get(user.cv_blob):
            self.redirect_to('user-details', user_id=user_id)
        else:
            self.send_blob(user.cv_blob, save_as="%s.pdf" % user_id)


class AdminUserDeleteHandler(Handler):
    @admin_required
    def get(self, user_id):
        user = User.get_by_id(int(user_id))
        params = {"this_user": user}
        self.render_template("admin/user_delete.html", params)

    @admin_required
    def post(self, user_id):
        user = User.get_by_id(int(user_id))
        if user.email not in ADMINS:
            user.deleted = True
            user.put()
            logga("User %s deleted." % user_id)
        self.redirect_to("users-list")


class AdminUserEditHandler(Handler):
    @admin_required
    def get(self, user_id):
        user = User.get_by_id(int(user_id))
        params = {"this_user": user}
        self.render_template("admin/user_edit.html", params)

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

        User.update(user=user, first_name=first_name, last_name=last_name, address=address, phone_number=phone_number,
                    summary=summary, photo_url=photo_url, dob=dob, github=github, job_searching=bool(job_searching),
                    current_town=current_town, linkedin=linkedin, homepage=homepage)

        logga("User %s edited." % user_id)
        self.redirect_to("user-details", user_id=int(user_id))