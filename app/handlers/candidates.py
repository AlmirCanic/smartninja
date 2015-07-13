import datetime
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from app.emails.contact_candidate import email_employer_contact_candidate
from app.handlers.base import Handler
from app.models.auth import User
from app.models.contact_candidate import ContactCandidate
from app.models.course import CourseApplication
from app.models.employer import Employer
from app.settings import is_local
from app.utils.decorators import employer_required, admin_required


# ADMIN
from app.utils.other import convert_markdown_to_html


class AdminContactedCandidatesListHandler(Handler):
    @admin_required
    def get(self):
        contacted_list = ContactCandidate.query(ContactCandidate.deleted == False).order(-ContactCandidate.created).fetch()

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
        candidates = User.query(User.job_searching == True,
                                User.grade_avg_score >= 3.0).order(-User.grade_avg_score).fetch()

        current_user = users.get_current_user()
        employer = Employer.query(Employer.email == current_user.email().lower()).get()

        params = {"candidates": candidates, "employer": employer, "today": datetime.date.today()}
        return self.render_template("employer/candidates_list.html", params)


class EmployerCandidateDetailsHandler(Handler):
    @employer_required
    def get(self, candidate_id):
        candidate = User.get_by_id(int(candidate_id))

        applications = CourseApplication.query(CourseApplication.student_id == int(candidate_id),
                                               CourseApplication.deleted == False,
                                               CourseApplication.grade_score != None).fetch()

        current_user = users.get_current_user()
        employer = Employer.query(Employer.email == current_user.email().lower()).get()

        if candidate.long_description:
            candidate.long_description = convert_markdown_to_html(candidate.long_description)

        params = {"candidate": candidate, "applications": applications, "employer": employer}
        return self.render_template("employer/candidate_details.html", params)

    @employer_required
    def post(self, candidate_id):
        message = self.request.get("message")

        candidate = User.get_by_id(int(candidate_id))
        current_user = users.get_current_user()
        employer_user = User.get_by_email(email=current_user.email().lower())

        contact_candidate = ContactCandidate.create(candidate=candidate, employer_user=employer_user, message=message)

        employer = Employer.query(Employer.user_id == employer_user.get_id).get()

        contact_candidate.employer_company_id = employer.partner_id
        contact_candidate.employer_company_title = employer.partner_title
        contact_candidate.put()

        # partner or employer id added to candidate, so they know who they already contacted
        if employer.partner_id:
            if employer.partner_id not in candidate.contacted_by:
                candidate.contacted_by += (employer.partner_id, )
        else:
            if employer.get_id not in candidate.contacted_by:
                candidate.contacted_by += (employer.get_id, )
        candidate.put()

        if not is_local():
            email_employer_contact_candidate(contact_candidate)

        applications = CourseApplication.query(CourseApplication.student_id == int(candidate_id),
                                               CourseApplication.deleted == False,
                                               CourseApplication.grade_score != None).fetch()

        params = {"contact_success": True, "candidate": candidate, "applications": applications, "employer": employer}
        return self.render_template("employer/candidate_details.html", params)


class EmployerCandidateCVDownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
    @employer_required
    def get(self, candidate_id):
        candidate = User.get_by_id(int(candidate_id))

        if not blobstore.get(candidate.cv_blob):
            self.redirect_to('user-details', user_id=candidate_id)
        else:
            self.send_blob(candidate.cv_blob, save_as="%s.pdf" % candidate_id)


class EmployerContactedCandidatesListHandler(Handler):
    @employer_required
    def get(self):
        user = users.get_current_user()
        employer = Employer.query(Employer.email == user.email().lower()).get()

        if employer.partner_id:
            contacted_list = ContactCandidate.query(ContactCandidate.employer_company_id == employer.partner_id,
                                                    ContactCandidate.deleted == False).order(-ContactCandidate.created).fetch()
        else:
            contacted_list = ContactCandidate.query(ContactCandidate.employer_email == user.email().lower(),
                                                    ContactCandidate.deleted == False).order(-ContactCandidate.created).fetch()

        params = {"contacted_list": contacted_list, "employer": employer}

        return self.render_template("employer/contacted_list.html", params)