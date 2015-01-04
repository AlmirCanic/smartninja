from google.appengine.api import mail


def prijava_februar(ime, priimek, email, naslov, starost, telefon, kraj_tecaja, kotizacija):
    message_body = '''
        Nova prijava na Februar 2015!
        Ime in priimek: {0} {1}
        Email: {2}
        Naslov: {3}
        Starost: {4}
        Telefon: {5}
        Kraj tecaja: {6}
        Kotizacija: {7} EUR
    '''.format(ime.encode('utf-8'),
               priimek.encode('utf-8'),
               email.encode('utf-8'),
               naslov.encode('utf-8'),
               starost.encode('utf-8'),
               telefon.encode('utf-8'),
               kraj_tecaja.encode('utf-8'),
               kotizacija.encode('utf-8'))

    html_message_body = '''
        <p>Nova prijava na Februar 2015!</p>
        <p>Ime in priimek: {0} {1}</p>
        <p>Email: {2}</p>
        <p>Naslov: {3}</p>
        <p>Starost: {4}</p>
        <p>Telefon: {5}</p>
        <p>Kraj tecaja: {6}</p>
        <p>Kotizacija: {7} EUR</p>
    '''.format(ime.encode('utf-8'),
               priimek.encode('utf-8'),
               email.encode('utf-8'),
               naslov.encode('utf-8'),
               starost.encode('utf-8'),
               telefon.encode('utf-8'),
               kraj_tecaja.encode('utf-8'),
               kotizacija.encode('utf-8'))

    message = mail.EmailMessage(sender="SmartNinja <info@smartninja.org>",
                                to="info@smartninja.org",
                                subject="Nova prijava na Februar 2015",
                                body=message_body,
                                html=html_message_body)
    message.send()