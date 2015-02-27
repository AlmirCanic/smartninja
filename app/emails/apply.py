import os
import datetime
from google.appengine.api import mail
import jinja2
from app.handlers.newsletter import subscribe_mailchimp

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               extensions=['jinja2.ext.autoescape'],
                               autoescape=False)


def email_course_app_to_smartninja(course, user, application):
    message_body = '''
        New application for {0}!
        Name: {1}
        Email: {2}
        Address: {3}
        DOB: {4}
        Phone number: {5}
        Course address: {6} ({7})
        Price: {8} {9}
        Has laptop: {10}
        T-shirt size: {11}
        Invoice on company: {12} (if True, see application details)
        Other info: {13}
    '''.format(course.title.encode('utf-8'),
               user.get_full_name.encode('utf-8'),
               user.email.encode('utf-8'),
               user.address.encode('utf-8'),
               user.dob.encode('utf-8'),
               user.phone_number.encode('utf-8'),
               course.city.encode('utf-8'),
               course.place.encode('utf-8'),
               application.price,
               application.currency.encode('utf-8'),
               application.laptop.encode('utf-8'),
               application.shirt.encode('utf-8'),
               application.company_invoice,
               application.other_info.encode('utf-8'))

    html_message_body = '''
        <p>New application for {0}!</p>
        <p>Name: {1}</p>
        <p>Email: {2}</p>
        <p>Address: {3}</p>
        <p>DOB: {4}</p>
        <p>Phone number: {5}</p>
        <p>Course address: {6} ({7})</p>
        <p>Price: {8} {9}</p>
        <p>Has laptop: {10}</p>
        <p>T-shirt size: {11}</p>
        <p>Invoice on company: {12} (if True, see application details)</p>
        <p>Other info: {13}</p>
    '''.format(course.title.encode('utf-8'),
               user.get_full_name.encode('utf-8'),
               user.email.encode('utf-8'),
               user.address.encode('utf-8'),
               user.dob.encode('utf-8'),
               user.phone_number.encode('utf-8'),
               course.city.encode('utf-8'),
               course.place.encode('utf-8'),
               application.price,
               application.currency.encode('utf-8'),
               application.laptop.encode('utf-8'),
               application.shirt.encode('utf-8'),
               application.company_invoice,
               application.other_info.encode('utf-8'))

    message = mail.EmailMessage(sender="SmartNinja <info@smartninja.org>",
                                to="info@smartninja.org",
                                subject="New application for {0}".format(course.title.encode('utf-8')),
                                reply_to="%s" % user.email,
                                body=message_body,
                                html=html_message_body)
    message.send()


def email_course_application_thank_you(course_app):
    import time
    ts = int(time.time())
    final_date = course_app.created + datetime.timedelta(days=8)
    price_str = str(course_app.price).replace(".0", ",00")

    params = {"course_app": course_app, "ts": ts, "final_date": final_date, "price_str": price_str}

    html_template = jinja_env.get_template("emails/si/course_application.html")

    if course_app.company_invoice:
        text_template_path_company = os.path.join(os.path.dirname(__file__), '../templates/emails/si/course_application_company.txt')
        with open(text_template_path_company, "r") as text_template:
            message_body = text_template.read().format(course_app.company_title.encode('utf-8'),
                                                       course_app.company_address.encode('utf-8'),
                                                       course_app.company_zip.encode('utf-8'),
                                                       course_app.company_town.encode('utf-8'),
                                                       course_app.company_tax_number.encode('utf-8'),
                                                       ts,
                                                       "%s.%s.%s" % (course_app.created.day, course_app.created.month, course_app.created.year),
                                                       "%s.%s.%s" % (final_date.day, final_date.month, final_date.year),
                                                       course_app.course_title.encode('utf-8'),
                                                       price_str,
                                                       course_app.price)
    else:
        text_template_path_user = os.path.join(os.path.dirname(__file__), '../templates/emails/si/course_application.txt')
        with open(text_template_path_user, "r") as text_template:
            message_body = text_template.read().format(course_app.student_name.encode('utf-8'),
                                                       ts,
                                                       "%s.%s.%s" % (course_app.created.day, course_app.created.month, course_app.created.year),
                                                       "%s.%s.%s" % (final_date.day, final_date.month, final_date.year),
                                                       course_app.course_title.encode('utf-8'),
                                                       price_str,
                                                       course_app.price)

    html_message_body = html_template.render(params)

    message = mail.EmailMessage(sender="SmartNinja <info@smartninja.org>",
                                to=course_app.student_email,
                                subject="Predracun za SmartNinja tecaj",
                                body=message_body,
                                html=html_message_body)
    message.send()

    subscribe_mailchimp(course_app.student_email)