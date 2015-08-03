"""
    Users who attend a course can grade a certain lesson and instructor's presentation
"""
import datetime
from google.appengine.api import users
import operator
from app.handlers.base import Handler
from app.models.auth import User
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.lesson_survey import LessonSurvey
from app.utils.decorators import student_required, admin_required, instructor_required
from app.utils.lesson_survey_utils import statements, survey_statements_summary, group_statements_by_lesson


# ADMIN
class AdminLessonSurveyList(Handler):
    @admin_required
    def get(self):
        courses = Course.query(Course.deleted == False,
                               Course.end_date >= datetime.date.today()).order(Course.end_date).fetch()

        params = {"current_courses": courses}

        return self.render_template("admin/lesson_survey_list.html", params)


class AdminLessonSurveyPastList(Handler):
    @admin_required
    def get(self):
        courses = Course.query(Course.deleted == False,
                               Course.end_date < datetime.date.today()).order(Course.end_date).fetch()

        params = {"past_courses": courses}

        return self.render_template("admin/lesson_survey_past_list.html", params)


class AdminCourseSurveysHandler(Handler):
    @admin_required
    def get(self, course_id):
        course = Course.get_by_id(int(course_id))
        surveys = LessonSurvey.query(LessonSurvey.course_id == int(course_id),
                                     LessonSurvey.deleted == False).order(-LessonSurvey.created).fetch()

        survey_summary = survey_statements_summary(surveys)

        summary_groups = group_statements_by_lesson(survey_summary)

        summary_groups.sort(key=operator.attrgetter("lesson_order"))

        params = {"course": course, "surveys": surveys, "summary": summary_groups}
        return self.render_template("admin/lesson_surveys_for_course.html", params=params)


class AdminLessonSurveyDetails(Handler):
    @admin_required
    def get(self, lesson_survey_id):
        survey = LessonSurvey.get_by_id(int(lesson_survey_id))

        params = {"survey": survey}

        return self.render_template("admin/lesson_survey_details.html", params)


# INSTRUCTOR
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