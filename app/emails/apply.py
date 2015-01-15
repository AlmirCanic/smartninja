import os
from google.appengine.api import mail
import jinja2
from app.handlers.newsletter import subscribe_mailchimp

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               extensions=['jinja2.ext.autoescape'],
                               autoescape=False)


def prijava_februar(ime, priimek, email, naslov, starost, telefon, kraj_tecaja, kotizacija, prenosnik, majica):
    message_body = '''
        Nova prijava na Februar 2015!
        Ime in priimek: {0} {1}
        Email: {2}
        Naslov: {3}
        Starost: {4}
        Telefon: {5}
        Kraj tecaja: {6}
        Kotizacija: {7} EUR
        Svoj prenosnik: {8}
        Velikost majice: {9}
    '''.format(ime.encode('utf-8'),
               priimek.encode('utf-8'),
               email.encode('utf-8'),
               naslov.encode('utf-8'),
               starost.encode('utf-8'),
               telefon.encode('utf-8'),
               kraj_tecaja.encode('utf-8'),
               kotizacija.encode('utf-8'),
               prenosnik.encode('utf-8'),
               majica.encode('utf-8'))

    html_message_body = '''
        <p>Nova prijava na Februar 2015!</p>
        <p>Ime in priimek: {0} {1}</p>
        <p>Email: {2}</p>
        <p>Naslov: {3}</p>
        <p>Starost: {4}</p>
        <p>Telefon: {5}</p>
        <p>Kraj tecaja: {6}</p>
        <p>Kotizacija: {7} EUR</p>
        <p>Svoj prenosnik: {8}</p>
        <p>Velikost majice: {9}</p>
    '''.format(ime.encode('utf-8'),
               priimek.encode('utf-8'),
               email.encode('utf-8'),
               naslov.encode('utf-8'),
               starost.encode('utf-8'),
               telefon.encode('utf-8'),
               kraj_tecaja.encode('utf-8'),
               kotizacija.encode('utf-8'),
               prenosnik.encode('utf-8'),
               majica.encode('utf-8'))

    message = mail.EmailMessage(sender="SmartNinja <info@smartninja.org>",
                                to="info@smartninja.org",
                                subject="Nova prijava na Februar 2015 - {0}".format(kraj_tecaja.encode('utf-8')),
                                reply_to="{0}".format(email.encode('utf-8')),
                                body=message_body,
                                html=html_message_body)
    message.send()


def email_course_application_thank_you(course_app):
    params = {"course_app": course_app}
    html_template = jinja_env.get_template("emails/si/course_application.html")
    text_template_path = os.path.join(os.path.dirname(__file__), '../templates/emails/si/course_application.txt')

    with open(text_template_path, "r") as text_template:
        message_body = text_template.read().format(course_app.course_title.encode('utf-8'),
                                                   course_app.student_name.encode('utf-8'),
                                                   course_app.student_email.encode('utf-8'),
                                                   course_app.price,
                                                   course_app.laptop.encode('utf-8'),
                                                   course_app.shirt.encode('utf-8'))

    html_message_body = html_template.render(params)

    message = mail.EmailMessage(sender="SmartNinja <info@smartninja.org>",
                                to=course_app.student_email,
                                subject="Hvala za prijavo na %s" % course_app.course_title,
                                body=message_body,
                                html=html_message_body)
    message.send()

    subscribe_mailchimp(course_app.student_email)