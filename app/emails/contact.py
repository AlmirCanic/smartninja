from google.appengine.api import mail


# a message to info@smartninja.org
def email_contact_us_to_smartninja(first_name, email, message, last_name=None, phone=None):
    message_body = '''
        New message from the contact form!
        Name: {0} {1}
        Email: {2}
        Phone: {3}
        Message: {4}
    '''.format(first_name.encode('utf-8'),
               last_name.encode('utf-8'),
               email.encode('utf-8'),
               phone.encode('utf-8'),
               message.encode('utf-8'))

    html_message_body = '''
        <p>New message from the contact form!</p>
        <p>Name: {0} {1}</p>
        <p>Email: {2}</p>
        <p>Phone: {3}</p>
        <p>Message: {4}</p>
    '''.format(first_name.encode('utf-8'),
               last_name.encode('utf-8'),
               email.encode('utf-8'),
               phone.encode('utf-8'),
               message.encode('utf-8'))

    message = mail.EmailMessage(sender="SmartNinja <info@smartninja.org>",
                                to="info@smartninja.org",
                                subject="New contact form message",
                                reply_to="%s" % email,
                                body=message_body,
                                html=html_message_body)
    message.send()


# a message to info@smartninja.si
def email_contact_us_to_smartninja_si(first_name, email, message, last_name=None, phone=None):
    message_body = '''
        New message from the contact form!
        Name: {0} {1}
        Email: {2}
        Phone: {3}
        Message: {4}
    '''.format(first_name.encode('utf-8'),
               last_name.encode('utf-8'),
               email.encode('utf-8'),
               phone.encode('utf-8'),
               message.encode('utf-8'))

    html_message_body = '''
        <p>New message from the contact form!</p>
        <p>Name: {0} {1}</p>
        <p>Email: {2}</p>
        <p>Phone: {3}</p>
        <p>Message: {4}</p>
    '''.format(first_name.encode('utf-8'),
               last_name.encode('utf-8'),
               email.encode('utf-8'),
               phone.encode('utf-8'),
               message.encode('utf-8'))

    message = mail.EmailMessage(sender="SmartNinja <info@smartninja.org>",
                                to="info@smartninja.si",
                                subject="New contact form message",
                                reply_to="%s" % email,
                                body=message_body,
                                html=html_message_body)
    message.send()