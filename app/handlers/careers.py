from google.appengine.api import memcache
from app.emails.careers import email_careers_to_smartninja_si
from app.handlers.base import Handler
from app.models.auth import User
from app.models.course import CourseType
from app.models.franchise import Franchise, FranchiseList
from app.models.instructor import Instructor
from app.models.job import Job
from app.models.job_application import JobApplication
from app.settings import is_local
from app.utils.csrf import get_csrf, check_csrf
from app.utils.decorators import manager_required, admin_required
from app.utils.other import logga


# ADMIN
class AdminCareersJobsListHandler(Handler):
    @admin_required
    def get(self):
        jobs = Job.query(Job.deleted == False).fetch()

        active_jobs = []
        past_jobs = []

        for job in jobs:
            if job.active:
                active_jobs.append(job)
            else:
                past_jobs.append(job)

        params = {"active_jobs": active_jobs, "past_jobs": past_jobs}

        return self.render_template("admin/careers_jobs_list.html", params)


class AdminCareersJobAddHandler(Handler):
    @admin_required
    def get(self):
        franchises = Franchise.query(Franchise.deleted == False).fetch()
        curriculums = CourseType.query(CourseType.deleted == False).fetch()

        params = {"franchises": franchises, "curriculums": curriculums}

        return self.render_template("admin/careers_job_add.html", params)

    @admin_required
    def post(self):
        title = self.request.get("title")
        city = self.request.get("city")
        curriculum_id = self.request.get("curriculum")
        franchise_id = self.request.get("franchise")
        description = self.request.get("description")

        curriculum = CourseType.get_by_id(int(curriculum_id))
        franchise = Franchise.get_by_id(int(franchise_id))

        job = Job.create(title=title, city=city, curriculum=curriculum, description=description, franchise=franchise)
        logga("Job %s created." % job.get_id)

        return self.redirect_to("admin-careers-jobs-list")


class AdminCareersJobEditHandler(Handler):
    @admin_required
    def get(self, job_id):
        job = Job.get_by_id(int(job_id))

        franchises = Franchise.query(Franchise.deleted == False).fetch()
        curriculums = CourseType.query(CourseType.deleted == False).fetch()

        params = {"job": job, "franchises": franchises, "curriculums": curriculums}

        return self.render_template("admin/careers_job_edit.html", params)

    @admin_required
    def post(self, job_id):
        job = Job.get_by_id(int(job_id))

        title = self.request.get("title")
        city = self.request.get("city")
        curriculum_id = self.request.get("curriculum")
        franchise_id = self.request.get("franchise")
        description = self.request.get("description")

        curriculum = CourseType.get_by_id(int(curriculum_id))
        franchise = Franchise.get_by_id(int(franchise_id))

        Job.update(job, title=title, city=city, curriculum=curriculum, description=description, franchise=franchise)
        logga("Job %s updated." % job.get_id)

        return self.redirect_to("admin-careers-job-details", job_id=job_id)


class AdminCareersJobDeleteHandler(Handler):
    @admin_required
    def get(self, job_id):
        job = Job.get_by_id(int(job_id))

        params = {"job": job}

        return self.render_template("admin/careers_job_delete.html", params)

    @admin_required
    def post(self, job_id):
        job = Job.get_by_id(int(job_id))

        Job.delete(job=job)
        logga("Job %s deleted." % job.get_id)

        return self.redirect_to("admin-careers-jobs-list")


class AdminCareersJobDeactivateHandler(Handler):
    @admin_required
    def post(self, job_id):
        job = Job.get_by_id(int(job_id))

        if job.active:
            job.active = False
            logga("Job %s deactivated." % job.get_id)
        else:
            job.active = True
            logga("Job %s activated." % job.get_id)

        job.put()

        return self.redirect_to("admin-careers-job-details", job_id=job_id)


class AdminCareersJobDetailsHandler(Handler):
    @admin_required
    def get(self, job_id):
        job = Job.get_by_id(int(job_id))
        applications = JobApplication.query(JobApplication.job_id == int(job_id),
                                            JobApplication.deleted == False).fetch()

        params = {"job": job, "applications": applications}

        return self.render_template("admin/careers_job_details.html", params)


class AdminCareersJobApplicationDetailsHandler(Handler):
    @admin_required
    def get(self, job_id, application_id):
        job = Job.get_by_id(int(job_id))
        application = JobApplication.get_by_id(int(application_id))

        params = {"job": job, "application": application}

        return self.render_template("admin/careers_job_application_details.html", params)


class AdminCareersJobApplicationEditHandler(Handler):
    @admin_required
    def get(self, job_id, application_id):
        application = JobApplication.get_by_id(int(application_id))

        params = {"application": application}

        return self.render_template("admin/careers_job_application_edit.html", params)

    @admin_required
    def post(self, job_id, application_id):
        application = JobApplication.get_by_id(int(application_id))

        phone = self.request.get("phone")
        city = self.request.get("city")
        linkedin = self.request.get("linkedin")
        github = self.request.get("github")

        JobApplication.update(application=application, phone=phone, city=city, linkedin=linkedin, github=github)

        return self.redirect_to("admin-careers-application-details", job_id=job_id, application_id=application_id)


class AdminCareersJobApplicationGradeHandler(Handler):
    @admin_required
    def post(self, job_id, application_id):
        application = JobApplication.get_by_id(int(application_id))

        grade = self.request.get("score")
        notes = self.request.get("notes")

        application.manager_grade = int(grade)
        application.manager_notes = notes
        application.put()

        return self.redirect_to("admin-careers-application-details", job_id=job_id, application_id=application_id)


class AdminCareersJobApplicationContactApproveHandler(Handler):
    @admin_required
    def post(self, job_id, application_id):
        application = JobApplication.get_by_id(int(application_id))

        contacted = self.request.get("contacted")
        approved = self.request.get("approved")

        JobApplication.contacted_and_approved(application=application, contacted=bool(contacted), approved=bool(approved))

        return self.redirect_to("admin-careers-application-details", job_id=job_id, application_id=application_id)


# MANAGER
class ManagerCareersDetailsHandler(Handler):
    """TEMPORARY: Remove this handler when local websites are ready"""
    @manager_required
    def get(self):
        forms_id = memcache.get(key="forms-id")
        height = memcache.get(key="forms-height")
        text = memcache.get(key="forms-text")

        params = {"form_id": forms_id, "height": height, "text": text}

        return self.render_template("manager/careers_details.html", params)


class ManagerCareersEditHandler(Handler):
    """TEMPORARY: Remove this handler when local websites are ready"""
    @manager_required
    def post(self):
        forms_id = self.request.get("forms-id")
        height = self.request.get("site-height")
        text = self.request.get("text")

        memcache.set(key="forms-id", value=forms_id)
        memcache.set(key="forms-height", value=height)
        memcache.set(key="forms-text", value=text)

        return self.redirect_to("manager-careers-details")


# PUBLIC
class PublicCareersJobDetailsHandler(Handler):
    def get(self, job_id):
        job = Job.get_by_id(int(job_id))
        jobs = Job.query(Job.deleted == False, Job.active == True).fetch()
        csrf = get_csrf()

        params = {"job": job, "jobs": jobs, "csrf": csrf}

        return self.render_template("public/careers_job_details.html", params)

    def post(self, job_id):
        hidden = self.request.get("hidden")
        csrf = self.request.get("csrf")
        if hidden:
            return self.redirect_to("public-careers-job-details", job_id=int(job_id))
        elif check_csrf(csrf):
            job = Job.get_by_id(int(job_id))

            first_name = self.request.get("first_name")
            last_name = self.request.get("last_name")
            email = self.request.get("email").strip().lower()
            city = self.request.get("city")
            phone = self.request.get("phone")
            linkedin = self.request.get("linkedin")
            github = self.request.get("github")
            experience = self.request.get("experience")
            other_info = self.request.get("other_info")

            # create user, instructor and job_application objects for the applicant
            user = User.get_or_short_create(email=email, first_name=first_name, last_name=last_name)
            instructor = Instructor.add_or_create(full_name=user.get_full_name, email=email,
                                                  franchises=[FranchiseList(franchise_id=job.franchise_id, franchise_title=job.franchise_title)],
                                                  user_id=user.get_id, city=city)
            job_application = JobApplication.create(instructor=instructor, city=city, email=email, experience=experience,
                                                    github_url=github, job=job, linkedin_url=linkedin, phone=phone,
                                                    other_info=other_info)
            # send email to smartninja.si
            if not is_local():
                email_careers_to_smartninja_si(full_name=user.get_full_name, email=email, city=city, phone=phone,
                                               linkedin=linkedin, github=github, experience=experience, other=other_info)
            return self.render_template("public/careers_job_thank_you.html")
        else:
            return self.redirect_to("oops")