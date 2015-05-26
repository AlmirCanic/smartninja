from app.handlers.base import Handler
from app.models.auth import User
from app.utils.decorators import employer_required


class EmployerCandidatesListHandler(Handler):
    @employer_required
    def get(self):
        candidates = User.query(User.job_searching == True).fetch()

        params = {"candidates": candidates}
        return self.render_template("employer/candidates_list.html", params)

    @employer_required
    def post(self):
        skill = self.request.get("skill")

        candidates = User.query(User.job_searching == True, User.grade_all_tags == skill).fetch()

        params = {"candidates": candidates}
        return self.render_template("employer/candidates_list.html", params)