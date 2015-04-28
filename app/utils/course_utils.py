def update_student_grade(application):
    from app.models.auth import User
    from app.models.course import CourseApplication
    student = User.get_by_id(application.student_id)
    applications = CourseApplication.query(CourseApplication.student_id == application.student_id).fetch()
    grade_score_sum = 0
    num_of_grades = 0
    all_grade_tags = []
    for course_app in applications:
        if course_app.grade_score:
            grade_score_sum += course_app.grade_score
            num_of_grades += 1

        if course_app.grade_tags:
            all_grade_tags += course_app.grade_tags

    student.grade_avg_score = float(grade_score_sum) / float(num_of_grades)
    student.grade_all_tags = list(set(all_grade_tags))
    student.put()