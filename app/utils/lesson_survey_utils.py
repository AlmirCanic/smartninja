def statements():
    return ["Instructor's presentation was clear and understandable.",
            "Lesson and homework assignments were too difficult.",
            "I learned things I didn't know before at this lesson.",
            "The lesson was too long (too much content).",
            "The lesson was too short (too little content)."]


class Statement:
    __counter = 0
    score = 0.0
    statement = ""

    def __init__(self, lesson_id, lesson_title, lesson_order):
        self.lesson_id = lesson_id
        self.lesson_title = lesson_title
        self.lesson_order = lesson_order

    def increase_counter(self):
        self.__counter += 1

    def count_avg(self):
        self.score = float(self.score / self.__counter)


def survey_statements_summary(surveys):
    """
    Group statements by lesson (lesson id) and statement. Then make a summary of statement scores for each lesson.
    This means you have to group statements and then calculate average score for each statement.

    :param surveys: the "questions" attribute inside LessonSurvey object. It contains all the statements and scores for a survey.
    :return: returns a list of Statement objects that have fields: statement, lesson id, lesson title and avg score
    """
    statements = []

    for survey in surveys:
        for statement, score in survey.questions.iteritems():
            if statement and score:
                right_result = None
                have_result = False

                for item in statements:
                    if item.lesson_id == survey.lesson_id and item.statement == statement:
                        right_result = item
                        have_result = True
                        right_result.score += float(score)
                        break

                if not have_result and score:
                    right_result = Statement(lesson_id=survey.lesson_id, lesson_title=survey.lesson_title,
                                             lesson_order=survey.lesson_order)
                    statements.append(right_result)
                    right_result.statement = statement
                    right_result.score = float(score)

                right_result.increase_counter()

    for item in statements:
        item.count_avg()

    return statements


class LessonStatements:
    def __init__(self, lesson_id, lesson_title, lesson_order):
        self.lesson_id = lesson_id
        self.lesson_title = lesson_title
        self.lesson_order = lesson_order
        self.statements = []


def group_statements_by_lesson(statements_list):
    group = []

    for statement in statements_list:
        have_result = False

        for item in group:
            if item.lesson_id == statement.lesson_id:
                item.statements.append(statement)
                have_result = True
                break

        if not have_result:
            lesson_statement = LessonStatements(lesson_id=statement.lesson_id,
                                                lesson_title=statement.lesson_title,
                                                lesson_order=statement.lesson_order)
            lesson_statement.statements.append(statement)
            group.append(lesson_statement)

    return group