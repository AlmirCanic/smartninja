from google.appengine.api import memcache
from app.handlers.base import Handler
from app.models.course import CourseType
from app.models.franchise import Franchise
from app.models.job import Job
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

        params = {"job": job}

        return self.render_template("admin/careers_job_details.html", params)


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