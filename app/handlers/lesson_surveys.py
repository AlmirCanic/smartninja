"""
    Users who attend a course can grade a certain lesson and instructor's presentation
"""
from google.appengine.api import users
from app.handlers.base import Handler
from app.models.auth import User
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.lesson_survey import LessonSurvey
from app.utils.decorators import student_required, admin_required, instructor_required
from app.utils.lesson_survey_utils import statements


# ADMIN
class AdminLessonSurveyList(Handler):
    @admin_required
    def get(self):
        surveys = LessonSurvey.query(LessonSurvey.deleted == False).fetch()

        params = {"surveys": surveys}

        return self.render_template("admin/lesson_survey_list.html", params)


class AdminLessonSurveyDetails(Handler):
    @admin_required
    def get(self, lesson_survey_id):
        survey = LessonSurvey.get_by_id(int(lesson_survey_id))

        params = {"survey": survey}

        return self.render_template("admin/lesson_survey_details.html", params)


# ADMIN
class InstructorLessonSurveyList(Handler):
    @instructor_required
    def get(self):
        user = users.get_current_user()
        instructor = User.get_by_email(user.email().lower())

        surveys = LessonSurvey.query(LessonSurvey.deleted == False,
                                     LessonSurvey.instructor_user_id == instructor.get_id).fetch()

        params = {"surveys": surveys}

        return self.render_template("instructor/lesson_survey_list.html", params)


class InstructorLessonSurveyDetails(Handler):
    @instructor_required
    def get(self, lesson_survey_id):
        survey = LessonSurvey.get_by_id(int(lesson_survey_id))

        params = {"survey": survey}

        return self.render_template("instructor/lesson_survey_details.html", params)


# STUDENT
class StudentLessonSurveyAdd(Handler):
    @student_required
    def get(self, course_id, lesson_id):
        course = Course.get_by_id(int(course_id))
        lesson = Lesson.get_by_id(int(lesson_id))

        questions = statements()  # statements for a lesson survey

        params = {"course": course, "lesson": lesson, "questions": questions}

        return self.render_template("student/lesson_survey_add.html", params)

    @student_required
    def post(self, course_id, lesson_id):
        course = Course.get_by_id(int(course_id))
        lesson = Lesson.get_by_id(int(lesson_id))

        text = self.request.get("text")

        questions = statements()  # statements for a lesson survey

        statement_results = {}

        for counter, question in enumerate(questions):
            result = self.request.get("questions%s" % str(counter+1))
            statement_results[question] = result

        LessonSurvey.create(course=course, lesson=lesson, statements=statement_results, text=text)

        return self.redirect_to("student-course-details", course_id=course_id)