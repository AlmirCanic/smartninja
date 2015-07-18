from app.handlers.base import Handler
from app.models.auth import User
from app.settings import ADMINS
from app.utils.decorators import admin_required, manager_required
from app.utils.other import convert_tags_to_string, convert_tags_to_list
from app.utils.user_utils import change_email


# ADMIN
class AdminUserChangeEmailHandler(Handler):
    @admin_required
    def get(self, user_id):
        user = User.get_by_id(int(user_id))
        params = {"this_user": user}
        self.render_template("admin/user_change_email.html", params)

    @admin_required
    def post(self, user_id):
        user = User.get_by_id(int(user_id))
        email = self.request.get("email")

        other_user = User.get_by_email(email=email)

        if not other_user or other_user.deleted == True:
            change_email(user, email)
            self.redirect_to("user-details", user_id=int(user_id))
        else:
            self.redirect_to("admin-user-join-accounts", user_id_1=int(user_id), user_id_2=other_user.get_id)


class AdminUserJoinAccountsHandler(Handler):
    @admin_required
    def get(self, user_id_1, user_id_2):
        user1 = User.get_by_id(int(user_id_1))
        user2 = User.get_by_id(int(user_id_2))

        tags1 = convert_tags_to_string(user1.grade_all_tags)
        tags2 = convert_tags_to_string(user2.grade_all_tags)

        params = {"user1": user1, "user2": user2, "tags1": tags1, "tags2": tags2}
        self.render_template("admin/user_join_accounts.html", params)

    @admin_required
    def post(self, user_id_1, user_id_2):
        user1 = User.get_by_id(int(user_id_1))
        user2 = User.get_by_id(int(user_id_2))
        email = user2.email

        first_name = self.request.get("first_name")
        last_name = self.request.get("last_name")
        address = self.request.get("address")
        photo_url = self.request.get("photo")
        phone_number = self.request.get("phone_number")
        dob = self.request.get("dob")
        github = self.request.get("github")
        grade_avg_score = self.request.get("grade_avg_score")
        grade_all_tags = self.request.get("grade_all_tags")

        if grade_avg_score == None or grade_avg_score == "None" or grade_avg_score == "":
            grade_avg_score = 0.0

        if grade_all_tags == "":
            grade_all_tags = []
        else:
            grade_all_tags = convert_tags_to_list(grade_all_tags)

        user = User.update(user=user1, first_name=first_name, last_name=last_name, address=address, phone_number=phone_number,
                    summary=user1.summary, photo_url=photo_url, dob=dob, github=github)

        user.grade_avg_score = float(grade_avg_score)
        user.grade_all_tags = list(grade_all_tags)
        user.put()

        change_email(user1, email)
        change_email(user2, email, new_user=user1)

        user2.deleted = True
        user2.put()

        self.redirect_to("user-details", user_id=int(user_id_1))


# MANAGER
class ManagerUserChangeEmailHandler(Handler):
    @manager_required
    def get(self, user_id):
        user = User.get_by_id(int(user_id))
        params = {"this_user": user}
        return self.render_template("manager/user_change_email.html", params)

    @manager_required
    def post(self, user_id):
        user = User.get_by_id(int(user_id))
        email = self.request.get("email")

        other_user = User.get_by_email(email=email)

        if other_user:
            if user.email in ADMINS or other_user.email in ADMINS:
                return self.redirect_to("forbidden")

        if not other_user or other_user.deleted == True:
            change_email(user, email)
            return self.redirect_to("manager-user-details", user_id=int(user_id))
        else:
            return self.redirect_to("manager-user-join-accounts", user_id_1=int(user_id), user_id_2=other_user.get_id)


class ManagerUserJoinAccountsHandler(Handler):
    @manager_required
    def get(self, user_id_1, user_id_2):
        user1 = User.get_by_id(int(user_id_1))
        user2 = User.get_by_id(int(user_id_2))

        tags1 = convert_tags_to_string(user1.grade_all_tags)
        tags2 = convert_tags_to_string(user2.grade_all_tags)

        params = {"user1": user1, "user2": user2, "tags1": tags1, "tags2": tags2}
        return self.render_template("manager/user_join_accounts.html", params)

    @manager_required
    def post(self, user_id_1, user_id_2):
        user1 = User.get_by_id(int(user_id_1))
        user2 = User.get_by_id(int(user_id_2))
        email = user2.email

        if user1.email in ADMINS or user2.email in ADMINS:
            return self.redirect_to("forbidden")

        first_name = self.request.get("first_name")
        last_name = self.request.get("last_name")
        address = self.request.get("address")
        photo_url = self.request.get("photo")
        phone_number = self.request.get("phone_number")
        dob = self.request.get("dob")
        github = self.request.get("github")
        grade_avg_score = self.request.get("grade_avg_score")
        grade_all_tags = self.request.get("grade_all_tags")

        if grade_avg_score == None or grade_avg_score == "None" or grade_avg_score == "":
            grade_avg_score = 0.0

        if grade_all_tags == "":
            grade_all_tags = []
        else:
            grade_all_tags = convert_tags_to_list(grade_all_tags)

        user = User.update(user=user1, first_name=first_name, last_name=last_name, address=address,
                           phone_number=phone_number, summary=user1.summary, photo_url=photo_url, dob=dob,
                           github=github)

        user.grade_avg_score = float(grade_avg_score)
        user.grade_all_tags = list(grade_all_tags)
        user.put()

        change_email(user1, email)
        change_email(user2, email, new_user=user1)

        user2.deleted = True
        user2.put()

        return self.redirect_to("manager-user-details", user_id=int(user_id_1))