from app.handlers.base import Handler
from app.models.course import CourseType
from app.models.lesson import Lesson
from app.utils.decorators import admin_required, instructor_required


# ADMIN
from app.utils.other import logga


class AdminCourseTypesListHandler(Handler):
    @admin_required
    def get(self):
        course_types = CourseType.query(CourseType.deleted == False).fetch()
        params = {"course_types": course_types}
        self.render_template("admin/course_types_list.html", params)


class AdminCourseTypeDetailsHandler(Handler):
    @admin_required
    def get(self, course_type_id):
        course_type = CourseType.get_by_id(int(course_type_id))
        lessons = Lesson.query(Lesson.course_type == int(course_type_id), Lesson.deleted == False).order(Lesson.order).fetch()
        params = {"course_type": course_type, "lessons": lessons}
        self.render_template("admin/course_type_details.html", params)


class AdminCourseTypeAddHandler(Handler):
    @admin_required
    def get(self):
        self.render_template("admin/course_type_add.html")

    @admin_required
    def post(self):
        title = self.request.get("title")
        curriculum = self.request.get("curriculum")
        description = self.request.get("description")

        if title and curriculum:
            cur = CourseType.create(title=title, curriculum=curriculum, description=description)
            logga("Curriculum %s added." % cur.get_id)
            self.redirect_to("course-types-list")


class AdminCourseTypeEditHandler(Handler):
    @admin_required
    def get(self, course_type_id):
        course_type = CourseType.get_by_id(int(course_type_id))
        params = {"course_type": course_type}
        self.render_template("admin/course_type_edit.html", params)

    @admin_required
    def post(self, course_type_id):
        course_type = CourseType.get_by_id(int(course_type_id))
        course_type.title = self.request.get("title")
        course_type.curriculum = self.request.get("curriculum")
        course_type.description = self.request.get("description")
        course_type.put()
        logga("Curriculum %s edited." % course_type_id)
        self.redirect_to("course-type-details", course_type_id=int(course_type_id))


class AdminCourseTypeDeleteHandler(Handler):
    @admin_required
    def get(self, course_type_id):
        course_type = CourseType.get_by_id(int(course_type_id))
        params = {"course_type": course_type}
        self.render_template("admin/course_type_delete.html", params)

    @admin_required
    def post(self, course_type_id):
        course_type = CourseType.get_by_id(int(course_type_id))
        course_type.deleted = True
        course_type.put()
        logga("Curriculum %s deleted." % course_type_id)
        self.redirect_to("course-types-list")


# INSTRUCTOR

class InstructorCurriculumsListHandler(Handler):
    @instructor_required
    def get(self):
        course_types = CourseType.query(CourseType.deleted == False).fetch()
        params = {"course_types": course_types}
        self.render_template("instructor/course_types_list.html", params)


class InstructorCurriculumDetailsHandler(Handler):
    @instructor_required
    def get(self, course_type_id):
        course_type = CourseType.get_by_id(int(course_type_id))
        lessons = Lesson.query(Lesson.course_type == int(course_type_id), Lesson.deleted == False).order(Lesson.order).fetch()
        params = {"course_type": course_type, "lessons": lessons}
        self.render_template("instructor/course_type_details.html", params)


class InstructorCurriculumAddHandler(Handler):
    @instructor_required
    def get(self):
        self.render_template("instructor/course_type_add.html")

    @instructor_required
    def post(self):
        title = self.request.get("title")
        curriculum = self.request.get("curriculum")
        description = self.request.get("description")

        if title and curriculum:
            cur = CourseType.create(title=title, curriculum=curriculum, description=description)
            logga("Curriculum %s added." % cur.get_id)
            self.redirect_to("instructor-curriculum-list")


class InstructorCurriculumEditHandler(Handler):
    @instructor_required
    def get(self, course_type_id):
        course_type = CourseType.get_by_id(int(course_type_id))
        params = {"course_type": course_type}
        self.render_template("instructor/course_type_edit.html", params)

    @instructor_required
    def post(self, course_type_id):
        course_type = CourseType.get_by_id(int(course_type_id))
        course_type.title = self.request.get("title")
        course_type.curriculum = self.request.get("curriculum")
        course_type.description = self.request.get("description")
        course_type.put()
        logga("Curriculum %s edited." % course_type_id)
        self.redirect_to("instructor-curriculum-details", course_type_id=int(course_type_id))