import datetime
from app.handlers.base import Handler
from app.models.auth import User
from app.models.course import CourseType, Course, Price, CourseInstructor, CourseApplication
from app.models.employer import Employer
from app.models.franchise import Franchise
from app.models.instructor import Instructor
from app.models.student import StudentCourse
from app.utils.decorators import admin_required
from app.settings import is_local
from app.utils.other import convert_tags_to_list


class LocalhostFakeDataHandler(Handler):
    @admin_required
    def get(self):
        if is_local():
            # generate a curriculum
            curriculum = CourseType.create(title="Programming Weekend",
                                           curriculum="/", description="/")

            # generate user (out of admin)
            admin = User.short_create(email="matej.ramuta@gmail.com", first_name="Matej", last_name="Ramuta")
            admin.photo_url = "http://localhost:20080/assets/img/public/matej_ramuta.jpg"
            admin.summary = "Experienced web and mobile developer, mostly working with Python and Android."
            admin.put()

            # add user to employer, instructor lists
            Instructor.create(full_name=admin.get_full_name, user_id=admin.get_id, email=admin.email)
            Employer.create(full_name=admin.get_full_name, user_id=admin.get_id, email=admin.email)

            instructor = CourseInstructor(name=admin.get_full_name, summary=admin.summary,
                                          photo_url=admin.photo_url, user_id=admin.get_id)

            # generate franchise
            franchise = Franchise.create(title="SmartNinja Slovenija", full_company_name="SNIT d.o.o.", street="Bla 12",
                                         city="Novo mesto", zip="8000", country="Slovenia", website="je ni",
                                         tax_number="32543254")

            # create courses
            course1 = Course.create(title="HTML Weekend", course_type=curriculum.get_id, city="Ljubljana",
                                    place="Poligon", spots=10, summary="bla", description="bla bla",
                                    start_date=datetime.date(2015, 11, 5), end_date=datetime.date(2015, 12, 5),
                                    prices=[Price(price_dot=99.0, price_comma="99,00", summary="All")],
                                    category="Programming", course_instructors=[instructor], currency="EUR",
                                    image_url="http://i.imgur.com/9Dy2wa8.jpg", partners=[],
                                    tags=convert_tags_to_list("2 days,HTML,Ljubljana"), franchise=franchise, level=1)

            course2 = Course.create(title="Startup marketing", course_type=curriculum.get_id, city="Ljubljana",
                                    place="TPLJ", spots=10, summary="juhu", description="juhu bruhu",
                                    start_date=datetime.date(2015, 10, 22), end_date=datetime.date(2015, 11, 2),
                                    prices=[Price(price_dot=99.0, price_comma="99,00", summary="All")],
                                    category="Marketing", course_instructors=[instructor], currency="EUR",
                                    image_url="http://i.imgur.com/Wo2RFcg.jpg", partners=[],
                                    tags=convert_tags_to_list("2 days,HTML,Ljubljana"), franchise=franchise, level=1)

            # create new users (job searching true)
            student1 = User.short_create(email="bjanko@gmail.com", first_name="Janko", last_name="Bananko")
            student2 = User.short_create(email="mpiha@gmail.com", first_name="Miha", last_name="Piha")

            student1.job_searching = True
            student1.photo_url = "http://i.imgur.com/ibe57bY.jpg"
            student1.current_town = "Ljubljana"
            student1.github_url = "http://github.com/EgonR"
            student1.summary = "IT enthusiast. Started programming in HTML and CSS. Looking for a job. Hard worker."
            student1.put()

            student2.job_searching = True
            student2.photo_url = "http://i.imgur.com/jwazgX4.jpg"
            student2.current_town = "Kamnik"
            student2.github_url = "http://github.com/DavorPadovan"
            student2.summary = "I love IT and programming. Have developed a website for my grandma."
            student2.put()

            # apply users to courses (+ student grades)
            application1 = CourseApplication.create(course=course1, currency="EUR", laptop="yes", price=99.0,
                                                    shirt="M", student_email=student1.email, student_id=student1.get_id,
                                                    student_name=student1.get_full_name)
            application1.payment_status = True
            StudentCourse.create(user_id=student1.get_id, user_name=student1.get_full_name, user_email=student1.email,
                                 course=course1)
            CourseApplication.grade_student(application=application1, score=3, summary="Very good", tags=["HTML", "CSS"])
            application1.put()

            application2 = CourseApplication.create(course=course1, currency="EUR", laptop="yes", price=99.0,
                                                    shirt="L", student_email=student2.email, student_id=student2.get_id,
                                                    student_name=student2.get_full_name)
            CourseApplication.grade_student(application=application2, score=2, summary="Medium", tags=["HTML"])
            application2.payment_status = True
            StudentCourse.create(user_id=student2.get_id, user_name=student2.get_full_name, user_email=student2.email,
                                 course=course1)
            application2.put()

            application3 = CourseApplication.create(course=course2, currency="EUR", laptop="yes", price=99.0,
                                                    shirt="M", student_email=student1.email, student_id=student1.get_id,
                                                    student_name=student1.get_full_name)

            self.redirect_to("admin")