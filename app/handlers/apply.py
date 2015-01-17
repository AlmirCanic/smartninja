import datetime
from app.emails.apply import prijava_februar, email_course_application_thank_you
from app.handlers.base import Handler
from app.models.auth import User
from app.models.course import CourseType, Course, CourseApplication
from app.settings import is_local
from app.utils.decorators import admin_required


class AdminCourseApplicationDetailsHandler(Handler):
    @admin_required
    def get(self, application_id):
        application = CourseApplication.get_by_id(int(application_id))
        user_id = application.student_id
        user = User.get_by_id(user_id)
        params = {"application": application, "this_user": user}
        self.render_template("admin/application_details.html", params)

    @admin_required
    def post(self, application_id):
        application = CourseApplication.get_by_id(int(application_id))
        application.payment_status = bool(self.request.get("paid"))
        application.price = float(self.request.get("price"))
        application.invoice = self.request.get("invoice")
        application.put()
        self.redirect_to("course-details", course_id=application.course_id)


class AdminCourseApplicationDeleteHandler(Handler):
    @admin_required
    def get(self, application_id):
        application = CourseApplication.get_by_id(int(application_id))
        params = {"application": application}
        self.render_template("admin/application_delete.html", params)

    @admin_required
    def post(self, application_id):
        application = CourseApplication.get_by_id(int(application_id))
        application.deleted = True
        application.put()
        course = Course.get_by_id(int(application.course_id))
        course.taken -= 1
        course.put()
        self.redirect_to("course-details", course_id=application.course_id)


# TODO: just temporary, delete after feb 2015
class TempPrijavaHandler(Handler):
    def post(self):
        hidden = self.request.get("hidden")
        if hidden:
            return self.redirect_to("temp")
        else:
            ime = self.request.get("firstname")
            priimek = self.request.get("lastname")
            email = self.request.get("email").strip()
            naslov = self.request.get("address")
            starost = self.request.get("age")
            telefon = self.request.get("phone2")
            kraj_tecaja = self.request.get("country")
            kotizacija = self.request.get("sleepover")
            prenosnik = self.request.get("prenosnik")
            majica = self.request.get("majica")

            if ime and priimek and email and naslov and starost and telefon and kraj_tecaja and kotizacija and prenosnik and majica:
                user = User.get_by_email(email)

                if not user:
                    # add to database
                    user = User.create(first_name=ime, last_name=priimek, email=email, address=naslov, dob=starost, phone_number=telefon)

                course_app = add_user_to_course(user=user, kraj_tecaja=kraj_tecaja, kotizacija=float(kotizacija), prenosnik=prenosnik, majica=majica)

                # send email to info@smartninja.org
                if not is_local():
                    prijava_februar(ime, priimek, email, naslov, starost, telefon, kraj_tecaja, kotizacija, prenosnik, majica)

                # send email to the student
                if not is_local():
                    email_course_application_thank_you(course_app)

                params = {"error": "Prijava oddana! :)"}
            else:
                params = {"error": "Prosim izpolni vsa polja"}
        self.render_template("public/main2.html", params)


# TODO: just temporary, delete after feb 2015
def add_user_to_course(user, kraj_tecaja, kotizacija, prenosnik, majica):
    course_type = CourseType.query(CourseType.title == "SmartNinja Vikend Slovenia").get()
    if not course_type:
        course_type = CourseType()
        course_type.title = "SmartNinja Vikend Slovenia"
        course_type.put()

    course = None

    price = [97.00, 147.00, 197.00]

    if kraj_tecaja == "Ljubljana":
        course = Course.query(Course.title == "SmartNinja Vikend Ljubljana").get()
        if not course:
            course = Course.create(title="SmartNinja Vikend Ljubljana", city="Ljubljana", start_date=datetime.date(2015, 2, 7),
                                   end_date=datetime.date(2015, 2, 8), description="", price=price, place="",
                                   course_type=course_type.get_id, currency="EUR", spots=10)
    elif kraj_tecaja == "Maribor":
        course = Course.query(Course.title == "SmartNinja Vikend Maribor").get()
        if not course:
            course = Course.create(title="SmartNinja Vikend Maribor", city="Maribor", start_date=datetime.date(2015, 2, 14),
                                   end_date=datetime.date(2015, 2, 15), description="", price=price, place="",
                                   course_type=course_type.get_id, currency="EUR", spots=10)
    elif kraj_tecaja == "NovaGorica":
        course = Course.query(Course.title == "SmartNinja Vikend Nova Gorica").get()
        if not course:
            course = Course.create(title="SmartNinja Vikend Nova Gorica", city="Nova Gorica", start_date=datetime.date(2015, 2, 28),
                                   end_date=datetime.date(2015, 3, 1), description="", price=price, place="",
                                   course_type=course_type.get_id, currency="EUR", spots=10)

    if course:
        course_app = CourseApplication.create(course_title=course.title, course_id=course.get_id, student_name=user.get_full_name,
                                              student_id=user.get_id, student_email=user.email, price=kotizacija, currency="EUR",
                                              laptop=prenosnik, shirt=majica)
        course.taken += 1
        course.put()
        return course_app