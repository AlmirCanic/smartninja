from app.handlers.base import Handler
from app.models.auth import User
from app.models.course import CourseApplication
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


class EmployerCandidateDetailsHandler(Handler):
    @employer_required
    def get(self, candidate_id):
        candidate = User.get_by_id(int(candidate_id))

        applications = CourseApplication.query(CourseApplication.student_id == int(candidate_id),
                                               CourseApplication.deleted == False,
                                               CourseApplication.grade_score != None).fetch()

        params = {"candidate": candidate, "applications": applications}
        return self.render_template("employer/candidate_details.html", params)