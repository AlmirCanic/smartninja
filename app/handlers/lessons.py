from app.handlers.base import Handler
from app.models.course import CourseType, Course
from app.models.lesson import Lesson
from app.utils.decorators import admin_required, instructor_required, student_required
from app.utils.other import convert_markdown_to_html, logga


# ADMIN

class AdminLessonAddHandler(Handler):
    @admin_required
    def get(self, course_type_id):
        course_type = CourseType.get_by_id(int(course_type_id))
        params = {"course_type": course_type}
        self.render_template("admin/lesson_add.html", params=params)

    @admin_required
    def post(self, course_type_id):
        title = self.request.get("title")
        order = self.request.get("order")
        text = self.request.get("text")

        if title and text:
            lesson = Lesson.create(title=title, order=int(order), text=text, course_type=int(course_type_id))
            logga("Lesson %s added." % lesson.get_id)
            self.redirect_to("admin-lesson-details", lesson_id=lesson.get_id)


class AdminLessonDetailsHandler(Handler):
    @admin_required
    def get(self, lesson_id):
        lesson = Lesson.get_by_id(int(lesson_id))
        course_type = CourseType.get_by_id(lesson.course_type)
        lesson.text = convert_markdown_to_html(lesson.text)
        params = {"lesson": lesson, "course_type": course_type}
        self.render_template("admin/lesson_details.html", params)


class AdminLessonEditHandler(Handler):
    @admin_required
    def get(self, lesson_id):
        lesson = Lesson.get_by_id(int(lesson_id))
        course_type = CourseType.get_by_id(lesson.course_type)
        params = {"course_type": course_type, "lesson": lesson}
        self.render_template("admin/lesson_edit.html", params)

    @admin_required
    def post(self, lesson_id):
        title = self.request.get("title")
        order = self.request.get("order")
        text = self.request.get("text")

        if title and text:
            lesson = Lesson.get_by_id(int(lesson_id))
            course_type = CourseType.get_by_id(lesson.course_type)
            Lesson.update(lesson=lesson, title=title, order=int(order), text=text, course_type=course_type.get_id)
            logga("Lesson %s updated." % lesson_id)
            self.redirect_to("admin-lesson-details", lesson_id=int(lesson_id))
        else:
            self.redirect_to("oops")


class AdminLessonDeleteHandler(Handler):
    @admin_required
    def get(self, lesson_id):
        lesson = Lesson.get_by_id(int(lesson_id))
        course_type = CourseType.get_by_id(lesson.course_type)
        params = {"course_type": course_type, "lesson": lesson}
        self.render_template("admin/lesson_delete.html", params)

    @admin_required
    def post(self, lesson_id):
        lesson = Lesson.get_by_id(int(lesson_id))
        lesson.deleted = True
        lesson.put()
        logga("Lesson %s deleted." % lesson_id)
        self.redirect_to("course-type-details", course_type_id=lesson.course_type)


# INSTRUCTOR

class InstructorLessonAddHandler(Handler):
    @instructor_required
    def get(self, course_type_id):
        course_type = CourseType.get_by_id(int(course_type_id))
        params = {"course_type": course_type}
        self.render_template("instructor/lesson_add.html", params=params)

    @instructor_required
    def post(self, course_type_id):
        title = self.request.get("title")
        order = self.request.get("order")
        text = self.request.get("text")

        if title and text:
            lesson = Lesson.create(title=title, order=int(order), text=text, course_type=int(course_type_id))
            logga("Lesson %s added." % lesson.get_id)
            self.redirect_to("instructor-lesson-details", lesson_id=lesson.get_id)


class InstructorLessonDetailsHandler(Handler):
    @instructor_required
    def get(self, lesson_id):
        lesson = Lesson.get_by_id(int(lesson_id))
        course_type = CourseType.get_by_id(lesson.course_type)
        lesson.text = convert_markdown_to_html(lesson.text)
        params = {"lesson": lesson, "course_type": course_type}
        self.render_template("instructor/lesson_details.html", params)


class InstructorLessonEditHandler(Handler):
    @instructor_required
    def get(self, lesson_id):
        lesson = Lesson.get_by_id(int(lesson_id))
        course_type = CourseType.get_by_id(lesson.course_type)
        params = {"course_type": course_type, "lesson": lesson}
        self.render_template("instructor/lesson_edit.html", params)

    @instructor_required
    def post(self, lesson_id):
        title = self.request.get("title")
        order = self.request.get("order")
        text = self.request.get("text")

        if title and text:
            lesson = Lesson.get_by_id(int(lesson_id))
            course_type = CourseType.get_by_id(lesson.course_type)
            Lesson.update(lesson=lesson, title=title, order=int(order), text=text, course_type=course_type.get_id)
            logga("Lesson %s updated." % lesson_id)
            self.redirect_to("instructor-lesson-details", lesson_id=int(lesson_id))
        else:
            self.redirect_to("oops")


class InstructorLessonDeleteHandler(Handler):
    @instructor_required
    def get(self, lesson_id):
        lesson = Lesson.get_by_id(int(lesson_id))
        course_type = CourseType.get_by_id(lesson.course_type)
        params = {"course_type": course_type, "lesson": lesson}
        self.render_template("instructor/lesson_delete.html", params)

    @instructor_required
    def post(self, lesson_id):
        lesson = Lesson.get_by_id(int(lesson_id))
        lesson.deleted = True
        lesson.put()
        logga("Lesson %s deleted." % lesson_id)
        self.redirect_to("instructor-curriculum-details", course_type_id=lesson.course_type)


# STUDENT
class StudentLessonDetailsHandler(Handler):
    @student_required
    def get(self, course_id, lesson_id):
        lesson = Lesson.get_by_id(int(lesson_id))
        course = Course.get_by_id(int(course_id))
        lesson.text = convert_markdown_to_html(lesson.text)
        params = {"lesson": lesson, "course": course}
        self.render_template("student/lesson_details.html", params)