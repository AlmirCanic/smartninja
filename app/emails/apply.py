import os
from google.appengine.api import mail
import jinja2
from app.handlers.newsletter import subscribe_mailchimp

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               extensions=['jinja2.ext.autoescape'],
                               autoescape=False)


def email_course_app_to_smartninja(course, user, application):
    if not user.address:
        user.address = "/"

    if not user.dob:
        user.dob = "/"

    if not user.phone_number:
        user.phone_number = "/"

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
        ----------------
        Course info
        Course title: {14}
        Course spots taken: {15}/{16}
        Course start/end date: {17} - {18}
        Course instructor: {19}
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
               application.other_info.encode('utf-8'),
               course.title.encode('utf-8'),
               course.taken,
               course.spots,
               course.start_date,
               course.end_date,
               course.course_instructors[0].name.encode('utf-8'))

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
        ----------------
        <h3>Course info</h3>
        <p>Course title: {14}</p>
        <p>Course spots taken: {15}/{16}</p>
        <p>Course start/end date: {17} - {18}</p>
        <p>Course instructor: {19}</p>
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
               application.other_info.encode('utf-8'),
               course.title.encode('utf-8'),
               course.taken,
               course.spots,
               course.start_date,
               course.end_date,
               course.course_instructors[0].name.encode('utf-8'))

    message = mail.EmailMessage(sender="SmartNinja <info@smartninja.org>",
                                to="info@smartninja.si",
                                subject="New application for {0} ({1})".format(course.title.encode('utf-8'),
                                                                               course.course_instructors[0].name.encode('utf-8')),
                                reply_to="%s" % user.email,
                                body=message_body,
                                html=html_message_body)
    message.send()


def email_course_application_thank_you(course_app, ts, final_date, price_str):
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
                                subject="Hvala za prijavo na {0}".format(course_app.course_title.encode('utf-8')),
                                reply_to="SmartNinja Slovenija <info@smartninja.si>",
                                body=message_body,
                                html=html_message_body)
    message.send()

    subscribe_mailchimp(course_app.student_email)


def email_course_application_thank_you_2(course_app):
    message_body = '''
        Hvala za prijavo na SmartNinja tecaj. V kratkem dobis email s predracunom ter email za prijavo na nase e-novice.

        POZOR: V kolikor teh emailov ne dobis, poglej pod spam.

        Lep pozdrav,
        Ekipa SmartNinja
    '''

    html_template = jinja_env.get_template("emails/si/hvala_za_prijavo.html")
    html_message_body = html_template.render()

    message = mail.EmailMessage(sender="SmartNinja <info@smartninja.org>",
                                to=course_app.student_email,
                                subject="Hvala za prijavo na {0}".format(course_app.course_title.encode('utf-8')),
                                reply_to="SmartNinja Slovenija <info@smartninja.si>",
                                body=message_body,
                                html=html_message_body)
    message.send()