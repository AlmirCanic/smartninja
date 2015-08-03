from app.utils.lesson_survey_utils import survey_statements_summary, group_statements_by_lesson


class Survey:
    def __init__(self, lesson_id, lesson_title, questions):
        self.lesson_id = lesson_id
        self.lesson_title = lesson_title
        self.questions = questions


def test_lesson_survey_statements_summary():
    print "test_lesson_survey_statements_summary() started"

    question1 = {"statement A": "1",
                 "statement B": "2",
                 "statement C": "3"}

    question2 = {"statement A": "1",
                 "statement B": "1",
                 "statement C": "1"}

    question3 = {"statement A": "2",
                 "statement B": "2",
                 "statement C": "2"}

    question4 = {"statement A": "3",
                 "statement B": "2",
                 "statement C": "1"}

    question5 = {"statement A": "1",
                 "statement B": "1",
                 "statement C": "1"}

    question6 = {"statement A": "2",
                 "statement B": "2",
                 "statement C": "2"}

    survey = Survey(lesson_id=111, questions=question1, lesson_title="prva")
    survey2 = Survey(lesson_id=111, questions=question2, lesson_title="prva")
    survey3 = Survey(lesson_id=222, questions=question3, lesson_title="druga")
    survey4 = Survey(lesson_id=222, questions=question4, lesson_title="druga")

    surveys = [survey, survey2, survey3, survey4]

    results = survey_statements_summary(surveys)

    # lesson 111
    assert results[0].lesson_title == "prva"
    print True

    assert len(results) == 6
    print True

    for result in results:
        if result.lesson_id == 111 and result.statement == "statement A":
            assert result.score == 1
            print True

        if result.lesson_id == 111 and result.statement == "statement B":
            assert result.score == float(1.5)
            print True

    assert len(group_statements_by_lesson(results)) == 2
    print True

    assert len(group_statements_by_lesson(results)[0].statements) == 3
    print True

    print "test_lesson_survey_statements_summary() finished"


test_lesson_survey_statements_summary()