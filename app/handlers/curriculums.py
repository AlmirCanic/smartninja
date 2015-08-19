from google.appengine.api import users
from app.handlers.base import Handler
from app.models.course import CourseType
from app.models.franchise import Franchise, FranchiseList
from app.models.instructor import Instructor
from app.models.lesson import Lesson
from app.models.manager import Manager
from app.utils.decorators import admin_required, instructor_required, manager_required
from app.utils.other import logga


# ADMIN
class AdminCourseTypesListHandler(Handler):
    @admin_required
    def get(self):
        course_types = CourseType.query(CourseType.deleted == False).fetch()
        params = {"course_types": course_types}
        return self.render_template("admin/course_types_list.html", params)


class AdminCourseTypeDetailsHandler(Handler):
    @admin_required
    def get(self, course_type_id):
        course_type = CourseType.get_by_id(int(course_type_id))
        lessons = Lesson.query(Lesson.course_type == int(course_type_id),
                               Lesson.deleted == False).order(Lesson.order).fetch()
        params = {"course_type": course_type, "lessons": lessons}
        return self.render_template("admin/course_type_details.html", params)


class AdminCourseTypeAddHandler(Handler):
    @admin_required
    def get(self):
        franchises = Franchise.query(Franchise.deleted == False).fetch()
        params = {"franchises": franchises}
        return self.render_template("admin/course_type_add.html", params)

    @admin_required
    def post(self):
        title = self.request.get("title")
        curriculum = self.request.get("curriculum")
        description = self.request.get("description")
        franchise_id = self.request.get("franchise")

        franchise = Franchise.get_by_id(int(franchise_id))
        franchise_list_item = FranchiseList(franchise_id=franchise.get_id, franchise_title=franchise.title)

        if title and curriculum:
            cur = CourseType.create(title=title, curriculum=curriculum, description=description,
                                    franchises=[franchise_list_item])
            logga("Curriculum %s added." % cur.get_id)
            return self.redirect_to("course-types-list")


class AdminCourseTypeEditHandler(Handler):
    @admin_required
    def get(self, course_type_id):
        course_type = CourseType.get_by_id(int(course_type_id))
        franchises = Franchise.query(Franchise.deleted == False).fetch()
        params = {"course_type": course_type, "franchises": franchises}
        return self.render_template("admin/course_type_edit.html", params)

    @admin_required
    def post(self, course_type_id):
        course_type = CourseType.get_by_id(int(course_type_id))
        title = self.request.get("title")
        curriculum = self.request.get("curriculum")
        description = self.request.get("description")
        franchise_id = self.request.get("franchise")

        franchise = Franchise.get_by_id(int(franchise_id))
        franchise_list_item = FranchiseList(franchise_id=franchise.get_id, franchise_title=franchise.title)

        CourseType.update(course_type=course_type, title=title, curriculum=curriculum, description=description,
                          franchises=[franchise_list_item])

        logga("Curriculum %s edited." % course_type_id)
        return self.redirect_to("course-type-details", course_type_id=int(course_type_id))


class AdminCourseTypeDeleteHandler(Handler):
    @admin_required
    def get(self, course_type_id):
        course_type = CourseType.get_by_id(int(course_type_id))
        params = {"course_type": course_type}
        return self.render_template("admin/course_type_delete.html", params)

    @admin_required
    def post(self, course_type_id):
        course_type = CourseType.get_by_id(int(course_type_id))
        course_type.deleted = True
        course_type.put()
        logga("Curriculum %s deleted." % course_type_id)
        return self.redirect_to("course-types-list")


# MANAGER
class ManagerCourseTypesListHandler(Handler):
    @manager_required
    def get(self):
        current_user = users.get_current_user()
        manager = Manager.query(Manager.email == str(current_user.email()).lower()).get()

        course_types = CourseType.query(CourseType.deleted == False,
                                        CourseType.franchises.franchise_id == manager.franchise_id).fetch()

        params = {"course_types": course_types}
        return self.render_template("manager/course_types_list.html", params)


class ManagerCourseTypeDetailsHandler(Handler):
    @manager_required
    def get(self, course_type_id):
        course_type = CourseType.get_by_id(int(course_type_id))

        lessons = Lesson.query(Lesson.course_type == int(course_type_id),
                               Lesson.deleted == False).order(Lesson.order).fetch()

        params = {"course_type": course_type, "lessons": lessons}
        return self.render_template("manager/course_type_details.html", params)


class ManagerCourseTypeAddHandler(Handler):
    @manager_required
    def get(self):
        return self.render_template("manager/course_type_add.html")

    @manager_required
    def post(self):
        title = self.request.get("title")
        curriculum = self.request.get("curriculum")
        description = self.request.get("description")

        current_user = users.get_current_user()
        manager = Manager.query(Manager.email == str(current_user.email()).lower()).get()

        franchise_list_item = FranchiseList(franchise_id=manager.franchise_id, franchise_title=manager.franchise_title)

        if title and curriculum:
            cur = CourseType.create(title=title, curriculum=curriculum, description=description,
                                    franchises=[franchise_list_item])
            logga("Curriculum %s added." % cur.get_id)
            return self.redirect_to("manager-course-types-list")


class ManagerCourseTypeEditHandler(Handler):
    @manager_required
    def get(self, course_type_id):
        course_type = CourseType.get_by_id(int(course_type_id))
        params = {"course_type": course_type}
        return self.render_template("manager/course_type_edit.html", params)

    @manager_required
    def post(self, course_type_id):
        course_type = CourseType.get_by_id(int(course_type_id))
        title = self.request.get("title")
        curriculum = self.request.get("curriculum")
        description = self.request.get("description")

        CourseType.update(course_type=course_type, title=title, curriculum=curriculum, description=description)

        logga("Curriculum %s edited." % course_type_id)
        return self.redirect_to("manager-course-type-details", course_type_id=int(course_type_id))


class ManagerCourseTypeDeleteHandler(Handler):
    @manager_required
    def get(self, course_type_id):
        course_type = CourseType.get_by_id(int(course_type_id))
        params = {"course_type": course_type}
        return self.render_template("manager/course_type_delete.html", params)

    @manager_required
    def post(self, course_type_id):
        course_type = CourseType.get_by_id(int(course_type_id))

        current_user = users.get_current_user()
        manager = Manager.query(Manager.email == str(current_user.email()).lower()).get()
        franchise_list_item = FranchiseList(franchise_id=manager.franchise_id, franchise_title=manager.franchise_title)

        if franchise_list_item in course_type.franchises:
            course_type.franchises.remove(franchise_list_item)
            course_type.put()

        logga("Curriculum %s removed for franchise %s." % (course_type_id, manager.franchise_id))
        return self.redirect_to("manager-course-types-list")


# INSTRUCTOR
class InstructorCurriculumsListHandler(Handler):
    @instructor_required
    def get(self):
        curr_user = users.get_current_user()
        instructor = Instructor.query(Instructor.email == curr_user.email().lower()).get()

        params = {"instructor": instructor}
        return self.render_template("instructor/course_types_list.html", params)


class InstructorCurriculumDetailsHandler(Handler):
    @instructor_required
    def get(self, course_type_id):
        course_type = CourseType.get_by_id(int(course_type_id))
        lessons = Lesson.query(Lesson.course_type == int(course_type_id), Lesson.deleted == False).order(Lesson.order).fetch()
        params = {"course_type": course_type, "lessons": lessons}
        return self.render_template("instructor/course_type_details.html", params)


'''
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
'''