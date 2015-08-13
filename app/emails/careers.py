# a message to info@smartninja.si
from google.appengine.api import mail


def email_careers_to_smartninja_si(full_name, email, city, phone, linkedin, github, experience, other):
    message_body = '''
        New message from the contact form!
        Name: {0}
        City: {1}
        Email: {2}
        Phone: {3}
        LinkedIn: {4}
        GitHub: {5}
        Experience: {6}
        Other info: {7}
    '''.format(full_name.encode('utf-8'),
               city.encode('utf-8'),
               email.encode('utf-8'),
               phone.encode('utf-8'),
               linkedin.encode('utf-8'),
               github.encode('utf-8'),
               experience.encode('utf-8'),
               other.encode('utf-8'))

    html_message_body = '''
        <p>New message from the contact form!</p>
        <p>Name: {0} {1}</p>
        <p>Email: {2}</p>
        <p>Phone: {3}</p>
        <p><a href="{4}">LinkedIn ali online CV</a></p>
        <p><a href="{5}">GitHub</a></p>
        <p>Experience: {6}</p>
        <p>Other info: {7}</p>
    '''.format(full_name.encode('utf-8'),
               city.encode('utf-8'),
               email.encode('utf-8'),
               phone.encode('utf-8'),
               linkedin.encode('utf-8'),
               github.encode('utf-8'),
               experience.encode('utf-8'),
               other.encode('utf-8'))

    message = mail.EmailMessage(sender="SmartNinja <info@smartninja.org>",
                                to="info@smartninja.si",
                                subject="New instructor job application",
                                reply_to="%s" % email,
                                body=message_body,
                                html=html_message_body)
    message.send()