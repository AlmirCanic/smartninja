from google.appengine.api import mail


def email_employer_contact_candidate(contact_candidate):
    message_body = '''
        Dear {0}!

        You've got an email from a potential employer:

        "{1}"

        Employer's contact: {2}

        Kind regards,
        SmartNinja Team
    '''.format(contact_candidate.candidate_name, contact_candidate.message, contact_candidate.employer_email)

    html_message_body = '''
        <h2>Dear {0}!</h2>

        <p>You've got an email from a potential employer:<p>

        <blockquote>"{1}"</blockquote>

        <p>Employer's contact: {2}</p>

        <p>If you have any question regarding this email, don't hesitate to contact us</p>

        <p>Kind regards,<br>
        SmartNinja Team</p>
    '''.format(contact_candidate.candidate_name, contact_candidate.message, contact_candidate.employer_email)

    message = mail.EmailMessage(sender="SmartNinja <info@smartninja.org>",
                                to=contact_candidate.candidate_email,
                                subject="New job opportunity",
                                body=message_body,
                                html=html_message_body)
    message.send()