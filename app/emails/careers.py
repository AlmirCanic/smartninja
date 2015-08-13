from google.appengine.api import mail


def email_careers_to_smartninja_si(job, full_name, email, city, phone, linkedin, github, experience, other):
    message_body = '''
        New job application!
        Name: {0}
        City: {1}
        Email: {2}
        Phone: {3}
        LinkedIn: {4}
        GitHub: {5}
        Experience: {6}
        Other info: {7}
        ------------
        Job info
        Job title: {8}
        Curriculum title: {9}
        Job city: {10}
        Job applications so far: {11}
    '''.format(full_name.encode('utf-8'),
               city.encode('utf-8'),
               email.encode('utf-8'),
               phone.encode('utf-8'),
               linkedin.encode('utf-8'),
               github.encode('utf-8'),
               experience.encode('utf-8'),
               other.encode('utf-8'),
               job.title.encode('utf-8'),
               job.curriculum_title.encode('utf-8'),
               job.city.encode('utf-8'),
               job.applied)

    html_message_body = '''
        <p>New job application!</p>
        <p>Name: {0} </p>
        <p>City: {1}</p>
        <p>Email: {2}</p>
        <p>Phone: {3}</p>
        <p><a href="{4}">LinkedIn ali online CV</a></p>
        <p><a href="{5}">GitHub</a></p>
        <p>Experience: {6}</p>
        <p>Other info: {7}</p>
        <h3>Job info</h3>
        <p>Job title: {8}</p>
        <p>Curriculum title: {9}</p>
        <p>Job city: {10}</p>
        <p>Job applications so far: {11}</p>
    '''.format(full_name.encode('utf-8'),
               city.encode('utf-8'),
               email.encode('utf-8'),
               phone.encode('utf-8'),
               linkedin.encode('utf-8'),
               github.encode('utf-8'),
               experience.encode('utf-8'),
               other.encode('utf-8'),
               job.title.encode('utf-8'),
               job.curriculum_title.encode('utf-8'),
               job.city.encode('utf-8'),
               job.applied)

    message = mail.EmailMessage(sender="SmartNinja <info@smartninja.org>",
                                to="info@smartninja.si",
                                subject="New instructor job application for {0}, {1}".format(job.title.encode('utf-8'),
                                                                                             job.city.encode('utf-8')),
                                reply_to="%s" % email,
                                body=message_body,
                                html=html_message_body)
    message.send()