# ADMIN
from app.handlers.base import Handler
from app.models.auth import User
from app.models.instructor import Instructor
from app.utils.decorators import admin_required


class AdminInstructorsListHandler(Handler):
    @admin_required
    def get(self):
        instructors = Instructor.query().fetch()
        params = {"instructors": instructors}
        self.render_template("admin/instructor_list.html", params)


class AdminInstructorAddHandler(Handler):
    @admin_required
    def get(self):
        self.render_template("admin/instructor_add.html")

    @admin_required
    def post(self):
        email = self.request.get("email")
        first_name = self.request.get("first-name")
        last_name = self.request.get("last-name")

        user = User.get_by_email(email=email)

        if not user:
            user = User.short_create(email=email, first_name=first_name, last_name=last_name)

        Instructor.create(full_name=user.get_full_name, email=email, user_id=user.get_id)

        return self.redirect_to("admin-instructors-list")


class AdminInstructorDeleteHandler(Handler):
    @admin_required
    def get(self, instructor_id):
        instructor = Instructor.get_by_id(int(instructor_id))
        params = {"instructor": instructor}
        self.render_template("admin/instructor_delete.html", params)
    @admin_required
    def post(self, instructor_id):
        instructor = Instructor.get_by_id(int(instructor_id))
        instructor.key.delete()
        self.redirect_to("admin-instructors-list")