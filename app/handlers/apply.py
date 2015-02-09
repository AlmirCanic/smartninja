import datetime
from app.emails.apply import prijava_februar, email_course_application_thank_you, email_course_app_to_smartninja
from app.handlers.base import Handler
from app.models.auth import User
from app.models.course import CourseType, Course, CourseApplication
from app.settings import is_local
from app.utils.csrf import check_csrf
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
        CourseApplication.delete(application=application)
        self.redirect_to("course-details", course_id=application.course_id)


# PUBLIC

class PublicCourseApplicationAddHandler(Handler):
    def post(self, course_id):
        hidden = self.request.get("hidden")
        csrf = self.request.get("csrf")
        if hidden:
            return self.redirect_to("public-course-details", course_id=int(course_id))
        elif check_csrf(csrf):
            first_name = self.request.get("first_name")
            last_name = self.request.get("last_name")
            email = self.request.get("email").strip()
            address = self.request.get("address")
            dob = self.request.get("dob")
            phone = self.request.get("phone")
            laptop = self.request.get("laptop")
            shirt = self.request.get("shirt")
            price = self.request.get("price")
            company = self.request.get("company_invoice")
            other_info = self.request.get("other_info")

            # TODO: invoice on company

            if first_name and last_name and email and address and dob and phone and laptop and shirt:
                user = User.get_by_email(email)

                if not user:
                    # add user to database
                    user = User.create(first_name=first_name, last_name=last_name, email=email, address=address,
                                       dob=dob, phone_number=phone)

                course = Course.get_by_id(int(course_id))

                if not price:
                    try:
                        price = str(course.prices[0].price_dot)
                    except:
                        price = str(course.price[0])

                if company:
                    company_title = self.request.get("company_title")
                    company_address = self.request.get("company_address")
                    company_zip = self.request.get("company_zip")
                    company_town = self.request.get("company_town")
                    company_tax = self.request.get("company_tax")
                    course_app = CourseApplication.create(course=course, student_name=user.get_full_name,
                                                          student_id=user.get_id, student_email=email,
                                                          price=float(price), currency=course.currency, laptop=laptop,
                                                          shirt=shirt, company_invoice=True, company_title=company_title,
                                                          company_address=company_address, company_zip=company_zip,
                                                          company_town=company_town, company_tax_number=company_tax,
                                                          other_info=other_info)
                elif not company:
                    course_app = CourseApplication.create(course=course, student_name=user.get_full_name, student_id=user.get_id,
                                                      student_email=email, price=float(price), currency=course.currency,
                                                      laptop=laptop, shirt=shirt, other_info=other_info)
                else:
                    return self.redirect_to("oops")

                # send email to info@smartninja.org
                if not is_local():
                    email_course_app_to_smartninja(course=course, user=user, application=course_app)

                # send email to the student
                if not is_local():
                    email_course_application_thank_you(course_app)

                return self.redirect_to("apply-thank-you")
            else:
                # TODO: error in params
                return self.redirect_to("oops")
        else:
            return self.redirect_to("oops")