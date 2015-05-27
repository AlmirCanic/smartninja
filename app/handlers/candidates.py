from google.appengine.api import users
from app.emails.contact_candidate import email_employer_contact_candidate
from app.handlers.base import Handler
from app.models.auth import User
from app.models.contact_candidate import ContactCandidate
from app.models.course import CourseApplication
from app.settings import is_local
from app.utils.decorators import employer_required, admin_required


# ADMIN
class AdminContactedCandidatesListHandler(Handler):
    @admin_required
    def get(self):
        contacted_list = ContactCandidate.query(ContactCandidate.deleted == False).fetch()

        params = {"contacted_list": contacted_list}

        return self.render_template("admin/contacted_list.html", params)


class AdminSuccessfullyEmployedHandler(Handler):
    @admin_required
    def post(self, contacted_candidate_id):
        employed = self.request.get("employed")

        contacted = ContactCandidate.get_by_id(int(contacted_candidate_id))
        contacted.successful_employment = bool(employed)
        contacted.put()

        return self.redirect_to("admin-contacted-list")


# EMPLOYER
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

    @employer_required
    def post(self, candidate_id):
        message = self.request.get("message")

        candidate = User.get_by_id(int(candidate_id))
        employer = users.get_current_user()
        employer_user = User.get_by_email(email=employer.email())

        contact_candidate = ContactCandidate.create(candidate=candidate, employer_user=employer_user, message=message)

        if not is_local():
            email_employer_contact_candidate(contact_candidate)

        applications = CourseApplication.query(CourseApplication.student_id == int(candidate_id),
                                               CourseApplication.deleted == False,
                                               CourseApplication.grade_score != None).fetch()

        params = {"contact_success": True, "candidate": candidate, "applications": applications}
        return self.render_template("employer/candidate_details.html", params)


class EmployerContactedCandidatesListHandler(Handler):
    @employer_required
    def get(self):
        employer = users.get_current_user()

        contacted_list = ContactCandidate.query(ContactCandidate.employer_email == employer.email(),
                                                ContactCandidate.deleted == False).fetch()

        params = {"contacted_list": contacted_list}

        return self.render_template("employer/contacted_list.html", params)