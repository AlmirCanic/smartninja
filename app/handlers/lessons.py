from app.handlers.base import Handler
from app.models.course import CourseType
from app.models.lesson import Lesson
from app.utils.decorators import admin_required
from app.utils.other import convert_markdown_to_html


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
            Lesson.create(title=title, order=int(order), text=text, course_type=int(course_type_id))
            self.redirect_to("course-type-details", course_type_id=course_type_id)


class AdminLessonDetailsHandler(Handler):
    @admin_required
    def get(self, lesson_id):
        lesson = Lesson.get_by_id(int(lesson_id))
        course_type = CourseType.get_by_id(lesson.course_type)
        lesson.text = convert_markdown_to_html(lesson.text)
        params = {"lesson": lesson, "course_type": course_type}
        self.render_template("admin/lesson_details.html", params)