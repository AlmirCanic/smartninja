from app.emails.apply import prijava_februar
from app.handlers.base import Handler


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

            if ime and priimek and email and naslov and starost and telefon and kraj_tecaja and kotizacija:
                prijava_februar(ime, priimek, email, naslov, starost, telefon, kraj_tecaja, kotizacija)
                params = {"error": "Prijava oddana! :)"}
            else:
                params = {"error": "Prosim izpolni vsa polja"}
        self.render_template("public/main2.html", params)